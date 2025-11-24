import threading
import queue
import time
from typing import List, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot

from src.TeaCOPER.manager import LogManager
from src.TeaCOPER.module import SelectModule
from src.TeaCOPER.model import Course
from src.TeaCOPER.thread import WorkerThread
from src.TeaCOPER.utils import SessionUtil
from src.TeaCOPER.utils import ConfigUtil

logger = LogManager("控制线程")

class ControlThread(QObject, threading.Thread):
    course_status_changed = Signal(str, str)   # 课程代码 : 状态
    worker_status_changed = Signal(int, str)   # 线程号 : 状态
    process_finished = Signal(int, int)        # 完成数 : 总数

    def __init__(self):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.daemon = True

        self.session = SessionUtil.getSession()

        self.command_queue = queue.Queue()     # 命令队列 : GUI -> 控制线程
        #self.worker_queue = queue.Queue()     # 工作队列 : 工作线程 -> 控制线程
        self.status_queue = queue.Queue()      # 状态队列 : 工作线程 -> 控制线程
        self.resource_queue = queue.Queue()    # 资源队列 : 控制线程 -> 工作线程

        self.resource_lock = threading.Lock()  # 资源锁 : 防止资源抢占
        self.time_lock = threading.Lock()      # 时间锁 : 用于规定最小抢课间隔

        self.workers = []
        self.running = False
        self.course_list = []

    def run(self):
        """控制线程主循环"""
        self.running = True
        self._start_workers()

        while self.running:
            try:
                # 监听并处理来自前端的命令
                self._process_commands()

                # 处理工作线程状态更新
                self._process_worker_status_update()

                # 检查工作线程状态
                self._check_workers_status()

                time.sleep(0.1)
            except Exception as e:
                logger.error(e)

    def _start_workers(self):
        from src.TeaCOPER.module import SelectModule
        from src.TeaCOPER.module import LoginModule


        # 初始化session
        logger.info("正在获取会话")
        self.session = SessionUtil.initSession(self.session)
        logger.info("成功获取会话")

        # 模拟登录
        logger.info("正在模拟登录")
        login_module = LoginModule(self.session)
        get = login_module.login()
        logger.debug(get)
        logger.info("完成模拟登录")

        ### 这里需要补充验证方法来激活会话
        ### 否则后续抢课进程无法进行，会被重定向回主页
        ### 等待开发这一部分

        # 创建工作线程
        for i in range(ConfigUtil.readConfigFile("select")["ThreadNum"]): # 配置文件修改线程数
            worker = WorkerThread(
                worker_id = i,
                session = self.session,
                course_list = self.course_list,
                status_queue = self.status_queue,
                resource_queue = self.resource_queue,
                resource_lock = self.resource_lock,
                time_lock = self.time_lock
            )
            self.workers.append(worker)
            worker.start()
            self.worker_status_changed.emit(i,"Waiting")

    def _process_commands(self):
        """处理来自前端的命令"""
        try:
            while not self.command_queue.empty():
                command = self.command_queue.get()
                self._execute_command(command)
        except queue.Empty:
            pass
        except Exception as e:
            logger.error(e)

    def _execute_command(self, command: Dict[str, Any]):
        """执行具体命令"""
        cmd_type = command.get("type")

        if cmd_type == "start_selection":      #开始选课
            self.course_list = command.get("courses")
            self._distribute_courses()
        elif cmd_type == "stop_selection":     #结束选课
            self.running = False
            self._stop_workers()
        elif cmd_type == "pause_selection":    #暂停选课
            self._pause_workers()
        elif cmd_type == "resume_selection":   #继续选课
            self._resume_workers()
        elif cmd_type == "update_settings":    #更新设置
            settings = command.get("settings")
            self.resource_queue.put(settings)

    def _distribute_courses(self):
        """分配课程到工作线程"""
        # 若课程列表为空则不创建资源
        if not self.course_list:
            return

        # 遍历课程列表
        for course in self.course_list:
            # 创建资源数据包
            resource = {
                'type' : 'course',
                'course' : course,
                'status' : 'waiting',
                'order' : -1
            }

            self.resource_queue.put(resource)

    def _process_worker_status_update(self):
        """处理工作线程状态更新"""
        try:
            while not self.status_queue.empty():
                # 若状态队列有工作线程传递的状态更新，则对其进行处理
                status = self.status_queue.get()
                self._handle_status(status)
        except queue.Empty:
            pass
        except Exception as e:
            logger.error(e)

    def _handle_status(self, status: Dict[str, Any]):
        """处理单个状态变化"""
        # 获取状态更新类型
        type = status.get("type")

        if type == "course_status_changed":
            # 若是课程状态更新则交由课程状态信号处理
            course_id = status.get("course_id")
            status = status.get("status")
            self.course_status_changed.emit(course_id, status)

        elif type == "worker_status_changed":
            # 若是线程状态更新则交由线程状态信号处理
            worker_id = status.get("worker_id")
            status = status.get("status")
            self.worker_status_changed.emit(worker_id, status)


    def _check_workers_status(self):
        """检查工作线程状态"""
        # 便利所有工作线程
        for i,worker in enumerate(self.workers):
            # 若出现莫名其妙停止则上报错误
            if not worker.is_alive():
                logger.warn("检测到有工作线程异常停止")
                if worker.course != None:
                    course = worker.course
                    self.resource_queue.put(course)
                self.worker_status_changed.emit(i,"Excepted")
                self._restart_worker(i)

    def _restart_worker(self, worker_id):
        try:
            logger.info("正在重启异常停止的工作线程")
            worker = WorkerThread(
                worker_id=worker_id,
                session=self.session,
                course_list=self.course_list,
                status_queue=self.status_queue,
                resource_queue=self.resource_queue,
                resource_lock=self.resource_lock,
                time_lock=self.time_lock
            )

            worker.start()
            self.workers[worker_id] = worker
            self.worker_status_changed.emit(worker_id, "Waiting")
            logger.info("重启工作线程成功")
        except Exception as e:
            logger.error(e)

    def _stop_workers(self):
        """停止所有工作线程"""
        for worker in self.workers:
            worker.stop()

    def _pause_workers(self):
        """暂停所有工作线程"""
        for worker in self.workers:
            worker.pause()

    def _resume_workers(self):
        """恢复所有工作成饭"""
        for worker in self.workers:
            worker.resume()

    def start_selection(self, courses: List[Course]):
        """开始选课"""
        command = {
            "type" : "start_selection",
            "courses" : courses
        }
        self.command_queue.put(command)

    def stop_selection(self):
        """停止选课"""
        command = {
            "type" : "stop_selection",
        }
        self.command_queue.put(command)

    def update_settings(self, settings : Dict[str , Any]):
        """更新设置"""
        command = {
            "type" : "update_settings",
            "settings" : settings
        }
        self.command_queue.put(command)

