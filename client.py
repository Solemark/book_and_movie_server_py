from socket import socket


class Client:
    def __init__(self) -> None:
        while True:
            print("\n".join(self.client_prompt()))
            res: str = input("Enter your option: ")
            msg: str = ""
            match res:
                case "1":
                    msg = f"B,{self.get_details('book')}"
                case "2":
                    msg = f"M,{self.get_details('movie')}"
                case _:
                    exit(0)
            self.send_message(msg)

    def client_prompt(self) -> list[str]:
        """get the client prompt"""
        return [
            "**************************************",
            "Place your order by selecting a number",
            "**************************************",
            "1. Purchase book",
            "2. Purchase movie",
            "Press any other key to exit",
            "**************************************",
        ]

    def get_details(self, t: str) -> str:
        """Get the (type) details and compose for serialization"""
        print(f"Enter {t} details:")
        return f"{input(f'Enter {t} name: ')},{input(f'Enter {t} quantity: ')},{input(f'Enter {t} price: ')}"

    def send_message(self, msg: str) -> None:
        """Encode then send the message. Await a response"""
        s: socket = socket()
        s.connect(("localhost", 8000))
        s.send(msg.encode())
        res = s.recv(1024).decode()
        print(res)
        s.close()


if __name__ == "__main__":
    Client()
