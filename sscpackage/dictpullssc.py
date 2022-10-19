from typing import Any

import json
import dotenv
import os

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")

dictpullsscflag = False
g_answer = None
count = 0


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

    if not seq:
        return []
    else:
        if not isinstance(seq, str):
            if isinstance(seq, dict):
                if header in seq.keys():
                    g_answer = seq[header]
                    return g_answer

                for key in seq.keys():
                    if not isinstance(seq[key], str):
                        if hasattr(seq[key], "__iter__"):
                            dictpull(seq[key], header)

            elif isinstance(seq, set):
                for element in seq:
                    if not isinstance(element, str):
                        if hasattr(element, "__iter__"):
                            dictpull(element, header)

            elif isinstance(seq, tuple):
                for element in seq:
                    if not isinstance(element, str):
                        if hasattr(element, "__iter__"):
                            dictpull(element, header)

            elif isinstance(seq, int):
                pass

            elif isinstance(seq, float):
                pass

            else:
                for element in range(len(seq)):
                    if not isinstance(seq[element], str):
                        if hasattr(seq[element], "__iter__"):
                            dictpull(seq[element], header)

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
        DictPullSSC.answer = None

    def dictpullssc(self, seq: dict, header: str) -> {}:
        return dictpull(seq, header)

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

    test_actual_valjson = {
        "trailingEnterprisesValueEBITDARatio": [
            {
                "dataId": 102,
                "asOfDate": "2022-10-06",
                "periodType": "TTM",
                "reportedValue": {"raw": 7.267784, "fmt": "7.27"},
            }
        ]
    }

    fd = open(ROOT_VAR_SSC + "test_META_sector.json", "r")
    from_json = json.load(fd)

    DD = DictPullSSC()
    DD1 = DictPullSSC()

    print(DD.dictpullssc(test_actual_valjson, "raw"))
    testsec = DD.dictpullssc(from_json, "sector")
    print(testsec)

    testind = DD1.dictpullssc(from_json, "longBusinessSummary")

    print(testind)

    print(DD.dictpullssc(testnest, "LAYER5"))
    print(DD1.dictpullssc(simpletest, "LL8"))
    print(DD.dictpullssc(testdict, "NEXT LAYER"))
    print(DD.dictpullssc(complexdict, "ANSWER"))
