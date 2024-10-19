class Item:
    def __init__(
        self, name: str, quantity: float, price: float, tax: float = 0
    ) -> None:
        self.__name = name
        self.__quantity = quantity
        self.__price = price
        self.__tax = tax

    def get_name(self) -> str:
        """Get the item name"""
        return self.__name

    def get_quantity(self) -> float:
        """Get the item quantity"""
        return self.__quantity

    def get_price(self) -> float:
        """Get the item price"""
        return self.__price

    def get_tax(self) -> float:
        """Get the item tax"""
        return self.__tax

    def get_result(self) -> float:
        """Get the item result"""
        return (self.__quantity * self.__price) + (
            (self.__quantity * self.__price) * self.__tax
        )

    def __str__(self) -> str:
        return f"{self.__name},{self.__quantity},{self.__price}"
