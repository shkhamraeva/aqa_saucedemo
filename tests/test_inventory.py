from config.base import INVENTORY_URL
from config.products import EXPECTED_PRODUCTS, EXPECTED_PRICES
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from config.users import USER1_NAME, USERS_PASSWORD

class TestInventory:

    def test_inv_001_check_count_products(self,page):
        login_page = LoginPage(page)
        login_page.open()

        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)
        assert page.locator(".inventory_item").count() == 6, \
        (f"Ошибка: ожидалось 6 товаров, но отображается "
         f"{page.locator('.inventory_item').count()}")

    def test_inv_002_check_products_names(self, page):
        login_page = LoginPage(page)
        login_page.open()

        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)
        actual_names = inventory_page.get_products_names()
        assert sorted(actual_names) == sorted(EXPECTED_PRODUCTS), \
            (f"Названия товаров не совпадают с эталоном.\nОжидалось: "
             f"{sorted(EXPECTED_PRODUCTS)}\nПолучено: {sorted(actual_names)}")

    def test_inv_003_check_products_prices(self, page):
        login_page = LoginPage(page)
        login_page.open()

        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)
        actual_prices = inventory_page.get_products_prices()
        assert sorted(actual_prices) == sorted(EXPECTED_PRICES), \
            (f"Цены не совпадают с эталоном.\nОжидалось: "
             f"{sorted(EXPECTED_PRICES)}\nПолучено: {sorted(actual_prices)}")