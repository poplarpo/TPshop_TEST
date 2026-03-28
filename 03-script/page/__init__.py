from selenium.webdriver.common.by import By

"""以下为登录页面元素配置信息"""
# 登录链接
login_link = By.PARTIAL_LINK_TEXT, "登录"
# 用户名
login_username = By.ID, "username"
# 密码
login_pwd = By.ID, "password"
# 验证码
login_verify_code = By.ID, "verify_code"
# 登录按钮
login_btn = By.CSS_SELECTOR, ".J-login-submit"
# 获取异常文本信息
login_err_info = By.CSS_SELECTOR, ".layui-layer-content"
# 点击异常提示框 按钮
login_err_btn_ok = By.CSS_SELECTOR, ".layui-layer-btn0"

"""以下为注册配置数据"""
#注册连接
register_link = By.PARTIAL_LINK_TEXT, "注册"
#电话号码
register_phone_num = By.CSS_SELECTOR,'.J_cellphone'
#图像验证码
register_verify_code =By.CSS_SELECTOR,'.J_imgcode'
#密码
register_pwd=By.CSS_SELECTOR,'.J_password'
#确认密码
register_confirm_pwd=By.CSS_SELECTOR,'.J_password2'
#推荐人手机
register_cell_phone=By.CSS_SELECTOR,'.J_cellphone'
#协议勾选框
register_protocal=By.CSS_SELECTOR,'.J_protocal'
#点击同意协议并注册
register_btn_agree=By.CSS_SELECTOR,'.J_btn_agree'
#异常信息
register_error_content=By.CSS_SELECTOR,'.layui-layer-ico2'
#信息确定按钮
register_btn_ok=By.CSS_SELECTOR,'.layui-layer-btn0'

"""以下为购物车配置数据"""
"""以下都是针对商品edge_6"""
#选择框
cart_checkbox = By.CSS_SELECTOR, "input.checkCart.checkCircle"
cart_selected=By.CSS_SELECTOR, "#edge_6 input.check-box"
#数量减少框
cart_less1=By.CSS_SELECTOR, "#edge_6 a.decrement"
#数量增加框
cart_more1=By.CSS_SELECTOR, "#edge_6 a.increment"
#数量
cart_num= By.NAME, "changeQuantity_6"
#选中所有商品
cart_select_all=By.CSS_SELECTOR,'checkCartAll'
#删除选中商品
cart_delete_all=By.ID,'removeGoods'


"""以下为商品详情页配置数据"""
#立即购买
detail_buynow=By.CSS_SELECTOR,'.paybybill'
#加入购物车
detail_addcart=By.CSS_SELECTOR,'.addcar'
#数量
detail_num= By.XPATH, "//input[@class='buyNum']"
#数量-
detail_mins=By.XPATH,"//a[@class='mins']"
#数量+
detail_add=By.XPATH,"//a[@class='add']"
#加入购物车成功后提示
detail_add_ok=By.XPATH, "//div[@class='conect-title']/span"
#加入购物车后的iframe
detail_iframe=By.ID, "layui-layer-iframe1"

"""以下为结算页配置数据"""
# 结算链接
order_link = By.CSS_SELECTOR, "a.gwc-qjs"
#提交订单
order_submit =By.CSS_SELECTOR, "a.Sub-orders.gwc-qjs"