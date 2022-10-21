"""Example from Muumi
class EmptyDictException(Exception):

    pass


def get_keys(dct: dict) -> list:
    if dct:
        return list(dct.keys())
    else:
        # dct was empty
        raise EmptyDictException


def func(dct: dict) -> None:
    print(f"executing func({dct})")
    try:
        result = get_keys(dct)
    except EmptyDictException:
        print("handled an error")
    else:
        print(result)


func({"a": 1})
func({})
"""
import shelve


def get_keysshelve(shelver: shelve) -> list:
    if shelver:
        return list(shelver.keys())
    else:
        # shelver was empty
        raise EmptyShelveException


def gotmilk(dat):
    if dat:
        return True
    else:
        raise GotNoMilk


class AlreadyExistsException(Exception):
    pass

class GotNoMilk(Exception):
    print("It's Got No Milk, Buddy!")
    pass


class NoShelveException(Exception):
    pass


class EmptyDataFetch(Exception):
    pass


class EmptyShelveException(Exception):
    """Raised when a dict is empty"""

    pass


class SqlParseException(Exception):
    """Raised when there is a problem parsing SQL using mysql.connector"""

    pass
