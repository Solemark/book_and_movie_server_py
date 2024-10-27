from item import Item


class Movie(Item):
    def __init__(
        self, name: str, quantity: float, price: float, tax: float = 0.3
    ) -> None:
        super().__init__(name, quantity, price, tax)
