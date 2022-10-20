"""
Some helper funcs for unittest.mock
"""
import unittest.mock


def testmock_print(mck: unittest.mock.MagicMock, header: str) -> None:
    listofprints = {
        "CALLED: ": mck.called,
        "CALL COUNT: ": mck.call_count,
        "CALL ARGS: ": mck.call_args,
        "CALL ARGS LIST: ": mck.call_args_list,
        "METHOD CALLS: ": mck.method_calls,
        "MOCK CALLS: ": mck.mock_calls,
    }

    headerblock = "\n" + " " + header + " " + " \n"
    print(headerblock)
    for key in listofprints.keys():
        print(f"{key}")
        if listofprints[key]:
            print(listofprints[key])
