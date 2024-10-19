from socket import socket
from typing import Any
from os import linesep
from book import Book


class BookServer:
    def __init__(
        self, address: str = "localhost", port: int = 8001, connections: int = 5
    ) -> None:
        self.__ADDRESS: str = address
        self.__PORT: int = port
        self.__CONNECTIONS: int = connections
        self.__books: list[Book] = self.__get_books()

        self.__SERVER = socket()
        self.__SERVER.bind((self.__ADDRESS, self.__PORT))
        self.__SERVER.listen(self.__CONNECTIONS)

        print(f"Listening on {self.__ADDRESS}:{self.__PORT}")

        self.__run_server()

    def __run_server(self) -> None:
        """Run the Book Server"""
        while True:
            sock, addr = self.__SERVER.accept()
            print(f"Incoming message from {addr}")

            b: list[str] = sock.recv(1024).decode().split(",")
            res: bool = self.__save_books(Book(b[0], float(b[1]), float(b[2])))

            sock.send(
                "Book saved successfully!".encode()
                if res
                else "Book failed to save!".encode()
            )
            sock.close()

    def __get_books(self) -> list[Book]:
        """Get the list of books from file"""
        f: Any = open("data/books.csv").readlines()
        books: list[Book] = []
        for d in f:
            b: list[str] = d.split(",")
            books.append(Book(b[0], float(b[1]), float(b[2])))
        return books

    def __save_books(self, b: Book) -> bool:
        """Save the Book list"""
        try:
            self.__books.append(b)
            f: Any = open("data/books.csv", "w")
            for book in self.__books:
                f.write(book.__str__() + linesep)
            return True
        except Exception:
            return False


if __name__ == "__main__":
    BookServer()
