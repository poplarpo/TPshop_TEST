# 导包
import unittest
import time
from page.page_login import PageLogin
from page.page_detail import PageDetail
import page



class TestDetail(unittest.TestCase):
    detail = None
    login = None

    @classmethod
    def setUpClass(cls):
        # 1. 登录
        cls.login = PageLogin()
        cls.login.page_click_login_link()
        cls.login.page_login('13800001111', '123456', code='8888')
        time.sleep(2)

        # 2. 复用driver
        cls.detail = PageDetail()
        cls.detail.driver = cls.login.driver

        # 直接访问商品详情页
        cls.detail.driver.get("http://localhost/Home/Goods/goodsInfo/id/65.html")
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.detail.driver.quit()

    #测试当详情商品数量为1时是否能再减少数量
    def test_detail_mins_num(self):
        before_num = self.detail.page_detail_num()
        print("初始数量：", before_num)
        if(before_num>1):
            #让数量等于1
            el = self.detail.base_find_element(page.detail_num)
            el.clear()
            el.send_keys('1')
        #点击减号
        self.detail.page_less_num()
        after_num = self.detail.page_detail_num()
        print("减少后：", after_num)

        # 断言
        self.assertEqual(after_num, before_num, "有问题")

    # 测试当成功添加数量
    def test_detail_add_num(self):
        # 获取增加前数量
        num1 = self.detail.page_detail_num()
        print("增加前：", num1)

        # 点击增加
        self.detail.page_detail_addnum()
        time.sleep(1)

        # 获取增加后数量
        num2 = self.detail.page_detail_num()
        print("增加后：", num2)

        # 断言
        self.assertEqual(num2, num1 + 1, "数量增加失败")

    #测试添加购物车成功
    def test_detail_addcart_ok(self):
        #点击添加购物车
        self.detail.page_detail_click_cart()
        #切换到iframe里面
        self.detail.switch_to_addcart_iframe()
        info = self.detail.page_detail_info()
        # 断言
        self.assertEqual("添加成功", info, "添加购物车成功哦")

        #切回主页面
        self.detail.switch_to_default()