from common import Server, File


class ServerCoordinator(Server):
    def __init__(
        self, port: int = 8000, conn: int = 5, addr: str = "localhost"
    ) -> None:
        super().__init__(port, File.Coord, conn, addr)
        self.__run_server()

    def __run_server(self) -> None:
        """run the server and wait for incoming messages"""
        while True:
            sock, addr = self.SERVER.accept()
            print(f"Incoming message from {addr}")

            m: list[str] = sock.recv(1024).decode().split(",")
            r: str = self.__send_message(m)

            sock.send(r.encode())
            sock.close()

    def __send_message(self, item: list[str]) -> str:
        """Send message to type and await response"""
        response: str = ""
        match item[0]:
            case "B":
                response = self.send_item(File.Book, item)
            case "M":
                response = self.send_item(File.Movie, item)
        return response


if __name__ == "__main__":
    ServerCoordinator()
