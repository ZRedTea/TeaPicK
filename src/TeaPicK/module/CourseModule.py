from requests import Session

from TeaPicK.utils.ConfigUtil import ConfigUtil
from TeaPicK.utils.CourseIdUtil import CourseIdUtil

from TeaPicK.manager.LogManager import LogManager

class CourseModule:
    """
    [模块类]
    获取课程列表的模块类
    """
    def __init__(self, session : Session):
        self.logger = LogManager("课程代码模块")
        self.session = session


    def getCourseList(self):
        """
        获取course列表
        :return: course_list
        """

        courseList = ConfigUtil.readJsonCourseConfigFile("courseList.json")

        for course in courseList:
            id = CourseIdUtil.getCourseId(self.session, course)
            course.setCourseId(id)

        return courseList




