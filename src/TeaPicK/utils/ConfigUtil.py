import configparser
import json
import os

from src.TeaCOPER.model.Course import CourseModel

class ConfigUtil:
    """
    [工具类]
    读取配置文件使用的工具类
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    @staticmethod
    def readConfigFile(configType : str):
        """
        读取配置文件中的内容并转换为字典
        但只返回某一
        :param configType:

        :return: configToDict
        """
        filePath = os.path.join(ConfigUtil.parent_dir, 'config', "config.toml")
        cfg = configparser.ConfigParser()
        cfg.read(filePath)
        return dict(cfg.items(configType))

    @staticmethod
    def readJsonCourseConfigFile(filePath : str):
        filePath = os.path.join(ConfigUtil.parent_dir, 'config', filePath)
        with open(filePath,'r',encoding='utf-8') as f:
            data = json.load(f)
            f.close()

        courses = data['course']
        courseList = []

        for course_key in courses:
            course = courses[course_key]
            temp = CourseModel(course["courseName"],course["courseNo"])
            courseList.append(temp)

        return courseList