import time

from src.TeaPicK.utils.SessionUtil import SessionUtil

from modules.SelectModule import SelectModule
from modules.LoginModule import LoginModule
from modules.CourseModule import CourseModule

from managers.LogManager import LogManager

def run():
    logger = LogManager("中央控件")

    LoginModuleObject = LoginModule()
    session = LoginModuleObject.login()

    CourseModuleObject = CourseModule(session)
    courseList = CourseModuleObject.getCourseList()

    userInput = float(input("请输入一个抢课间隔(若输入过大则自动归位0.5s):"))
    SelectModuleObject = SelectModule(session, courseList, max(0.5,userInput))
    SelectModuleObject.selectStart()

if __name__ == '__main__':
    run()