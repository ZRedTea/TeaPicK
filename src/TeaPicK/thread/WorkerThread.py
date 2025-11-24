import threading
from queue import Queue
from typing import List, Dict
from src.TeaCOPER.model import Course, Session


class WorkerThread(threading.Thread):
    def __init__(self, worker_id:int , session:Session,
                 course_list:List[Course], status_queue:Queue, resource_queue:Queue,
                 resource_lock, time_lock):
        threading.Thread.__init__(self)
        self.worker_id = worker_id
        self.session = session
        self.course_list = course_list

        self.status_queue = status_queue       # 状态队列 : 用于向控制线程传递状态更新数据包
        self.resource_queue = resource_queue   # 资源队列 : 用于接收来自控制线程的资源数据包

        self.resource_lock = resource_lock     # 资源锁 : 用于防止资源竞争
        self.time_lock = time_lock             # 时间锁 : 用于实现最小抢课间隔

        self.course = None                     # 标记该线程正在抢的课

        self.status = 1
        self.status_changed = False

    def run(self):
