# 导包
import pytest
import time

from selenium.webdriver.common.by import By

from page.page_cart import PageCart
from page.page_login import PageLogin
import page
from selenium.common.exceptions import NoSuchElementException

# 定义全局的 cart 和 login 实例
cart = None
login = None


# 模块级初始化（所有用例执行前执行一次）
@pytest.fixture(scope="module", autouse=True)
def setup_module():
    global cart, login
    # 1. 登录
    login = PageLogin()
    login.page_click_login_link()
    login.page_login('13800001111', '123456', code='8888')
    time.sleep(2)

    # 2. 复用driver，满足查看购物车的前提是登录成功
    cart = PageCart()
    cart.driver = login.driver

    # 直接访问购物车页面
    cart.driver.get("http://localhost/Home/Cart/index.html")
    time.sleep(2)

    # 用例执行完后清理
    yield
    cart.driver.quit()


# 新增：重置商品数量为1（每条用例执行前执行，保证用例独立性）
@pytest.fixture(scope="function", autouse=True)
def setup_function():
    # 获取当前数量，重置为1
    current_num = cart.page_num()
    if current_num > 1:
        for _ in range(current_num - 1):
            cart.page_click_less()
            time.sleep(0.5)
    elif current_num < 1:
        cart.page_click_add()
        time.sleep(0.5)
    yield


# 原用例：商品数量增加
def test_cart_add_num():
    # 获取增加前数量
    before_num = cart.page_num()
    print(f"增加前数量：{before_num}")

    # 点击增加
    cart.page_click_add()
    time.sleep(1)

    # 获取增加后数量
    after_num = cart.page_num()
    print(f"增加后数量：{after_num}")

    # 断言
    assert after_num == before_num + 1, "数量增加失败"


# 新增用例：商品数量减少
def test_cart_less_num():
    # 先点击增加，保证数量>1
    cart.page_click_add()
    time.sleep(0.5)
    before_num = cart.page_num()
    print(f"减少前数量：{before_num}")

    # 点击减少
    cart.page_click_less()
    time.sleep(1)

    # 获取减少后数量
    after_num = cart.page_num()
    print(f"减少后数量：{after_num}")

    # 断言
    assert after_num == before_num - 1, "数量减少失败"


# 新增用例：数量不能小于1
def test_cart_num_not_less_than_1():
    # 连续点击减少（即使当前是1，也点击多次）
    for _ in range(3):
        cart.page_click_less()
        time.sleep(0.5)

    # 获取最终数量
    final_num = cart.page_num()

    # 断言数量≥1
    assert final_num >= 1, "商品数量小于1，不符合预期"


# 原用例改造：全选并删除所有商品
def test_cart_all_delete():
    # 先判断全选状态
    try:
        is_selected = cart.page_select_all()
    except NoSuchElementException:
        # 兼容元素未找到的情况
        cart.base_click(page.cart_select_all)
        is_selected = cart.page_select_all()

    if is_selected:
        cart.base_click(page.cart_delete_all)
        print('已选中全选框，执行删除')
    else:
        cart.base_click(page.cart_select_all)
        time.sleep(0.5)
        cart.base_click(page.cart_delete_all)
        print('未选中全选框，选中后删除')

    # 断言：购物车为空（需根据实际页面元素调整，示例用“无商品”文本判断）
    try:
        empty_text = cart.base_get_text((By.XPATH, "//div[text()='购物车为空']"))
        assert empty_text == "购物车为空", "删除后购物车仍有商品"
    except NoSuchElementException:
        pytest.fail("未找到购物车为空的提示，删除失败")


# 新增用例：点击去结算按钮跳转
def test_cart_go_to_checkout():
    # 先确保有商品（重置后数量为1）
    cart.base_click(page.cart_selected)  # 选中当前商品
    time.sleep(0.5)

    # 点击去结算
    cart.page_cart_order()
    time.sleep(2)

    # 断言：跳转到结算页（根据实际URL/元素判断）
    current_url = cart.driver.current_url
    assert "checkout" in current_url or "order" in current_url, "未跳转到结算页面"


# 新增用例：取消全选状态
def test_cart_cancel_select_all():
    # 先选中全选
    cart.base_click(page.cart_select_all)
    time.sleep(0.5)
    assert cart.page_select_all() is True, "全选框未选中"

    # 取消全选
    cart.base_click(page.cart_select_all)
    time.sleep(0.5)

    # 断言：全选框未选中
    assert cart.page_select_all() is False, "全选框未取消选中"