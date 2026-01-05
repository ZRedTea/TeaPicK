import hashlib

from requests import Session
from src.TeaPicK.utils.ConfigUtil import ConfigUtil

from src.TeaPicK.managers.LogManager import LogManager

from src.TeaPicK.handlers.LoginHandler import LoginHandler

class LoginModule:
    """
    [模块类]
    实现模拟登录的模块类
    """
    def __init__(self):
        self.logger = LogManager("登录模块")
        self.session = Session
        self.url = ConfigUtil.readConfigFile("websiteConfig.ini", "website")["loginurl"]

        self.loginHandler = LoginHandler(self.url)

    def login(self):
        """
        实现模拟登录的方法
        :return: session
        """
        self.logger.info("正在准备模拟登录")
        self.logger.info("正在调用登录处理器")

        self.session = self.loginHandler.run()

        self.logger.info("模拟登录完成")
        return self.session