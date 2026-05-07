import allure

from config.base import INVENTORY_URL
from config.products import EXPECTED_PRODUCTS, EXPECTED_PRICES
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from config.users import USER1_NAME, USERS_PASSWORD

@allure.epic("SauceDemo")
@allure.feature("Страница товаров")
class TestInventory:

    @allure.title("Отображение всех 6 товаров")
    def test_inv_001(self,page):
        """
        001 Проверить, что на странице 6 карточек товаров
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()

        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)
        assert page.locator(".inventory_item").count() == 6, (
            f"Ошибка: ожидалось 6 товаров, но отображается "
            f"{page.locator('.inventory_item').count()}")

    @allure.title("Проверка названий всех товаров")
    def test_inv_002(self, page):
        """
        002 Сверить названия с ожидаемым списком
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()

        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)
        actual_names = inventory_page.get_products_names()
        assert sorted(actual_names) == sorted(EXPECTED_PRODUCTS), (
             f"Названия товаров не совпадают с эталоном.\nОжидалось: "
             f"{sorted(EXPECTED_PRODUCTS)}\nПолучено: {sorted(actual_names)}")

    @allure.title("Проверка цен всех товаров")
    def test_inv_003(self, page):
        """
        003 Цены соответствуют эталону (например, Backpack = $29.99)
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()

        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)
        actual_prices = inventory_page.get_products_prices()
        assert sorted(actual_prices) == sorted(EXPECTED_PRICES), (
             f"Цены не совпадают с эталоном.\nОжидалось: "
             f"{sorted(EXPECTED_PRICES)}\nПолучено: {sorted(actual_prices)}")

    @allure.title("Проверка изображений товаров")
    def test_inv_004(self, page):
        """
        004 Все <img> имеют src, не битые
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)
        images = inventory_page.get_products_images()

        for i, img in enumerate(images):
            src = img.get_attribute("src")
            assert src and len(src) > 0, (
                f"У товара индекс {i} отсутствует атрибут src")
            is_loaded = img.evaluate(
                "el => el.complete && el.naturalWidth > 0")
            assert is_loaded, (
                f"Изображение товара '{src}' не загрузилось или битое")