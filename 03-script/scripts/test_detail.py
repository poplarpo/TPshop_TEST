import pytest
import time
from page.page_login import PageLogin
from page.page_detail import PageDetail
import page

# 类级别的初始化固件（整个测试类只执行一次登录+打开页面）
@pytest.fixture(scope="class")
def init_detail():
    # 登录
    login = PageLogin()
    login.page_click_login_link()
    login.page_login('13800001111', '123456', code='8888')
    time.sleep(2)

    # 打开商品详情页
    detail = PageDetail()
    detail.driver = login.driver
    detail.driver.get("http://localhost/Home/Goods/goodsInfo/id/65.html")
    time.sleep(2)

    yield detail  # 传递给测试用例

    # 退出清理
    detail.driver.quit()

# 每次用例执行前重置数量为 1（方法级固件，保证用例独立性）
@pytest.fixture(scope="function")
def reset_num(init_detail):
    detail = init_detail
    el = detail.base_find_element(page.detail_num)
    el.clear()
    el.send_keys("1")
    time.sleep(0.5)
    return detail

# ====================== 测试类 ======================
class TestDetail:
    # ====================== 原有用例 ======================
    def test_detail_mins_num(self, reset_num):
        detail = reset_num
        before_num = detail.page_detail_num()
        detail.page_less_num()
        after_num = detail.page_detail_num()
        assert after_num == before_num, "商品数量=1时点击减号，数量不应变化"

    def test_detail_add_num(self, reset_num):
        detail = reset_num
        num1 = detail.page_detail_num()
        detail.page_detail_addnum()
        num2 = detail.page_detail_num()
        assert num2 == num1 + 1, "商品数量增加失败"

    def test_detail_addcart_ok(self, reset_num):
        detail = reset_num
        detail.page_detail_click_cart()
        detail.switch_to_addcart_iframe()
        info = detail.page_detail_info()
        assert "添加成功" in info, "添加购物车失败"
        detail.switch_to_default()

    # ====================== 新增测试用例 ======================

    # 1. 手动输入合法数量（2~99）
    def test_detail_input_valid_num(self, reset_num):
        detail = reset_num
        input_num = 10
        el = detail.base_find_element(page.detail_num)
        el.clear()
        el.send_keys(str(input_num))
        current_num = detail.page_detail_num()
        assert current_num == input_num, f"输入{input_num}失败"

    # 2. 输入0 → 应自动重置为1
    def test_detail_input_zero(self, reset_num):
        detail = reset_num
        el = detail.base_find_element(page.detail_num)
        el.clear()
        el.send_keys("0")
        el.blur()  # 失去焦点触发校验
        time.sleep(0.5)
        current_num = detail.page_detail_num()
        assert current_num == 1, "输入0后未重置为1"

    # 3. 输入负数 → 应重置为1
    def test_detail_input_negative_num(self, reset_num):
        detail = reset_num
        el = detail.base_find_element(page.detail_num)
        el.clear()
        el.send_keys("-5")
        el.blur()
        time.sleep(0.5)
        current_num = detail.page_detail_num()
        assert current_num == 1, "输入负数后未重置为1"

    # 4. 输入超大数（超过库存/上限）→ 应限制为最大值
    def test_detail_input_over_limit(self, reset_num):
        detail = reset_num
        el = detail.base_find_element(page.detail_num)
        el.clear()
        el.send_keys("9999")
        el.blur()
        time.sleep(0.5)
        current_num = detail.page_detail_num()
        assert current_num <= 200, "输入超大数未做上限限制"

    # 5. 输入字母/特殊字符 → 应保留为1
    def test_detail_input_invalid_str(self, reset_num):
        detail = reset_num
        el = detail.base_find_element(page.detail_num)
        el.clear()
        el.send_keys("abc@#")
        el.blur()
        time.sleep(0.5)
        current_num = detail.page_detail_num()
        assert current_num == 1, "输入非法字符后未重置为1"

    # 6. 选择商品规格（颜色/尺寸等）
    def test_detail_choose_sku(self, reset_num):
        detail = reset_num
        detail.page_click_sku_color()  # 点击颜色规格
        time.sleep(0.5)
        assert detail.base_find_element(page.sku_selected), "商品规格选择失败"

    # 7. 未选择规格 → 加入购物车应提示失败
    def test_detail_addcart_without_sku(self, reset_num):
        detail = reset_num
        detail.page_reset_sku()  # 取消选中规格
        detail.page_detail_click_cart()
        detail.switch_to_addcart_iframe()
        info = detail.page_detail_info()
        assert "请选择" in info or "失败" in info, "未选规格应提示错误"
        detail.switch_to_default()

    # 8. 校验商品标题是否正确
    def test_detail_goods_title(self, reset_num):
        detail = reset_num
        title = detail.page_get_goods_title()
        assert len(title) > 0, "商品标题为空"
        assert "商品" in title or "手机" in title, "商品标题不符合预期"

    # 9. 点击收藏商品
    def test_detail_collect_goods(self, reset_num):
        detail = reset_num
        detail.page_click_collect()
        time.sleep(1)
        collect_text = detail.page_get_collect_text()
        assert "已收藏" in collect_text or "收藏成功" in collect_text, "商品收藏失败"

    # 10. 点击分享商品按钮存在
    def test_detail_share_button_exist(self, reset_num):
        detail = reset_num
        assert detail.base_element_exist(page.share_btn), "分享按钮不存在"

    # 11. 购物车数量显示正常
    def test_detail_cart_badge(self, reset_num):
        detail = reset_num
        badge_text = detail.page_get_cart_badge()
        assert badge_text.isdigit(), "购物车角标不是数字"

# 运行
if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_detail.py", "--tb=short"])