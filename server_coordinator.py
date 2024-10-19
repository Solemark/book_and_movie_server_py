from socket import socket


class ServerCoordinator:
    def __init__(self) -> None:
        self.__ADDRESS: str = "localhost"
        self.__PORT: int = 8000
        self.__CONNECTIONS: int = 5

        self.__SERVER = socket()
        self.__SERVER.bind((self.__ADDRESS, self.__PORT))
        self.__SERVER.listen(self.__CONNECTIONS)

        print(f"Listening on {self.__ADDRESS}:{self.__PORT}")

        self.__run_server()

    def __run_server(self) -> None:
        """run the server and wait for incoming messages"""
        while True:
            sock, addr = self.__SERVER.accept()
            print(f"Incoming message from {addr}")

            m: list[str] = sock.recv(1024).decode().split(",")
            r: str = self.__send_message(m)

            sock.send(r.encode())
            sock.close()

    def __send_message(self, m: list[str]) -> str:
        """Send message to type and await response"""
        response: str = ""
        match m[0]:
            case "B":
                response = self.__send_book(m)
            case "M":
                response = self.__send_movie(m)
        return response

    def __send_book(self, m: list[str]) -> str:
        """Send message for type book and await response"""
        s: socket = socket()
        s.connect(("localhost", 8001))
        s.send(f"{m[1]},{m[2]},{m[3]}".encode())
        res = s.recv(1024).decode()
        s.close()
        return res

    def __send_movie(self, m: list[str]) -> str:
        """Send message for type movie and await response"""
        s: socket = socket()
        s.connect(("localhost", 8002))
        s.send(f"{m[1]},{m[2]},{m[3]}".encode())
        res = s.recv(1024).decode()
        s.close()
        return res


if __name__ == "__main__":
    ServerCoordinator()
