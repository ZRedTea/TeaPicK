import time

from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import json

from src.TeaPicK.managers.LogManager import LogManager

class LoginHandler:
    def __init__(self, login_url):
        self.logger = LogManager("登录处理")
        self.login_url = login_url
        self.driver = None
        self.session = None

    def setup_driver(self):
        """设置Chrome浏览器驱动"""
        options = webdriver.ChromeOptions()

        # 添加一些常用选项
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # 使用webdriver-manager自动管理驱动
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        # 修改webdriver属性，避免被检测
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def wait_for_login(self, timeout=300):
        """
        等待用户手动登录

        Args:
            timeout: 超时时间（秒），默认5分钟

        Returns:
            bool: 是否成功等待用户登录
        """

        self.logger.info("请在打开的网页中登录网站")
        self.logger.info("脚本会自动捕捉你的COOKIES")
        self.logger.info("登录后请打开一次选课界面")

        try:
            # 等待页面加载完成
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # 获取当前URL，用于判断是否已跳转
            initial_url = self.driver.current_url

            # 等待URL发生变化（表示登录成功跳转）
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url != initial_url
            )

            print("检测到页面跳转，登录可能已完成！")
            return True

        except Exception as e:
            print(f"等待登录超时或出错: {e}")
            return False

    def export_session(self):
        """
        将浏览器cookies导出为requests.Session对象

        Returns:
            requests.Session: 包含登录会话的requests Session对象
        """
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用setup_driver()")

        # 创建新的requests Session
        self.session = requests.Session()

        # 获取浏览器中的所有cookies
        selenium_cookies = self.driver.get_cookies()
        print(selenium_cookies)

        jar = RequestsCookieJar()
        for cookie in selenium_cookies:
            jar.set(cookie["name"], cookie["value"])
        self.session.cookies = jar
        print(self.session.cookies)

        print(f"成功导出 {len(selenium_cookies)} 个cookies到requests Session")
        return self.session

    def run(self, timeout=300):
        """
        运行完整的登录和导出流程

        Args:
            timeout: 等待登录的超时时间（秒）

        Returns:
            requests.Session: 导出的Session对象，失败时返回None
        """
        try:
            # 1. 设置浏览器驱动
            self.logger.info("正在设置浏览器驱动...")
            self.setup_driver()

            # 2. 打开登录页面
            self.logger.info(f"正在打开登录页面: {self.login_url}")
            self.driver.get(self.login_url)

            # 3. 等待用户手动登录
            if not self.wait_for_login(timeout):
                print("等待登录超时，程序退出")
                return None

            # 4. 导出Session
            self.logger.info("正在导出Session...")
            session = self.export_session()

            return session

        except Exception as e:
            print(f"运行过程中出错: {e}")
            return None
        finally:
            # 询问用户是否关闭浏览器
            if self.driver:
                keep_open = input("\n是否保持浏览器窗口打开？(y/n): ").lower()
                if keep_open != 'y':
                    self.driver.quit()
                    self.logger.info("浏览器已关闭")

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("浏览器已关闭")

