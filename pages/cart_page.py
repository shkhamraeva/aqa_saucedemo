from playwright.sync_api import expect
from config.base import URL_BASE, INVENTORY_URL, URL_CART
from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.cart_badge = self.page.locator(".shopping_cart_badge")
        self.continue_shopping_btn = self.page.locator("#continue-shopping")
        self.cart_items = self.page.locator(".cart_item")

    def check_cart_badge(self, expected: str):
        expect(self.cart_badge).to_have_text(expected)

    def verify_cart_page_url(self):
        expect(self.page).to_have_url(URL_BASE + URL_CART)

    def verify_inventory_page_url(self):
        expect(self.page).to_have_url(URL_BASE + INVENTORY_URL)

    def click_continue_shopping(self):
        self.continue_shopping_btn.click()

    def verify_cart_is_empty(self):
        expect(self.cart_items).to_have_count(0)