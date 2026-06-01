import allure

from config.users import USERS_PASSWORD, USER2_NAME
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

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

    @allure.title("Переход в корзину с любой страницы")
    def test_cart_006(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_cart_icon()
        cart_page = CartPage(login_user_page)
        cart_page.verify_cart_page_url()

    @allure.title("Возврат к покупкам из корзины")
    def test_cart_007(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_cart_icon()
        cart_page = CartPage(login_user_page)
        cart_page.click_continue_shopping()
        cart_page.verify_inventory_page_url()

    @allure.title("Пустая корзина")
    def test_cart_008(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_cart_icon()
        cart_page = CartPage(login_user_page)
        cart_page.verify_cart_is_empty()

    @allure.title("Сохранение корзины после перезагрузки")
    def test_cart_009(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_btn_add_to_cart()
        inventory_page.verify_items_in_bucket("1")
        inventory_page.reload_page()
        inventory_page.verify_items_in_bucket("1")

    @allure.title("Корзина при смене пользователя")
    def test_cart_010(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_btn_add_to_cart()
        inventory_page.verify_items_in_bucket("1")
        inventory_page.logout()

        login_page = LoginPage(login_user_page)
        login_page.login_procedure(USER2_NAME, USERS_PASSWORD)

        inventory_page2 = InventoryPage(login_user_page)
        inventory_page2.verify_bucket_is_empty()