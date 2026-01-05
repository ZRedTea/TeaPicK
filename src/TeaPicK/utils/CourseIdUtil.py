from requests import Session
import os
import json
import re

from src.TeaPicK.utils.ConfigUtil import ConfigUtil

from src.TeaPicK.models.CourseModel import CourseModel

class CourseIdUtil:

    # AI太好用了你们知道吗 正则表达式太好用了你们知道吗
    @staticmethod
    def find_id_by_no(data_string, target_no):
        """
        从类似JSON的字符串中根据no字段查找对应的id值

        Args:
            data_string: 包含多个对象的字符串
            target_no: 要查找的no值，如 '25262.02120004-1.05'

        Returns:
            str: 找到的id值，如果没找到返回None
        """
        # 方法1：使用正则表达式直接匹配
        # 匹配模式：id:数字,no:'目标编号'
        pattern = r"id:(\d+),no:'" + re.escape(target_no) + r"'"
        match = re.search(pattern, data_string)

        if match:
            return match.group(1)

        # 方法2：如果方法1没找到，尝试更灵活的匹配
        # 匹配模式：id:数字,no:'任意字符'，然后检查no是否匹配目标
        pattern2 = r"id:(\d+),no:'([^']+)'"
        matches = re.findall(pattern2, data_string)

        for id_val, no_val in matches:
            if no_val == target_no:
                return id_val

        return None

    @staticmethod
    def getCourseJson(session : Session):
        url = ConfigUtil.readConfigFile("websiteConfig.ini", "website")["coursedataurl"]
        profileId = ConfigUtil.readConfigFile("websiteConfig.ini", "website")["profile"]

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

        with open(f"course_data.action", "r", encoding="utf-8") as f:
            courseData = f.read()

        id = CourseIdUtil.find_id_by_no(courseData, courseNo)

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