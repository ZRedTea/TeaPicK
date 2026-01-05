import configparser
import json
import os
import sys

from src.TeaPicK.models.CourseModel import CourseModel


class ConfigUtil:
    """
    [工具类]
    读取配置文件使用的工具类
    """

    @staticmethod
    def _get_config_dir():
        """获取配置文件目录，支持打包环境"""
        if getattr(sys, 'frozen', False):
            # 打包后的可执行文件
            # 配置文件在可执行文件同级的 config 目录
            base_dir = os.path.dirname(sys.executable)
            config_dir = os.path.join(base_dir, 'config')
        else:
            # 开发环境
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            config_dir = os.path.join(parent_dir, 'config')

        # 如果 config 目录不存在，则创建
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return config_dir

    @staticmethod
    def _get_config_path(filePath: str):
        """获取配置文件的完整路径"""
        config_dir = ConfigUtil._get_config_dir()
        return os.path.join(config_dir, filePath)

    @staticmethod
    def readConfigFile(filePath: str, configType: str):
        """
        读取配置文件中的内容并转换为字典
        :param filePath:
        :param configType:
        :return: configToDict
        """
        filePath = ConfigUtil._get_config_path(filePath)
        cfg = configparser.ConfigParser()
        cfg.read(filePath, encoding='utf-8')
        return dict(cfg.items(configType))

    @staticmethod
    def readListConfigFile(filePath: str, configType: str):
        """
        读取配置文件中的列表内容并转换为列表
        :param filePath:
        :param configType:
        :return: configToList
        """
        filePath = ConfigUtil._get_config_path(filePath)
        cfg = configparser.ConfigParser()
        cfg.read(filePath, encoding='utf-8')
        configDict = dict(cfg.items(configType))
        return [item.strip() for item in configDict.values()]

    @staticmethod
    def readJsonCourseConfigFile(filePath: str):
        filePath = ConfigUtil._get_config_path(filePath)
        with open(filePath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        courses = data['course']
        courseList = []

        for course_key in courses:
            course = courses[course_key]
            temp = CourseModel(course["courseName"], course["courseNo"])
            courseList.append(temp)

        return courseList

    @staticmethod
    def check_and_create_default_configs():
        """检查并创建默认配置文件"""
        config_dir = ConfigUtil._get_config_dir()

        # 默认配置文件内容
        default_configs = {
            'LogConfig.ini': """[log-config]
LogName = DebugLog
""",
            'sessionConfig.ini': """[index-headers]
Connection = keep-alive
User-Agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36
Referer = https://jwxt.sias.edu.cn/eams/loginExt.action
""",
            'websiteConfig.ini': """[website]
loginURL=https://jwxt.sias.edu.cn/eams/loginExt.action
courseDataURL=https://jwxt.sias.edu.cn/eams/stdElectCourse!data.action
courseSelectURL=https://jwxt.sias.edu.cn/eams/stdElectCourse!batchOperator.action

; 需要改为自己的profileId
profile=
""",
            'courseList.json': """{
    "course": {
        "course1": {
            "courseName": "嵌入式系统与应用",
            "courseNo": "25262.28120190-3.09"
        },
        "course2": {
            "courseName": "你的课程名",
            "courseNo": "课程代码"
        }
    }
}
"""
        }

        # 检查并创建配置文件
        for filename, content in default_configs.items():
            file_path = os.path.join(config_dir, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"已创建默认配置文件: {filename}")
