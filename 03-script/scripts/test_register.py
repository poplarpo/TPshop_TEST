# 导包
import unittest
from page.page_register import PageRegister
from parameterized import parameterized


def get_data():
    return [("138", "8888", "123456",'123456',"请用手机号或邮箱注册"),
            ("13800001111", "8888", "123456",'654321','两次输入密码不一致')]


# 新建测试类 并 继承
class TestRegister(unittest.TestCase):
    register = None
    # setUp

    @classmethod
    def setUpClass(cls):
        # 实例化 获取页面对象
        cls.register = PageRegister()
        # 点击注册
        cls.register.page_click_register_link()

    # tearDown
    @classmethod
    def tearDownClass(cls):
        # 关闭 driver驱动对象
        cls.register.driver.quit()

    # 注册测试方法
    @parameterized.expand(get_data())
    def test_register(self,phonenum, code, pwd,pwd2, expect_result):
        # 调用注册方法
        self.register.page_register(phonenum,code,pwd,pwd2,)

        # 获取注册提示信息
        msg = self.register.page_get_error_info()
        try:
            # 断言
            self.assertEqual(msg, expect_result)
        except AssertionError:
            # 截图
            self.register.page_get_img()
        #处理提示框
        self.register.page_click_err_btn_ok()