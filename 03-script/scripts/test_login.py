# 导包
import pytest
from page.page_login import PageLogin

# ====================== 测试用例数据（扩充后） ======================
test_login_data = [
    # 格式：(username, pwd, code, expect_result)
    # 1. 正向用例：登录成功
    ("13800001111", "123456", "8888", "登录成功"),

    # 2. 反向用例：账号不存在
    ("13822223333", "123456", "8888", "账号不存在!"),

    # 3. 反向用例：密码错误
    ("13800001111", "123123", "8888", "密码错误"),

    # 4. 反向用例：账号为空
    ("", "123456", "8888", "用户名不能为空!"),

    # 5. 反向用例：密码为空
    ("13800001111", "", "8888", "密码不能为空!"),

    # 6. 反向用例：验证码为空
    ("13800001111", "123456", "", "验证码不能为空!"),

    # 7. 反向用例：验证码错误
    ("13800001111", "123456", "6666", "验证码错误"),

    # 8. 反向用例：手机号格式错误（非11位）
    ("1380000", "123456", "8888", "账号格式不匹配!"),

    # 9. 反向用例：密码长度过短
    ("13800001111", "123", "8888", "密码错误"),
]

# ====================== pytest 固件 ======================
@pytest.fixture(scope="class")
def login_page():
    # 前置：实例化登录页 + 打开登录界面
    login = PageLogin()
    login.page_click_login_link()
    yield login  # 提供给测试用例使用
    # 后置：关闭浏览器
    login.driver.quit()

# ====================== 测试用例 ======================
@pytest.mark.parametrize("username, pwd, code, expect_result", test_login_data)
def test_login(login_page, username, pwd, code, expect_result):
    """
    登录功能综合测试
    """
    # 1. 执行登录操作
    login_page.page_login(username, pwd, code)

    # 2. 获取页面提示信息
    actual_msg = login_page.page_get_error_info()

    try:
        # 3. 断言预期结果
        assert actual_msg == expect_result
    except AssertionError:
        # 4. 失败自动截图
        login_page.page_get_img()
        raise
    finally:
        # 5. 关闭提示框，不影响下一条用例
        login_page.page_click_err_btn_ok()

# 执行测试
if __name__ == "__main__":
    pytest.main(["-v", "-s", "test_login.py"])