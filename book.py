from item import Item


class Book(Item):
    def __init__(
        self, name: str, quantity: float, price: float, tax: float = 0.1
    ) -> None:
        super().__init__(name, quantity, price, tax)
