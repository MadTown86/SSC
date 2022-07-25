dictpullsscflag = False
count = 0

def dictpull(seq, header):
    """
    Dictpull takes a container as an argument and the name of the key you want to pull.  This only works for a 'key': 'value
    pair from a complex, nested sequence.

    :param seq: (This is a nested array that can contain any combination of dict, list, set or tuple.
    :param header: (key of the 'key':'value' pair you want to pull information for from a nested array
    :return: seq[header] = value is what is returned.
    """
    dictpull.answer = None
    global dictpullsscflag

    if not seq:
        return [seq]
    else:
        if not isinstance(seq, str):
            if isinstance(seq, dict):
                for key_index in range(len(seq.keys())):
                    if [x for x in seq.keys()][key_index] == header:
                        dictpull.answer = seq[header]
                        break
                    if isinstance(seq[[x for x in seq.keys()][key_index]], int):
                        continue
                    elif isinstance(seq[[x for x in seq.keys()][key_index]], str):
                        continue
                    elif isinstance(seq[[x for x in seq.keys()][key_index]], tuple):
                        continue

                    else:
                        pass
                    for recursivearg in dictpull(seq[[x for x in seq.keys()][key_index]], header):
                        continue

            elif isinstance(seq, set):
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
    if not dictpull.answer:
        return []
    else:
        return dictpull.answer


class DictPullSSC:
    def __init__(self):
        pass

    def dictpullssc(self, seq, header):
        dictpull(seq, header)
        self.answer = dictpull.answer
        return dictpull.answer

    def setanswerattr(self, answer):
        self.answer = answer

    def pullanswerattr(self):
        return self.answer



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





