from typing import Any

dictpullsscflag = False
count = 0


def dictpull(seq: dict[str, Any], header: str) -> {}:
    # TODO future - add an option to 'count' header until you get say the 3rd one in if repeat keys are an issue
    """
    Dictpull takes a container as an argument and the name of the key you want to pull.  This only works for a 'key': 'value
    pair from a complex, nested sequence.

    :param seq: (This is a nested array that can contain any combination of dict, list, set or tuple.
    :param header: (key of the 'key':'value' pair you want to pull information for from a nested array
    :return: seq[header] = value is what is returned.
    """
    global dictpullanswer
    global dictpullsscflag

    print(f'HEADER::: {header}')
    print(f'SEQUENCE::: {seq}')
    print(f'TYPE:: {type(seq)}')

    # Front Door Gate
    if DictPullSSC.answer:
        return DictPullSSC.answer

    if not seq:
        return [seq]
    else:
        if not isinstance(seq, str):
            if isinstance(seq, dict):
                print(f'KEY SEQUENCE:  {[x for x in seq.keys()]}')
                if header in seq.keys():
                    print("IN KEYLIST - HEADER")
                    print(f'SEQ[HEADER]:: {seq[header]}')
                    DictPullSSC.setanswerattr(seq[header])
                    return []
                for key_index in range(len(seq.keys())):
                    if [x for x in seq.keys()][key_index] == header:
                        DictPullSSC.setanswerattr(seq[header])
                        break
                    if isinstance(seq[[x for x in seq.keys()][key_index]], int):
                        continue
                    elif isinstance(seq[[x for x in seq.keys()][key_index]], str):
                        continue
                    elif isinstance(seq[[x for x in seq.keys()][key_index]], tuple):
                        continue
                    if seq[[x for x in seq.keys()][key_index]]:
                        for recursivearg in dictpull(seq[[x for x in seq.keys()][key_index]], header):
                            continue
                    else:
                        pass

            elif isinstance(seq, set):
                print("IN SET")
                for element in seq:
                    if not isinstance(element, str):
                        if hasattr(element, '__iter__'):
                            for recursesetarg in dictpull(element, header):
                                continue
                        else:
                            continue
                    else:
                        continue

            elif isinstance(seq, tuple):
                for element in seq:
                    if not isinstance(element, str):
                        if hasattr(element, "__iter__"):
                            for tuplevar in dictpull(element, header):
                                continue
                        else:
                            continue
                    else:
                        continue

            elif isinstance(seq, int):
                pass

            elif isinstance(seq, float):
                pass

            else:
                for element in range(len(seq)):
                    if not isinstance(seq[element], str):
                        if hasattr(seq[element], '__iter__'):
                            for recursiveargnotstring in dictpull(seq[element], header):
                                continue
                        else:
                            continue
                    else:
                        continue
        else:
            pass

    # Backdoor gate
    if not DictPullSSC.answer:
        return []
    else:
        return DictPullSSC.pullanswerattr()


class DictPullSSC:
    answer = None

    def __init__(self) -> None:
        DictPullSSC.purge_dictanswer()
        pass

    @staticmethod
    def purge_dictanswer():
        DictPullSSC.answer = None

    def dictpullssc(self, seq: dict, header: str) -> {}:
        print("BACK TO ORIGIN LOCATION")
        print(f'SEQ: {seq}')
        print(f'DICTPULL.ANSWER:::{DictPullSSC.answer}')
        if not DictPullSSC.answer:
            dictpull(seq, header)
        else:
            return DictPullSSC.answer

    @staticmethod
    def setanswerattr(answer) -> None:
        DictPullSSC.answer = answer

    @staticmethod
    def pullanswerattr() -> dict:
        return DictPullSSC.answer


if __name__ == "__main__":
    testnest = {"LAYER 1":
                    {"LAYER2-1": "VAL 2-1", "LAYER2-2": "VAL 2-2", "LAYER2-3":
                        {"LAYER3-1":
                             ["LAYER 4-LIST", "LAYER 4-2-LIST",
                              {"LAYER5": "ANSWER"}
                              ]
                         }
                     }
                }

    testdict = {"LAYER1": "NOT IT", "LAYER2": {"NEXT LAYER": "FOUNDIT"}}

    simpletest = ["LL1", ["LL2", "LL3", ["LL4"]], ["LL5"], ["LL6", ["LL7", [{"LL8": "FOUND IT"}]]]]

    complexdict = {
        "LAYER1D": "VALUE1D",
        "LAYER2D": {5, 6, 7},
        "LAYER3D": (88, 89, 90),
        "LAYER4D": ["L4LIST", "L4LIST2", {
            "LAYER4-A1": ["TRAVEL", 99, ["TERMINAL", "BOB", {"SETUP": 2}]],
            "LAYER4-A2": (30, 40, ["22", "25", 40], {"TRUE", "FALSE", "FAILED"}),
            "LAYER4-A3": {
                "LAYER4-B1": ["ABC", "EFG", ("MARY", "BILLY", {
                    "lAYER4-B1-A1": ["THIS IS", "YOUR", {"ANSWER": {"YOU FOUND IT": "VALUE YOU FOUND"}}]
                })]
            }
        }]
    }

    DD = DictPullSSC()
    DD1 = DictPullSSC()
    print(DD.dictpullssc(testnest, "LAYER5"))
    print(DD1.dictpullssc(simpletest, "LL8"))
    print(DD.dictpullssc(testdict, "NEXT LAYER"))
    print(DD.dictpullssc(complexdict, "ANSWER"))
