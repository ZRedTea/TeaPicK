import logging
import colorlog
import datetime
import os

from PyQt6.QtCore import QObject, pyqtSignal as Signal
from PyQt6.QtWidgets import QTextBrowser

from src.TeaCOPER.GUI.QTextEditLogHandler import QTextEditLogHandler
from src.TeaCOPER.utils.ConfigUtil import ConfigUtil

CRITI = 50
ERROR = 40
WARN = 35
COMPE = 30
INFO = 20
DEBUG = 10

logging.addLevelName(CRITI, "CRITI")
logging.addLevelName(ERROR, "ERROR")
logging.addLevelName(WARN, "WARN")
logging.addLevelName(COMPE, "COMPE")
logging.addLevelName(INFO, "INFO")
logging.addLevelName(DEBUG, "DEBUG")


class MyLogger(logging.Logger):
    """
    自定义日志记录器
    """

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

    def criti(self, msg, *args, **kwargs):
        if self.isEnabledFor(CRITI):
            self._log(CRITI, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        if self.isEnabledFor(WARN):
            self._log(WARN, msg, args, **kwargs)

    def compe(self, msg, *args, **kwargs):
        if self.isEnabledFor(COMPE):
            self._log(COMPE, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(INFO):
            self._log(INFO, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg, args, **kwargs)


class TruncateColoredFormatter(colorlog.ColoredFormatter):
    def __init__(self, fmt=None, datefmt=None, style='%', log_colors=None,
                 secondary_log_colors=None, max_filename_length=12, keep_start=3, keep_end=3):
        super().__init__(fmt, datefmt, style, log_colors, secondary_log_colors)
        self.max_filename_length = max_filename_length
        self.keep_start = keep_start
        self.keep_end = keep_end

    def format(self, record):
        # 处理文件名截断
        if hasattr(record, 'filename') and record.filename:
            filename = record.filename

            if len(filename) > self.max_filename_length:
                name, ext = os.path.splitext(filename)
                available_length = self.max_filename_length - len(ext) - 4  # 4是".."的长度

                if len(name) > (self.keep_start + self.keep_end):
                    truncated_name = name[:self.keep_start] + '..' + name[-self.keep_end:]
                else:
                    truncated_name = name[:self.max_filename_length - len(ext)]

                record.filename = truncated_name + ext

        return super().format(record)


logging.setLoggerClass(MyLogger)


def getLogger(name, level=DEBUG, log_format=None):
    """
    获取自定义日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别，默认DEBUG
        log_format: 日志格式

    Returns:
        MyLogger : 我去
    """
    if log_format is None:
        log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        normal_handler = logging.StreamHandler()
        normal_formatter = TruncateColoredFormatter(
            fmt='[%(asctime)s] %(name)-6s > %(levelname)-5s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red'
            }
        )
        normal_handler.setFormatter(normal_formatter)
        normal_handler.setLevel(INFO)

        debug_handler = logging.FileHandler(
            f"{ConfigUtil.readConfigFile("log-config")["logname"]} {datetime.datetime.now().strftime('%Y-%m-%d')}.log",
            mode='a')
        debug_formatter = TruncateColoredFormatter(
            fmt='[%(asctime)s] <%(filename)-12s>/%(name)-6s > %(levelname)-5s | %(message)s'
        )
        debug_handler.setFormatter(debug_formatter)
        debug_handler.setLevel(DEBUG)

        logger.addHandler(normal_handler)
        logger.addHandler(debug_handler)

    return logger


class LogManager(QObject):
    log_updated = Signal(str, str)  # 日志消息 : 日志等级

    def __init__(self, name: str):
        super().__init__()
        self.logger = getLogger(name)
        self.gui_handler = None

    def add_gui_handler(self, text_edit):
        """添加GUI日志处理器"""
        if self.gui_handler is None:
            self.gui_handler = QTextEditLogHandler(text_edit)
            self.gui_handler.setLevel(logging.INFO)
            self.logger.addHandler(self.gui_handler)

    def remove_gui_handler(self):
        """移除GUI日志处理器"""
        if self.gui_handler:
            self.logger.removeHandler(self.gui_handler)
            self.gui_handler = None

    def criti(self, msg):
        self.logger.criti(msg)
        self.log_updated.emit(msg, "CRITI")

    def error(self, msg):
        self.logger.error(msg)
        self.log_updated.emit(msg, "ERROR")

    def warn(self, msg):
        self.logger.warn(msg)
        self.log_updated.emit(msg, "WARN")

    def compe(self, msg):
        self.logger.compe(msg)
        self.log_updated.emit(msg, "COMPE")

    def info(self, msg):
        self.logger.info(msg)
        self.log_updated.emit(msg, "INFO")

    def debug(self, msg):
        self.logger.debug(msg)
        self.log_updated.emit(msg, "DEBUG")
