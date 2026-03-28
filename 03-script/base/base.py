from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Base:
    # 初始化
    def __init__(self):
        # self.driver = driver
        # 临时代替driver
        chrome_driver_path = r"D:\driver\chromedriver.exe"  # 修改为实际路径
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("http://localhost")


    # 查找元素方法 (提供：点击、输入、获取文本)使用
    def base_find_element(self, loc, timeout=30, poll=0.5):
        return WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll).until(lambda x: x.find_element(*loc))

    # 点击方法
    def base_click(self, loc):
        self.base_find_element(loc).click()

    # 输入方法
    def base_input(self, loc, value):
        el = self.base_find_element(loc)
        # 清空
        el.clear()
        # 输入
        el.send_keys(value)


    # 获取文本方法
    def base_get_text(self, loc):
        # 注意：一定要返回元素的文本信息
        return self.base_find_element(loc).text

    # 截图方法
    def base_get_image(self):
        self.driver.get_screenshot_as_file("../iamge/fail.png")


    def base_wait(self, loc, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(loc)
        )
