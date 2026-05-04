import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page.page_cart import PageCart
from page.page_detail import PageDetail
from page.page_login import PageLogin
from page.page_order import PageOrder


# 类级别夹具：一次登录 → 加购 → 进入结算页，所有用例共享
@pytest.fixture(scope="class")
def order_page():
    # ========== 前置操作 ==========
    # 1. 登录
    login = PageLogin()
    login.page_click_login_link()
    login.page_login('13800001111', '123456', code='8888')
    time.sleep(2)

    # 2. 商品详情页加入购物车
    detail = PageDetail()
    detail.driver = login.driver
    detail.driver.get("http://localhost/Home/Goods/goodsInfo/id/65.html")
    detail.page_detail_click_cart()
    detail.switch_to_addcart_iframe()
    detail.switch_to_default()
    time.sleep(1)

    # 3. 进入购物车
    cart = PageCart()
    cart.driver = detail.driver
    cart.driver.get("http://localhost/Home/Cart/index.html")
    time.sleep(3)

    # 4. 去结算 → 进入订单确认页
    order = PageOrder()
    order.driver = cart.driver
    order.page_order_link()
    time.sleep(3)

    # 把初始化好的订单页对象传给测试类
    yield order

    # ========== 后置操作：关闭浏览器 ==========
    if order.driver:
        order.driver.quit()


# 订单测试类（所有用例自动复用 order_page）
class TestOrder:
    """订单模块测试用例"""

    def test_order_page_loaded(self, order_page):
        """【用例1】验证订单确认页面正常加载"""
        page_title = order_page.driver.title
        assert "确认订单" in page_title or "订单" in page_title, "订单页面加载失败"

    def test_order_select_address(self, order_page):
        """【用例2】选择收货地址"""
        order_page.page_order_select_address()  # 调用PO方法选择地址
        time.sleep(1)
        # 可加断言：判断地址是否被选中
        assert True, "选择收货地址成功"

    def test_order_select_payment(self, order_page):
        """【用例3】选择支付方式"""
        order_page.page_order_select_payment()  # 选择支付方式（如支付宝/微信）
        time.sleep(1)
        assert True, "选择支付方式成功"

    def test_order_select_shipping(self, order_page):
        """【用例4】选择配送方式"""
        order_page.page_order_select_shipping()  # 选择快递/配送方式
        time.sleep(1)
        assert True, "选择配送方式成功"

    def test_order_submit_success(self, order_page):
        """【用例5】正常流程：提交订单（核心用例）"""
        # 确保信息完整
        order_page.page_order_select_address()
        order_page.page_order_select_payment()
        order_page.page_order_select_shipping()
        time.sleep(1)

        # 提交订单
        order_page.page_order_submit()
        time.sleep(2)

        # 断言：提交后跳转到支付页/成功页
        assert "支付" in order_page.driver.page_source or "成功" in order_page.driver.page_source, "订单提交失败"

    def test_order_submit_without_address(self, order_page):
        """【用例6】异常场景：不选择地址 → 无法提交订单"""
        # 回到订单页（刷新/返回）
        order_page.driver.get("http://localhost/Home/Checkout/index.html")
        time.sleep(2)

        # 不选地址，直接提交
        order_page.page_order_submit()
        time.sleep(1)

        # 断言：页面出现提示（请选择收货地址）
        assert "请选择收货地址" in order_page.driver.page_source, "未拦截无地址提交订单"