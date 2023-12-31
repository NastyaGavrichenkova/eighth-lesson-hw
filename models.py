class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return self.quantity >= quantity

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity):
            new_quantity = self.quantity - quantity
            self.quantity = new_quantity
            success_message = 'Your purchase was successful!'
            return new_quantity, success_message
        else:
            raise ValueError(f'There is not enough {self.name}. \n'
                             f'Max quantity is {self.quantity}.')

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        self.products[product] = self.products.get(product, 0) + buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if remove_count is None or remove_count > self.products.get(product):
            self.products.pop(product)
        else:
            new_quantity = self.products.get(product) - remove_count
            self.products[product] = new_quantity
            return new_quantity

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        subtotal = sum([product.price * quantity for product, quantity in self.products.items()])
        return subtotal

    def buy(self, item=None):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        message = ''
        if item is None:
            for product, quantity in self.products.items():
                new_quantity, message = product.buy(self.products[product])
            self.clear()
        else:
            item.buy(self.products[item])
            self.remove_product(item)

        print(message)
