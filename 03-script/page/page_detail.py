import page
from base.base import Base


class PageDetail(Base):

    # 点击立即购买
    def page_detail_click_buy(self):
        self.base_click(page.detail_buynow)

    # 点击加入购物车
    def page_detail_click_cart(self):
        self.base_click(page.detail_addcart)

    # 点击增加数量
    def page_detail_addnum(self):
        self.base_click(page.detail_add)

    # 点击减少数量
    def page_detail_less_num(self):
        self.base_click(page.detail_mins)

    #获取数量
    def page_detail_num(self):
        num=self.base_find_element(page.detail_num).get_attribute("value")
        return int(num)

    def switch_to_addcart_iframe(self):
        """切换到添加购物车的 iframe"""
        iframe = self.base_find_element(page.detail_iframe)
        self.driver.switch_to.frame(iframe)

    def switch_to_default(self):
        """切回主页面"""
        self.driver.switch_to.default_content()

    #获取添加成功提示
    def page_detail_info(self):

        info=self.base_find_element(page.detail_add_ok).text
        return info


