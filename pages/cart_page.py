from playwright.sync_api import expect
from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.cart_badge = self.page.locator(".shopping_cart_badge")

    def check_cart_badge(self, expected: str):
        expect(self.cart_badge).to_have_text(expected)