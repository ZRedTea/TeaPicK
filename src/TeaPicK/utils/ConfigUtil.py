import configparser
import json
import os

from src.TeaPicK.models.CourseModel import CourseModel

class ConfigUtil:
    """
    [工具类]
    读取配置文件使用的工具类
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    @staticmethod
    def readConfigFile(filePath : str, configType : str):
        """
        读取配置文件中的内容并转换为字典
        :param filePath:
        :param configType:

        :return: configToDict
        """
        filePath = os.path.join(ConfigUtil.parent_dir, 'config', filePath)
        # print(filePath)
        cfg = configparser.ConfigParser()
        cfg.read(filePath,encoding='utf-8')
        # print(cfg.items(configType))
        # print(dict(cfg.items(configType)))
        return dict(cfg.items(configType))

    @staticmethod
    def readListConfigFile(filePath : str, configType : str):
        """
        读取配置文件中的列表内容并转换为列表
        :param filePath:
        :param configType:

        :return: configToList
        """
        filePath = os.path.join(ConfigUtil.parent_dir, 'config', filePath)
        cfg = configparser.ConfigParser()
        cfg.read(filePath,encoding='utf-8')
        configDict = dict(cfg.items(configType))
        return [item.strip() for item in configDict.values()]

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