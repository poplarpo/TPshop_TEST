# 导包
import unittest
import time
from page.page_cart import PageCart
from page.page_login import PageLogin
import page



class TestCart(unittest.TestCase):
    cart = None
    login = None

    @classmethod
    def setUpClass(cls):
        # 1. 登录
        cls.login = PageLogin()
        cls.login.page_click_login_link()
        cls.login.page_login('13800001111', '123456', code='8888')
        time.sleep(2)

        # 2. 复用driver,满足查看购物车的前提是登录成功
        cls.cart = PageCart()
        cls.cart.driver = cls.login.driver

        # 直接访问购物车页面
        cls.cart.driver.get("http://localhost/Home/Cart/index.html")
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.cart.driver.quit()

    def test_cart_add_num(self):
        # 获取增加前数量
        before_num = self.cart.page_num()
        print("增加前数量：", before_num)

        # 点击增加
        self.cart.page_click_add()
        time.sleep(1)

        # 获取增加后数量
        after_num = self.cart.page_num()
        print("增加后数量：", after_num)

        # 断言
        self.assertEqual(after_num, before_num + 1, "数量增加失败")

    def test_all_delete(self):
        if(page.cart_select_all):
            self.cart.base_click(page.cart_delete_all)
            print('删完了')
        else:
            self.cart.base_click(page.cart_select_all)
            self.cart.base_click(page.cart_delete_all)
            print('不该删的也删完了')

