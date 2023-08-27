"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
import random

from models import Product, Cart


@pytest.fixture
def book():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def pen():
    return Product("pen", 5, "This is a pen", 300)


@pytest.fixture
def scissors():
    return Product("scissors", 20, "These are scissors", 99)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, book):
        # TODO напишите проверки на метод check_quantity
        equal_quantity = book.check_quantity(book.quantity)
        less_quantity = book.check_quantity(book.quantity - 1)
        large_quantity = book.check_quantity(book.quantity + 1)

        assert equal_quantity is True
        assert less_quantity is True
        assert large_quantity is False

    def test_product_buy(self, book):
        # TODO напишите проверки на метод buy
        new_quantity, message = book.buy(book.quantity - 1)

        assert book.quantity == new_quantity

    def test_product_buy_more_than_available(self, book):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии

        with pytest.raises(ValueError):
            book.buy(book.quantity + 1)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_products_to_empty_cart(self, book, pen, scissors, cart):
        cart.add_product(book, 10)
        cart.add_product(pen)
        cart.add_product(scissors)
        products_in_cart = [item.name for item in cart.products]
        quantity_in_cart = [item for item in cart.products.values()]

        assert products_in_cart == ['book', 'pen', 'scissors']
        assert quantity_in_cart == [10, 1, 1]

    def test_add_same_product(self, book, cart):
        number_of_additions = 2
        for _ in range(number_of_additions):
            cart.add_product(book)

        assert cart.products.get(book) == number_of_additions

    def test_remove_one_product(self, book, pen, cart):
        cart.add_product(book)
        cart.add_product(pen)
        cart.remove_product(book)
        products_in_cart = [item.name for item in cart.products]

        assert products_in_cart == ['pen']

    def test_remove_items(self, book, cart):
        cart.add_product(book, 50)
        new_quantity = cart.remove_product(book, 10)

        assert cart.products.get(book) == new_quantity

    def test_clear(self, book, pen, scissors, cart):
        cart.add_product(book)
        cart.add_product(pen)
        cart.add_product(scissors)
        cart.clear()

        assert len(cart.products) == 0

    def test_get_total_price(self, book, pen, scissors, cart):
        cart.add_product(book, 3)
        cart.add_product(pen, 4)
        cart.add_product(scissors, 1)
        product_prices = [item.price for item in cart.products]
        summa = sum(map(lambda x, y: x * y, cart.products.values(), product_prices))
        subtotal = cart.get_total_price()

        assert summa == subtotal

    def test_buy_all_cart(self, book, pen, scissors, cart):
        cart.add_product(book, 3)
        cart.add_product(pen, 4)
        cart.add_product(scissors, 98)
        cart.buy()

        assert len(cart.products) == 0

    def test_buy_one_product(self, book, pen, scissors, cart):
        cart.add_product(book, 3)
        cart.add_product(pen, 4)
        cart.add_product(scissors, 98)
        cart.buy(pen)
        products_in_cart = [item.name for item in cart.products]

        assert "pen" not in products_in_cart

    def test_buy_more_than_have(self, pen, scissors, cart):
        cart.add_product(scissors, 100)
        with pytest.raises(ValueError):
            cart.buy()
