import page
from base.base import Base


class PageRegister(Base):
    # 点击注册
    def page_click_register_link(self):
        self.base_click(page.register_link)

    # 输入手机号码
    def page_input_phonenum(self, phonenum):
        self.base_input(page.register_phone_num, phonenum)

    # 输入验证
    def page_input_verify_code(self, code):
        self.base_input(page.register_verify_code, code)

    # 输入密码
    def page_input_password(self, pwd):
        self.base_input(page.register_pwd, pwd)

    #确认密码
    def page_input_pwd2(self,pwd):
        self.base_input(page.register_confirm_pwd, pwd)

    # 推荐人手机
    def page_cell_number(self, number):
        self.base_input(page.register_cell_phone, number)


    # 点击勾选协议
    def page_click_protocol(self):
        self.base_click(page.register_protocal)

    #点击统一协议并注册
    def page_click_agree(self):
        self.base_click(page.register_btn_agree)

    # 获取异常提示信息
    def page_get_error_info(self):
        return self.base_get_text(page.register_error_content)

    # 点击异常信息框 确定
    def page_click_err_btn_ok(self):
        self.base_click(page.register_btn_ok)

    # 截图
    def page_get_img(self):
        self.base_get_image()

    # 组合业务方法
    def page_register(self,phonenum, code,pwd,pwd2):
        self.page_input_phonenum(phonenum)
        self.page_input_verify_code(code)
        self.page_input_password(pwd)
        self.page_input_pwd2(pwd2)
        #默认就勾选的就可以不用点
        # self.page_click_protocol()
        self.page_click_agree()

