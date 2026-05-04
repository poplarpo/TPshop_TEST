import page
from base.base import Base


class PageCart(Base):

    # 点击增加
    def page_click_add(self):
        self.base_click(page.cart_more1)

    # 点击减少
    def page_click_less(self):
        self.base_click(page.cart_less1)

    # 获取商品数量
    def page_num(self):
        num=self.base_find_element(page.cart_num).get_attribute("value")
        return int(num)

    #判断全选按钮是否被选中
    def page_select_all(self):
        all = self.base_find_element(page.cart_select_all)
        return all.is_selected()

    #点击去结算
    def page_cart_order(self):
        self.base_click(page.order_link)



