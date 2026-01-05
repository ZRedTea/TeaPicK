from requests import Session

from src.TeaPicK.utils.ConfigUtil import ConfigUtil
from src.TeaPicK.utils.CourseIdUtil import CourseIdUtil

from src.TeaPicK.managers.LogManager import LogManager

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

        CourseIdUtil.getCourseJson(self.session)

        for course in courseList:
            id = CourseIdUtil.getCourseId(self.session, course)
            course.setCourseId(id)

        return courseList




