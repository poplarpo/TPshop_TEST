from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

import page
from base.base import Base


class PageOrder(Base):
    # 点击去结算链接
    def page_order_link(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(lambda x: x.execute_script("return document.readyState") == "complete")

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            checkout_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.gwc-qjs")))

            if checkout_btn:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkout_btn)
                time.sleep(1)

                try:
                    checkout_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", checkout_btn)

                time.sleep(3)
                wait.until(lambda x: x.execute_script("return document.readyState") == "complete")
            else:
                raise Exception("找不到去结算按钮")

        except TimeoutException as e:
            raise e

    # 点击提交订单
    def page_order_submit(self):
        try:
            wait = WebDriverWait(self.driver, 15)
            wait.until(lambda x: x.execute_script("return document.readyState") == "complete")

            # 检查是否在订单确认页面
            if "cart2" not in self.driver.current_url and "cart3" not in self.driver.current_url:
                self.driver.get("http://localhost/Home/Cart/cart2.html")
                time.sleep(3)
                wait.until(lambda x: x.execute_script("return document.readyState") == "complete")

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # 直接调用submit_order函数
            has_function = self.driver.execute_script("return typeof submit_order !== 'undefined'")
            if has_function:
                self.driver.execute_script("submit_order();")
                time.sleep(3)
            else:
                # 尝试通过JavaScript点击
                js_click = """
                var elements = document.querySelectorAll('a.Sub-orders.gwc-qjs, a.Sub-orders, .Sub-orders');
                for(var i = 0; i < elements.length; i++) {
                    if(elements[i].onclick || elements[i].getAttribute('onclick')) {
                        elements[i].click();
                        return true;
                    }
                }
                return false;
                """
                result = self.driver.execute_script(js_click)
                if not result:
                    raise Exception("无法找到提交订单按钮")
                time.sleep(3)

        except Exception as e:
            self.driver.save_screenshot("submit_order_error.png")
            raise e