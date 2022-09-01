import pytest
from playwright.sync_api import Page
from pages.sovcombank.cards_page import CardsPage
import logging


logger = logging.getLogger("tests")


@pytest.fixture()
def main_bank_page(page: Page):
    bank_page = CardsPage('https://sovcombank.ru', page)
    bank_page.delete_cookies()
    bank_page.open()
    return bank_page


@pytest.mark.only_browser("chromium")
def test_validation_message_is_visible(main_bank_page):
    """Тест с главной страницы сайта переходит на вкладку карты.
        Затем кликает по клавише заказать халву используя JS скрипт.
        Переключается но новую вкладку.
        Проверяет наличие сообщения об ошибке если снять чекбокс на обработку персональых данных.
        Нажимает кнопку получить карту.
        Получает список полей и список сообщений об ошибке под каждым полем
        Созает словарь с ключом в виде названия поля и значением текстом ошибки.
        Выводит словарь в консоль.
        Закрывает текущую вкладку и переходит на предыдущую."""

    bank_page = main_bank_page
    bank_page.go_to_section('Карты')
    bank_page.order_halva_card()
    bank_page.edit_check_box_order()
    assert bank_page.get_check_box_error()
    assert bank_page.get_fields_and_warnings()
    bank_page.close_page()
