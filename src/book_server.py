from book import Book

from common import Server, File


class BookServer(Server):
    def __init__(
        self, port: int = 8001, conn: int = 5, addr: str = "localhost"
    ) -> None:
        super().__init__(port, File.Book, conn, addr)
        self.__run_server()

    def __run_server(self) -> None:
        """Run the Book Server"""
        while True:
            sock, addr = self.SERVER.accept()
            print(f"Incoming message from {addr}")

            b: list[str] = sock.recv(1024).decode().split(",")
            res: bool = self.save_file(File.Book, Book(b[0], float(b[1]), float(b[2])))

            sock.send(
                "Book saved successfully!".encode()
                if res
                else "Book failed to save!".encode()
            )
            sock.close()


if __name__ == "__main__":
    BookServer()
