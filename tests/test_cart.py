import allure

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

@allure.epic("SauceDemo")
@allure.feature("Корзина")
class TestCart:
    @allure.title("Добавление одного товара")
    def test_cart_001(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_btn_add_to_cart()
        cart_page = CartPage(login_user_page)
        cart_page.check_cart_badge("1")

    @allure.title("Добавление нескольких разных товаров")
    def test_cart_002(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_multiple_items_to_cart(count=3)
        cart_page = CartPage(login_user_page)
        cart_page.check_cart_badge("3")

    @allure.title("Добавление одного товара несколько раз")
    def test_cart_003(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.verify_first_item_button_is_remove()
        inventory_page.verify_items_in_bucket("1")

    @allure.title("Удаление товара из корзины")
    def test_cart_004(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_btn_add_to_cart()
        inventory_page.verify_items_in_bucket("1")
        inventory_page.check_btn_remove_visible()
        inventory_page.click_btn_remove()
        inventory_page.verify_bucket_is_empty()

