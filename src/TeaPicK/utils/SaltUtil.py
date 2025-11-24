import logging
import os

import requests
from bs4 import BeautifulSoup
from requests import Session

from src.TeaCOPER.manager.LogManager import LogManager

logger = LogManager("工具组件")

class SaltUtil:
    @staticmethod
    def getUUIDFromFile(filename : str):
        try:
            logger.info(f"正在准备从文件获取uuid")
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) < 12:
                    logger.error(f"文件内容错误 : 未找到12行")
                    return None
                line_12 = lines[11].strip()
                logger.info(f"成功获取到第12行内容")
                f.close()

            starter_marker = "SHA1('"
            end_marker = "' + form"

            start_index = line_12.find(starter_marker)
            if start_index == -1:
                logger.error(f"文件内容错误 : 起始标记异常")
                return None
            start_index = start_index + len(starter_marker)

            end_index = line_12.find(end_marker)
            if end_index == -1 or end_index <= start_index:
                logger.error(f"文件内容错误 : 末尾标记异常")
                return None

            logger.info(f"已成功获取起始标记和末尾标记")
            target_string = line_12[start_index:end_index]
            #os.remove(filename)
            return target_string

        except FileNotFoundError:
            logger.error(f"未找到文件")
            return None
        except Exception as e:
            logger.error(f"发生未知错误: {e}")
            return None

    @staticmethod
    def saveScriptFromResponse(html_content, filename : str):
        try:
            logger.info(f"正在准备保存响应中的script内容")
            soup = BeautifulSoup(html_content, 'html.parser')

            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'CryptoJS.SHA1' in script.string:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(script.string)
                        logger.info(f"已成功写入文件")
                        f.close()
                    return True

        except Exception as e:
            logger.error(f"发生未知错误: {e}")
            return None

    @staticmethod
    def getSalt(session : Session, url : str):
        logger.info(f"正在获取salt")
        response = session.get(url)
        SaltUtil.saveScriptFromResponse(response.text, "get.txt")
        salt = SaltUtil.getUUIDFromFile("get.txt")
        logger.info(f"已获取到salt")
        return salt