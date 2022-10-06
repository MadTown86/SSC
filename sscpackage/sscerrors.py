
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