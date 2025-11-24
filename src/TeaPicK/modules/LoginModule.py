import hashlib
import logging

from requests import Session
from src.TeaCOPER.utils.SaltUtil import SaltUtil
from src.TeaCOPER.utils.ConfigUtil import ConfigUtil

from src.TeaCOPER.manager.LogManager import LogManager

class LoginModule:
    """
    [模块类]
    实现模拟登录的模块类
    """
    def __init__(self, session : Session):
        self.logger = LogManager("登录模块")
        self.session = session
        self.url = ConfigUtil.readConfigFile("website")["loginurl"]
        self.__username = ConfigUtil.readConfigFile("user")["username"],
        self.__password = ConfigUtil.readConfigFile("user")["password"]

        self.params = {
            "username" : self.__username,
            "password" : hashlib.sha1((SaltUtil.getSalt(self.session,self.url)+self.__password).encode()).hexdigest(),
            "session_locale" : "zh_CN",
        }

    def login(self):
        """
        实现模拟登录的方法
        :return: responseWhenLogin
        """
        self.logger.info("正在准备模拟登录")
        self.logger.info("正在调用saltUtil")

        response = self.session.post(self.url,params = self.params)

        self.logger.info("模拟登录完成")
        return response