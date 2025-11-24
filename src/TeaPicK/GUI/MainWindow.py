# MainWindow.py
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QTextEdit, QWidget,
                             QLabel, QProgressBar)
from PyQt6.QtCore import QTimer
from src.TeaCOPER.thread import ControlThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.control_thread = ControlThread()
        self.init_ui()
        self.connect_signals()
        self.control_thread.start()

    def init_ui(self):
        self.setWindowTitle("选课系统 - 多线程版")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 控制按钮
        control_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始选课")
        self.stop_btn = QPushButton("停止")
        self.pause_btn = QPushButton("暂停")

        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.pause_btn)
        layout.addLayout(control_layout)

        # 工作线程状态
        self.worker_status_layout = QVBoxLayout()
        layout.addLayout(self.worker_status_layout)

        # 课程状态
        layout.addWidget(QLabel("选课状态:"))
        self.course_list = QListWidget()
        layout.addWidget(self.course_list)

        # 日志输出
        layout.addWidget(QLabel("运行日志:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # 连接信号
        self.start_btn.clicked.connect(self.start_selection)
        self.stop_btn.clicked.connect(self.stop_selection)
        self.pause_btn.clicked.connect(self.pause_selection)

    def connect_signals(self):
        self.control_thread.course_status_changed.connect(self.update_course_status)
        self.control_thread.worker_status_changed.connect(self.update_worker_status)
        self.control_thread.overall_progress.connect(self.update_progress)

    def start_selection(self):
        """开始选课"""
        from src.TeaCOPER.module import CourseModule
        from src.TeaCOPER.utils import SessionUtil

        # 获取课程列表
        session = SessionUtil.getSession()
        session = SessionUtil.initSession(session)
        course_module = CourseModule(session)
        courses = course_module.getCourseList()

        self.control_thread.start_selection(courses)
        self.log_text.append("开始选课...")

    def stop_selection(self):
        """停止选课"""
        self.control_thread.stop_selection()
        self.log_text.append("停止选课")

    def pause_selection(self):
        """暂停/恢复选课"""
        if self.pause_btn.text() == "暂停":
            self.control_thread.pause_selection()
            self.pause_btn.setText("恢复")
        else:
            self.control_thread.resume_selection()
            self.pause_btn.setText("暂停")

    def update_course_status(self, course_name, status):
        """更新课程状态"""
        item_text = f"{course_name}: {status}"
        self.course_list.addItem(item_text)
        self.log_text.append(f"课程状态: {item_text}")

    def update_worker_status(self, worker_id, status):
        """更新工作线程状态"""
        self.log_text.append(f"工作线程 {worker_id}: {status}")

    def update_progress(self, completed, total):
        """更新进度"""
        # 可以在这里更新进度条
        pass
