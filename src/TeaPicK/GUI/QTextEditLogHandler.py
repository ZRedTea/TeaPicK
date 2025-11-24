# 新增文件：src/GUI/QTextEditLogHandler.py
from PyQt6.QtCore import QObject, pyqtSignal
import logging


class QTextEditLogHandler(QObject, logging.Handler):
    """自定义日志处理器，将日志输出到QTextEdit"""

    # 定义信号，用于线程安全的UI更新
    log_signal = pyqtSignal(str, str)  # (message, color)

    def __init__(self, text_edit=None):
        super().__init__()
        self.text_edit = text_edit
        self.log_signal.connect(self._append_log)

        # 设置日志格式（与你的LogManager保持一致）
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)-6s > %(levelname)-5s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.setFormatter(formatter)

    def set_text_edit(self, text_edit):
        """设置文本编辑框"""
        self.text_edit = text_edit

    def emit(self, record):
        """重写emit方法，将日志输出到QTextEdit"""
        if self.text_edit is None:
            return

        msg = self.format(record)

        # 根据日志级别设置颜色（与colorlog颜色对应）
        if record.levelno >= 50:  # CRITI
            color = "red"
        elif record.levelno >= 40:  # ERROR
            color = "red"
        elif record.levelno >= 35:  # WARN
            color = "orange"
        elif record.levelno >= 30:  # COMPE
            color = "green"
        elif record.levelno >= 20:  # INFO
            color = "white"
        else:  # DEBUG
            color = "cyan"

        # 通过信号线程安全地更新UI
        self.log_signal.emit(msg, color)

    def _append_log(self, message, color):
        """实际添加日志到文本区域"""
        html_msg = f'<font color="{color}">{message}</font>'
        self.text_edit.append(html_msg)

        # 自动滚动到底部
        scrollbar = self.text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
