import allure

from config.base import INVENTORY_URL
from config.products import ExpectedProduct
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

        actual_count = inventory_page.get_products_count()
        expected_count = len(ExpectedProduct)
        assert actual_count == expected_count, \
            (f"Ошибка: ожидалось {expected_count} товаров, "
             f"но отображается {actual_count}")

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

        actual_names = sorted(inventory_page.get_products_names())
        expected_names = sorted(p.title for p in ExpectedProduct)

        assert actual_names == expected_names, \
            (f"Названия товаров не совпадают с эталоном.\n"
             f"Ожидалось: {expected_names}\n"
             f"Получено:  {actual_names}")

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

        actual_prices = sorted(inventory_page.get_products_prices())
        expected_prices = sorted(p.price for p in ExpectedProduct)

        assert actual_prices == expected_prices, \
        (f"Цены не совпадают с эталоном.\n"
         f"Ожидалось: {expected_prices}\n"
         f"Получено:  {actual_prices}")

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

    @allure.title("Сортировка по цене: низкая → высокая")
    def test_inv_005(self, page):
        """
        005 Выбрать сортировку, проверить порядок цен.
        Цены идут по возрастанию
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)

        inventory_page.select_sort("lohi")
        actual_prices = inventory_page.get_products_prices_as_float()
        expected_prices = sorted(actual_prices)

        assert actual_prices == expected_prices, \
            (f"Цены не отсортированы по возрастанию.\n"
             f"Ожидалось: {expected_prices}\n"
             f"Получено:  {actual_prices}")

    @allure.title("Сортировка по цене: высокая → низкая")
    def test_inv_006(self, page):
        """
        006 Аналогично, но по убыванию. Цены по убыванию
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)

        inventory_page.select_sort("hilo")
        actual_prices = inventory_page.get_products_prices_as_float()
        expected_prices = sorted(actual_prices, reverse=True)

        assert actual_prices == expected_prices, \
            (f"Цены не отсортированы по убыванию.\n"
             f"Ожидалось: {expected_prices}\n"
             f"Получено:  {actual_prices}")

    @allure.title("Сортировка по названию: A → Z")
    def test_inv_007(self, page):
        """
         007 Проверить алфавитный порядок.
         Названия отсортированы лексикографически
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)

        inventory_page.select_sort("az")
        actual_names = inventory_page.get_products_names()
        expected_names = sorted(actual_names)

        assert actual_names == expected_names, \
            (f"Названия не отсортированы по алфавиту A→Z.\n"
             f"Ожидалось: {expected_names}\n"
             f"Получено:  {actual_names}")

    @allure.title("Фильтрация после добавления в корзину")
    def test_inv_008(self, page):
        """
        008 Добавить товар → изменить сортировку → товар на месте.
        Товар не "теряется" при смене сортировки
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)

        inventory_page.click_btn_add_to_cart()
        inventory_page.select_sort("lohi")
        actual_names = inventory_page.get_products_names()
        assert ExpectedProduct.BACKPACK.title in actual_names, \
            (
                f"Товар '{ExpectedProduct.BACKPACK.title}' "
                f"не найден после смены сортировки.\n"
                f"Товары на странице: {actual_names}"
            )

    @allure.title("Клик по изображению товара (если есть переход)")
    def test_inv_009(self, page):
        """
        009 Клик на картинку → переход на детальную (если реализовано).
        Проверка навигации
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)

        inventory_page.click_backpack_img()

        actual_url = page.url
        assert "inventory-item" in actual_url, \
        (f"Ожидался переход на детальную страницу товара,\n"
         f"но текущий URL: {actual_url}")

    @allure.title("Проверка кнопки 'Remove' после добавления в корзину")
    def test_inv_010(self, page):
        """
        010 Добавить → кнопка сменилась на "Remove" → нажать →
        товар исчез из корзины. Бейдж корзины = 0
        :param page: фикстура браузера со страницей
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.expect_to_have_url(INVENTORY_URL)

        inventory_page.click_btn_add_to_cart()
        inventory_page.check_btn_remove_visible()
        inventory_page.click_btn_remove()
        actual_count = inventory_page.get_cart_badge_count()

        assert actual_count == 0, \
            (f"Ожидался бейдж корзины = 0, "
             f"но получено: {actual_count}")