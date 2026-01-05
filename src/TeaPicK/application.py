import time

from src.TeaPicK.utils.SessionUtil import SessionUtil

from modules.SelectModule import SelectModule
from modules.LoginModule import LoginModule
from modules.CourseModule import CourseModule

from managers.LogManager import LogManager
from utils.ConfigUtil import ConfigUtil

def run():
    logger = LogManager("中央控件")

    logger.info("正在准备模拟登录")
    userInput = input("请选择使用Chrome或是Edge(输入1选择Chrome, 2选择Edge):")
    if userInput == "1":
        browser_type = "chrome"
    else:
        browser_type = "edge"
    LoginModuleObject = LoginModule(browser_type)
    session = LoginModuleObject.login()
    logger.info("模拟登录完成")

    logger.info("正在准备获取课程序号")
    CourseModuleObject = CourseModule(session)
    courseList = CourseModuleObject.getCourseList()
    logger.info("课程序号获取完成")

    userInput = float(input("请输入一个抢课间隔(若输入过小则默认为0.5s):"))
    SelectModuleObject = SelectModule(session, courseList, max(0.5,userInput))
    SelectModuleObject.selectStart()

if __name__ == '__main__':
    ConfigUtil.check_and_create_default_configs()
    run()