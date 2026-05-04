import pytest
from page.page_register import PageRegister


# 测试数据
def get_register_data():
    return [
        ("138", "8888", "123456", "123456", "请用手机号或邮箱注册"),
        ("13800001111", "8888", "123456", "654321", "两次输入密码不一致"),
        ("", "8888", "123456", "123456", "手机号不能为空"),
        ("13800001111", "", "123456", "123456", "验证码不能为空"),
        ("13800001111", "8888", "", "", "密码不能为空"),
        ("13800001111", "8888", "123", "123", "密码长度不能少于6位"),
        ("13800001111", "8888", "111111", "111111", "密码过于简单，请重新输入"),
        ("138123", "8888", "123456", "123456", "请输入有效的手机号码"),
        ("13800001111", "8888", "123456", "", "请确认密码"),
        ("13800002222", "8888", "Abc123456", "Abc123456", "注册成功"),
    ]


@pytest.fixture(scope="module", autouse=True)
def reg():
    obj = PageRegister()
    obj.page_click_register_link()
    yield obj
    obj.driver.quit()


class TestRegister:
    @pytest.mark.parametrize("phone, code, pwd, pwd2, expect", get_register_data())
    def test_register(self, reg, phone, code, pwd, pwd2, expect):
        # 刷新页面
        reg.driver.refresh()

        # 等待输入框加载
        reg.base_wait(reg.page_input_phonenum)

        # 输入数据
        reg.page_input_phonenum(phone)
        reg.page_input_verify_code(code)
        reg.page_input_password(pwd)
        reg.page_input_pwd2(pwd2)

        # 勾选协议（避免重复点击）
        try:
            if not reg.base_find_element(reg.page_click_protocol).is_selected():
                reg.page_click_protocol()
        except:
            pass

        # 点击注册
        reg.page_click_agree()

        # 获取提示信息
        try:
            reg.base_wait(reg.page_get_error_info, timeout=3)
            msg = reg.page_get_error_info().strip()
            reg.page_click_err_btn_ok()
        except:
            msg = "注册成功"

        # 断言
        print(f"预期：{expect}，实际：{msg}")
        assert msg == expect