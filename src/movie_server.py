from common import Server, File, Item


class MovieServer(Server):
    def __init__(
        self, port: int = 8002, conn: int = 5, addr: str = "localhost"
    ) -> None:
        super().__init__(port, File.Movie, conn, addr)
        self.__run_server()

    def __run_server(self) -> None:
        """Run the Movie Server"""
        while True:
            sock, addr = self.SERVER.accept()
            print(f"Incoming message from {addr}")

            i: list[str] = sock.recv(1024).decode().split(",")
            res: bool = self.save_file(Item(File.Movie, i[0], float(i[1]), float(i[2])))

            sock.send(
                "Book saved successfully!".encode()
                if res
                else "Book failed to save!".encode()
            )
            sock.close()


if __name__ == "__main__":
    MovieServer()
