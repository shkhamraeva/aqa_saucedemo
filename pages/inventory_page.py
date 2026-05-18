from playwright.sync_api import expect

from config.products import BACKPACK
from pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.title = self.page.locator(".title")
        self.backpack1 = self.page.get_by_text(BACKPACK)
        self.price = self.page.locator(f"//*[text()='{BACKPACK}']/../../..//*[@class='inventory_item_price']")
        self.btn_add_to_card = self.page.locator(f"//*[text()='{BACKPACK}']/../../..//button")
        self.loc_price = "../../*[@class='inventory_item_price']"
        self.inventory_item = self.page.locator(".inventory_item")
        self.inventory_item_name = self.page.locator(".inventory_item_name")
        self.inventory_item_price = self.page.locator(".inventory_item_price")
        self.inventory_item_img = self.page.locator(".inventory_item img")
        self.sort_dropdown = self.page.locator(".product_sort_container")
        self.backpack_img = self.page.locator(
            f"//*[text()='{BACKPACK}']/../../..//img")
        self.cart_badge = self.page.locator(".shopping_cart_badge")

    def check_backpack1_visible(self):
        expect(self.backpack1).to_be_visible()

    def get_backpack1_price(self) -> str:
        price_ = self.price.text_content()
        return price_

    def check_is_price(self):
        assert self.get_backpack1_price().startswith("$")

    def click_btn_add_to_cart(self):
        self.btn_add_to_card.click()

    def check_have_title(self, title_text: str):
        expect(self.title).to_be_visible()
        expect(self.title).to_have_text(title_text)
        return True

    def get_products_count(self):
        return self.inventory_item.count()

    def get_products_names(self) -> list:
        return self.inventory_item_name.all_text_contents()

    def get_products_prices(self) -> list:
        return self.inventory_item_price.all_text_contents()

    def get_products_images(self) -> list:
        return self.inventory_item_img.all()

    def select_sort(self, option: str):
        self.sort_dropdown.select_option(option)

    def get_products_prices_as_float(self) -> list[float]:
        prices = self.inventory_item_price.all_text_contents()
        return [float(p.replace("$", "")) for p in prices]

    def click_backpack_img(self):
        self.backpack_img.click()

    def check_btn_remove_visible(self):
        expect(self.btn_add_to_card).to_have_text("Remove")

    def click_btn_remove(self):
        self.btn_add_to_card.click()

    def get_cart_badge_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.text_content())
