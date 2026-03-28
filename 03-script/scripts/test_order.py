import time
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from page.page_cart import PageCart
from page.page_detail import PageDetail
from page.page_login import PageLogin
from page.page_order import PageOrder


class TestOrder(unittest.TestCase):
    login = None
    cart = None
    order = None

    @classmethod
    def setUpClass(cls):
        # 1. 先要登录成功
        cls.login = PageLogin()
        cls.login.page_click_login_link()
        cls.login.page_login('13800001111', '123456', code='8888')
        time.sleep(2)

        #2.先去详情页加入购物车

        cls.detail = PageDetail()
        cls.detail.driver = cls.login.driver

        # 直接访问商品详情页
        cls.detail.driver.get("http://localhost/Home/Goods/goodsInfo/id/65.html")

        cls.detail.page_detail_click_cart()
        # 切换到iframe里面
        cls.detail.switch_to_addcart_iframe()

        # 切回主页面
        cls.detail.switch_to_default()

        # 3.再跳转去购物车
        cls.cart = PageCart()
        cls.cart.driver = cls.detail.driver

        # 直接访问购物车页面
        cls.cart.driver.get("http://localhost/Home/Cart/index.html")
        time.sleep(3)

        # 等待购物车页面加载完成
        wait = WebDriverWait(cls.cart.driver, 10)
        wait.until(lambda x: x.execute_script("return document.readyState") == "complete")

        # 滚动到页面底部，确保按钮可见
        cls.cart.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        cls.cart.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # 3. 创建订单页面对象并点击去结算
        cls.order = PageOrder()
        cls.order.driver = cls.cart.driver

        cls.order.page_order_link()  # 点击去结算
        time.sleep(3)


    @classmethod
    def tearDownClass(cls):
        if cls.order and cls.order.driver:
            cls.order.driver.quit()

    def test_submit_order(self):
        self.order.page_order_submit()