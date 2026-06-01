import re

from playwright.sync_api import expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.first_name_input = self.page.locator("#first-name")
        self.last_name_input = self.page.locator("#last-name")
        self.postal_code_input = self.page.locator("#postal-code")
        self.continue_button = self.page.locator("#continue")
        self.cancel_button = self.page.locator("#cancel")
        self.error_message_container = self.page.locator("[data-test='error']")

    def fill_checkout_form(self, first_name: str = "", last_name: str = "", postal_code: str = ""):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def click_continue(self):
        self.continue_button.click()

    def click_cancel(self):
        self.cancel_button.click()

    def verify_error_message(self, expected_text: str):
        expect(self.error_message_container).to_have_text(expected_text)


class CheckoutOverviewPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.finish_button = self.page.locator("#finish")
        self.item_total_label = self.page.locator(".summary_subtotal_label")
        self.tax_label = self.page.locator(".summary_tax_label")
        self.total_label = self.page.locator(".summary_total_label")
        self.cart_items = self.page.locator(".cart_item")
        self.item_prices = self.page.locator(".inventory_item_price")

    def click_finish(self):
        self.finish_button.click()

    def get_item_total(self) -> float:
        text = self.item_total_label.text_content()
        return float(text.split("$")[1])

    def get_tax(self) -> float:
        text = self.tax_label.text_content()
        return float(text.split("$")[1])

    def get_total(self) -> float:
        text = self.total_label.text_content()
        return float(text.split("$")[1])

    def verify_total_calculation(self):
        item_total = self.get_item_total()
        tax = self.get_tax()
        total = self.get_total()
        assert abs(total - (item_total + tax)) < 0.01

    def verify_prices_format(self):
        price_pattern = re.compile(r"\$\d+\.\d{2}$")
        assert price_pattern.search(
            self.item_total_label.text_content().strip())
        assert price_pattern.search(self.tax_label.text_content().strip())
        assert price_pattern.search(self.total_label.text_content().strip())

    def get_calculated_items_sum(self) -> float:
        prices_text = self.item_prices.all_text_contents()
        return sum(float(price.replace("$", "")) for price in prices_text)

    def verify_multiple_items_checkout(self, expected_count: int):
        expect(self.cart_items).to_have_count(expected_count)
        calculated_sum = self.get_calculated_items_sum()
        displayed_item_total = self.get_item_total()
        assert abs(calculated_sum - displayed_item_total) < 0.01
        self.verify_total_calculation()

class CheckoutCompletePage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.complete_header = self.page.locator(".complete-header")

    def verify_checkout_complete_message(self):
        expect(self.complete_header).to_have_text("Thank you for your order!")
