import requests
from requests import Session

from src.TeaCOPER.utils.ConfigUtil import ConfigUtil

class SessionUtil:
    """
    [工具类]
    操作session的工具类
    """
    @staticmethod
    def getSession():
        """
        获取一个session
        :return: session
        """
        return requests.Session()

    @staticmethod
    def initSession(session : Session):
        """
        初始化session
        :param session:

        :return: sessionAfterInit
        """
        url = ConfigUtil.readConfigFile("website")["loginurl"]
        headers = {
            "Connection" : ConfigUtil.readConfigFile("index-headers")["connection"],
            "Host" : "jwxt.sias.edu.cn",
            "Origin" : "https://jwxt.sias.edu.cn",
            "User-Agent" : ConfigUtil.readConfigFile("index-headers")["user-agent"],
            "Referer" : ConfigUtil.readConfigFile("index-headers")["referer"],
        }
        session.headers = headers
        # print(session.cookies)
        # response = requests.get(url)
        # print(response.cookies)
        response = session.get(url)
        session.cookies = response.cookies
        return session