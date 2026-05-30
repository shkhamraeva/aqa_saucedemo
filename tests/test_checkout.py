import allure
import pytest

from config.users import FIRST_NAME, LAST_NAME, POSTAL_CODE, \
    INVALID_POSTAL_CODE
from pages.cart_page import CartPage
from pages.checkout_page import (CheckoutPage, CheckoutOverviewPage,
                                 CheckoutCompletePage)
from pages.inventory_page import InventoryPage


@allure.epic("SauceDemo")
@allure.feature("Чекаут")
class TestCheckout:

    @allure.title("Полный успешный чекаут")
    def test_check_001(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            postal_code=POSTAL_CODE
        )
        checkout_page.click_continue()

        overview_page = CheckoutOverviewPage(login_user_page)
        overview_page.click_finish()

        complete_page = CheckoutCompletePage(login_user_page)
        complete_page.verify_checkout_complete_message()

    @pytest.mark.parametrize(
        "first_name, last_name, postal_code, expected_error",
        [
            ("", LAST_NAME, POSTAL_CODE, "Error: First Name is required"),
            (FIRST_NAME, "", POSTAL_CODE, "Error: Last Name is required"),
            (FIRST_NAME, LAST_NAME, "", "Error: Postal Code is required"),
        ],
        ids=["Empty First Name", "Empty Last Name", "Empty Postal Code"]
    )
    @allure.title("Чекаут с пустым полем формы")
    def test_check_002_003_004(self, login_user_page, first_name, last_name,
                               postal_code, expected_error):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(
            first_name=first_name,
            last_name=last_name,
            postal_code=postal_code
        )
        checkout_page.click_continue()
        checkout_page.verify_error_message(expected_error)

    @allure.title("Валидация Postal Code — любой формат принимается")
    def test_check_005(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            postal_code=INVALID_POSTAL_CODE
        )
        checkout_page.click_continue()

        overview_page = CheckoutOverviewPage(login_user_page)
        overview_page.click_finish()

        complete_page = CheckoutCompletePage(login_user_page)
        complete_page.verify_checkout_complete_message()

    @allure.title("Возврат к корзине из шага 1 чекаута")
    def test_check_006(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.click_cancel()

        cart_page.verify_cart_page_url()
        cart_page.verify_cart_has_items(1)

    @allure.title("Возврат к покупкам из шага 1 чекаута")
    def test_check_007(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.click_cancel()

        cart_page.click_continue_shopping()
        cart_page.verify_inventory_page_url()

    @allure.title("Расчёт итоговой суммы")
    def test_check_008(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            postal_code=POSTAL_CODE
        )
        checkout_page.click_continue()

        overview_page = CheckoutOverviewPage(login_user_page)
        overview_page.verify_total_calculation()

    @allure.title("Округление цен до 2 знаков после запятой")
    def test_check_009(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            postal_code=POSTAL_CODE
        )
        checkout_page.click_continue()

        overview_page = CheckoutOverviewPage(login_user_page)
        overview_page.verify_prices_format()

    @allure.title("Чекаут с несколькими товарами")
    def test_check_010(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_multiple_items_to_cart(count=2)
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            postal_code=POSTAL_CODE
        )
        checkout_page.click_continue()

        overview_page = CheckoutOverviewPage(login_user_page)
        overview_page.verify_multiple_items_checkout(expected_count=2)
        overview_page.click_finish()

        complete_page = CheckoutCompletePage(login_user_page)
        complete_page.verify_checkout_complete_message()