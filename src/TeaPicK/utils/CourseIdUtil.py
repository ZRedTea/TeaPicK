import requests
from requests import Session
import os
import json
import re

from src.TeaCOPER.utils.ConfigUtil import ConfigUtil

from src.TeaCOPER.model.Course import CourseModel

class CourseIdUtil:
    @staticmethod
    def findCourseId(filename, search_text):
        """
        在文件中搜索文本，找到时返回上一行的内容
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                previous_line = None
                current_line = None

                for line in file:
                    current_line = line.strip()

                    if search_text in current_line:
                        if previous_line is not None:
                            match = re.search(r'(\d+)', previous_line)
                            if match:
                                return match.group(1)
                            return None
                        else:
                            return "这是第一行，没有上一行"

                    previous_line = current_line

                return f"未找到包含 '{search_text}' 的行"

        except FileNotFoundError:
            return f"文件不存在: {filename}"
        except Exception as e:
            return f"读取文件时出错: {e}"



        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            print(f"其他错误: {e}")
            return None

    @staticmethod
    def getCourseJson(session : Session):
        url = ConfigUtil.readConfigFile("website")["coursedataurl"]
        profileId = ConfigUtil.readConfigFile("website")["profile"]
        url = url + profileId

        ThisSession = session
        ThisSession.headers['Referer'] = url

        params = {
            "profileId": profileId,
        }
        print (url)
        response = ThisSession.get(url, params=params)
        with open("course_data.action", "w", encoding="utf-8") as f:
            f.write(response.text)
            f.close()

    @staticmethod
    def getCourseId(session : Session, course : CourseModel):
        courseNo = course.getCourseNo()

        if not os.path.exists("course_data.action"):
            # courseIdUtil.getCourseJson(session)
            print("未找到文件")
            raise Exception("未找到文件")

        id = CourseIdUtil.findCourseId("course_data.action", courseNo)
        return id


















    # @staticmethod
    # def parse_javascript_json(response_text):
    #     """
    #     从JavaScript变量声明中提取JSON数据
    #     """
    #     try:
    #         # 使用正则表达式提取JSON数组部分
    #         # 匹配 var lessonJSONs = [{...}]; 模式
    #         pattern = r'var lessonJSONs\s*=\s*(\[.*?\]);'
    #         match = re.search(pattern, response_text, re.DOTALL)
    #
    #         if match:
    #             json_str = match.group(1)
    #             # 解析JSON
    #             data = json.loads(json_str)
    #             return data
    #         else:
    #             print("未找到 lessonJSONs 变量定义")
    #             return None