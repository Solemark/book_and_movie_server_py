from socket import socket
from typing import Any
from os import linesep
from movie import Movie


class MovieServer:
    def __init__(
        self, address: str = "localhost", port: int = 8002, connections: int = 5
    ) -> None:
        self.__ADDRESS: str = address
        self.__PORT: int = port
        self.__CONNECTIONS: int = connections
        self.__movies: list[Movie] = self.__get_movies()

        self.__SERVER = socket()
        self.__SERVER.bind((self.__ADDRESS, self.__PORT))
        self.__SERVER.listen(self.__CONNECTIONS)

        print(f"Listening on {self.__ADDRESS}:{self.__PORT}")

        self.__run_server()

    def __run_server(self) -> None:
        """Run the Movie Server"""
        while True:
            sock, addr = self.__SERVER.accept()
            print(f"Incoming message from {addr}")

            m: list[str] = sock.recv(1024).decode().split(",")
            res: bool = self.__save_movies(Movie(m[0], float(m[1]), float(m[2])))

            sock.send(
                "Book saved successfully!".encode()
                if res
                else "Book failed to save!".encode()
            )
            sock.close()

    def __get_movies(self) -> list[Movie]:
        """Get the list of movies from file"""
        f: Any = open("data/movies.csv").readlines()
        movies: list[Movie] = []
        for d in f:
            m: list[str] = d.split(",")
            movies.append(Movie(m[0], float(m[1]), float(m[2])))
        return movies

    def __save_movies(self, m: Movie) -> bool:
        """Save the Movie list"""
        try:
            self.__movies.append(m)
            f: Any = open("data/movies.csv", "w")
            for movie in self.__movies:
                f.write(movie.__str__() + linesep)
            return True
        except Exception:
            return False


if __name__ == "__main__":
    MovieServer()
