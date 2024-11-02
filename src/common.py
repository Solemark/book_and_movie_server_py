from enum import Enum
from os import linesep
from typing import Any
from socket import socket


class File(Enum):
    Book = "books"
    Movie = "movies"
    Coord = "coord"


class Item:
    def __init__(self, file: File, name: str, quantity: float, price: float) -> None:
        self.__file: File = file
        self.__name: str = name
        self.__quantity: float = float(quantity)
        self.__price: float = float(price)
        self.__tax: float = self.__set_tax(file)

    def __set_tax(self, file: File) -> float:
        """Set the tax based on the item type"""
        match file:
            case File.Book:
                return 0.1
            case File.Movie:
                return 0.3
            case _:
                return 0.0

    def get_type(self) -> File:
        """Get the item type"""
        return self.__file

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


class Server:
    def __init__(
        self, port: int, file: File, conn: int = 5, addr: str = "localhost"
    ) -> None:
        self.__ADDRESS: str = addr
        self.__PORT: int = port
        self.__CONNECTIONS: int = conn

        self.SERVER = socket()
        """SERVER isn't private, is used by children"""
        self.SERVER.bind((self.__ADDRESS, self.__PORT))
        self.SERVER.listen(self.__CONNECTIONS)

        """List of existing items on the server"""
        self.__data: list[Item] = self.get_file(file) if file.value != "coord" else []
        print(f"Listening on {self.__ADDRESS}:{self.__PORT}")

    def get_file(self, file: File) -> list[Item]:
        """Read file and return list"""
        f: Any = open(f"data/{file.value}.csv")
        data: list[Item] = []
        for i in f:
            d: list[str] = i.split(",")
            if file != File.Coord:
                data.append(Item(file, d[0], float(d[1]), float(d[2])))
        return data

    def save_file(self, item: Item) -> bool:
        """Save data to disk"""
        try:
            self.__data.append(item)
            f: Any = open(f"data/{item.get_type().value}.csv", "w")
            for d in self.__data:
                f.write(d.__str__() + linesep)
            return True
        except Exception:
            return False

    def send_item(self, file: File, item: list[str]) -> str:
        """Send message for type and await response"""
        s: socket = socket()
        s.connect(("localhost", 8001 if file is File.Book else 8002))
        s.send(f"{item[1]},{item[2]},{item[3]}".encode())
        res: str = s.recv(1024).decode()
        s.close()
        return res
