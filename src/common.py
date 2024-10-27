from enum import Enum
from os import linesep
from typing import Any
from socket import socket

from book import Book
from movie import Movie


class File(Enum):
    Book = "books"
    Movie = "movies"
    Coord = "coord"


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
        self.__data: list[Book | Movie] = (
            self.get_file(file) if file.value != "coord" else []
        )
        print(f"Listening on {self.__ADDRESS}:{self.__PORT}")

    def get_file(self, file: File) -> list[Book | Movie]:
        """Read file and return list"""
        f: Any = open(f"data/{file.value}.csv")
        data: list[Book | Movie] = []
        for i in f:
            d: list[str] = i.split(",")
            match file:
                case File.Book:
                    data.append(Book(d[0], float(d[1]), float(d[2])))
                case File.Movie:
                    data.append(Movie(d[0], float(d[1]), float(d[2])))
        return data

    def save_file(self, file: File, item: Book | Movie) -> bool:
        """Save data to disk"""
        try:
            self.__data.append(item)
            f: Any = open(f"data/{file.value}.csv", "w")
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
