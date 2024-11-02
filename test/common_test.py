from pytest import fixture
from src.common import File, Item, Server


def test_file() -> None:
    assert File.Book.value == "books"
    assert File.Movie.value == "movies"
    assert File.Coord.value == "coord"


@fixture
def item() -> Item:
    return Item(File.Book, "Test Book", 1, 20.0)


def test_get_item(item: Item) -> None:
    assert item.get_type() == File.Book
    assert item.get_name() == "Test Book"
    assert item.get_quantity() == 1
    assert item.get_price() == 20.00
    assert item.get_tax() == 0.10
    assert item.get_result() == 22.00
    assert item.__str__() == "Test Book,1.0,20.0"


@fixture
def server() -> Server:
    return Server(8000, File.Book)


def test_server_runs(server: Server) -> None:
    assert (
        server.SERVER.__str__()
        == "<socket.socket fd=11, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8000)>"
    )


def test_server_save_file(server: Server, item: Item) -> None:
    server.save_file(item)
    data: list[Item] = server.get_file(File.Book)
    assert item.__str__() == data[-1].__str__()
