from typing import Any

import json
import dotenv
import os

import dictpullssc

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")

dictpullsscflag = False
g_answer = None
count = 0

global returnlist
returnlist = []


def dictpull(seq: dict[str, Any], header: str) -> {}:
    global count
    global g_answer
    count += 1
    # TODO future - add an option to 'count' header until you get say the 3rd one in if repeat keys are an issue
    """
    Dictpull takes a container as an argument and the name of the key you want to pull.  This only works for a 'key': 'value
    pair from a complex, nested sequence.

    """
    global dictpullanswer
    global dictpullsscflag

    if g_answer:
        return g_answer
    else:
        if not seq:
            return []
        else:
            if not isinstance(seq, str):
                if isinstance(seq, dict):

                    if header in seq.keys():
                        g_answer = seq[header]
                        return g_answer

                    for key in seq.keys():
                        if g_answer:
                            return g_answer
                        if not isinstance(seq[key], int):
                            for rec1 in dictpull(seq[key], header):
                                return rec1

                elif isinstance(seq, set):
                    for element in seq:
                        if not isinstance(element, str):
                            if hasattr(element, "__iter__"):
                                for recset in dictpull(element, header):
                                    return recset


                elif isinstance(seq, tuple):
                    for element in seq:
                        if not isinstance(element, str):
                            if hasattr(element, "__iter__"):
                                for rectuple in dictpull(element, header):
                                    return rectuple

                elif isinstance(seq, int):
                    return []

                elif isinstance(seq, float):
                    return []

                elif isinstance(seq, list):
                    for index in range(len(seq)):
                        if not isinstance(seq[index], str):
                            if hasattr(seq[index], "__iter__"):
                                for reclist in dictpull(seq[index], header):
                                    return reclist

                else:
                    pass

    if g_answer:
        return g_answer
    else:
        return []


class DictPullSSC:
    answer = None

    def __init__(self) -> None:
        self.instancecount = 1
        DictPullSSC.purge_dictanswer()
        pass

    @staticmethod
    def purge_dictanswer():
        global g_answer
        g_answer = None
        DictPullSSC.answer = None

    def dictpullssc(self, seq: dict, header: str) -> {}:
        global g_answer
        dictpull(seq, header)
        return g_answer


    """
    if not DictPullSSC.answer:
        dictpull(seq, header)
    else:
        return DictPullSSC.answer

    """

    @staticmethod
    def setanswerattr(answer) -> None:
        DictPullSSC.answer = answer

    @staticmethod
    def pullanswerattr() -> dict:
        return DictPullSSC.answer


if __name__ == "__main__":
    testnest = {
        "LAYER 1": {
            "LAYER2-1": "VAL 2-1",
            "LAYER2-2": "VAL 2-2",
            "LAYER2-3": {
                "LAYER3-1": ["LAYER 4-LIST", "LAYER 4-2-LIST", {"LAYER5": "ANSWER"}]
            },
        }
    }

    testdict = {"LAYER1": "NOT IT", "LAYER2": {"NEXT LAYER": "FOUNDIT"}}

    simpletest = [
        "LL1",
        ["LL2", "LL3", ["LL4"]],
        ["LL5"],
        ["LL6", ["LL7", [{"LL8": "FOUND IT"}]]],
    ]

    complexdict = {
        "LAYER1D": "VALUE1D",
        "LAYER2D": {5, 6, 7},
        "LAYER3D": (88, 89, 90),
        "LAYER4D": [
            "L4LIST",
            "L4LIST2",
            {
                "LAYER4-A1": ["TRAVEL", 99, ["TERMINAL", "BOB", {"SETUP": 2}]],
                "LAYER4-A2": (30, 40, ["22", "25", 40], {"TRUE", "FALSE", "FAILED"}),
                "LAYER4-A3": {
                    "LAYER4-B1": [
                        "ABC",
                        "EFG",
                        (
                            "MARY",
                            "BILLY",
                            {
                                "lAYER4-B1-A1": [
                                    "THIS IS",
                                    "YOUR",
                                    {"ANSWER": {"YOU FOUND IT": "VALUE YOU FOUND"}},
                                ]
                            },
                        ),
                    ]
                },
            },
        ],
    }

    test_dictval = {
        "quarterlyMarketCap": [
            {
                "dataId": 40001,
                "asOfDate": "2021-09-30",
                "periodType": "3M",
                "reportedValue": {"raw": 947916270000, "fmt": "947.92B"},
                "nextvalue": [{"nestedfurther": 99}]
            }
        ]
    }

    fd = open(ROOT_VAR_SSC + "test_META_sector.json", "r")
    from_json = json.load(fd)

    test_raw = dictpull(test_dictval, "raw")
    print(f'RESULT: {list(test_raw)}')

"""
    DD = dictpullssc.DictPullSSC()
    DD1 = dictpullssc.DictPullSSC()

    test_dictvalres = dictpull(test_dictval, 'quarterlyMarketCap')
    print(test_dictvalres)
    DD.purge_dictanswer()

    testsec = DD.dictpullssc(from_json, 'sector')

    print("SECTOR")
    print(testsec)
    DD.purge_dictanswer()

    testind = DD1.dictpullssc(from_json, 'longBusinessSummary')

    print("INDUSTRY-->")
    print(testind)
    DD1.purge_dictanswer()


    print("LAYER5-->")
    print(DD.dictpullssc(testnest, "LAYER5"))
    DD.purge_dictanswer()
    print("LL8-->")
    print(DD1.dictpullssc(simpletest, "LL8"))
    DD1.purge_dictanswer()
    print("NEXT LAYER-->")
    print(DD.dictpullssc(testdict, "NEXT LAYER"))
    DD.purge_dictanswer()
    print("ANSWER-->")
    print(DD.dictpullssc(complexdict, "ANSWER"))
    DD.purge_dictanswer
"""