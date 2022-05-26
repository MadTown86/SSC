import unittest
import sscpackage.dictpullssc as dps

testnest = {"LAYER 1":
                {"LAYER2-1": "VAL 2-1", "LAYER2-2": "VAL 2-2", "LAYER2-3":
                    {"LAYER3-1":
                         ["LAYER 4-LIST", "LAYER 4-2-LIST",
                          {"LAYER5": "ANSWER"}
                          ]
                     }
                 }
            }

testnest_request = "LAYER5"
testnest_answer = "ANSWER"

testdict = {"LAYER1": "NOT IT", "LAYER2": {"NEXT LAYER": "FOUNDIT"}}
testdict_request = "NEXT LAYER"
testdict_answer = "FOUNDIT"

simpletest = ["LL1", ["LL2", "LL3", ["LL4"]], ["LL5"], ["LL6", ["LL7", [{"LL8": "FOUND IT"}]]]]
simpletest_request = "LL8"
simpletest_answer = "FOUND IT"


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
complexdict_request = "ANSWER"
complexdict_answer = {"YOU FOUND IT": "VALUE YOU FOUND"}


class MyTestCase(unittest.TestCase):
    """
    Test for dictpullssc.
    """
    def setUp(self):
        self.dictp = dps.DictPullSSC()

    def test_testnest(self):
        self.assertEqual(testnest_answer, self.dictp.dictpullssc(testnest, testnest_request))

    def test_simpletest(self):
        self.assertEqual(simpletest_answer, self.dictp.dictpullssc(simpletest, simpletest_request))

    def test_testdict(self):
        self.assertEqual(testdict_answer, self.dictp.dictpullssc(testdict, testdict_request))

    def test_complexdict(self):
        self.assertEqual(complexdict_answer, self.dictp.dictpullssc(complexdict, complexdict_request))

    def tearDown(self):
        del(self.dictp)

if __name__ == '__main__':
    unittest.main()
