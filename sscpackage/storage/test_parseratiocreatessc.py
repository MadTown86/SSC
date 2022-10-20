import unittest
import parseratiocreatessc
import parseincomessc
import parsebalancessc

def quickdictprint(dict):
    for key, value in dict.items():
        print(f'KEY: {key} >>> VALUE: {value}')
    return dict

class ParseRatioCreate(unittest.TestCase):
    def test_parseratiocreatessc(self):
        PS = parsebalancessc.ParseBalance()
        IS = parseincomessc.ParseIncome()

        keytest = PS.parse_shelvepullkeys()[0].split("__")[2]

        PRC = parseratiocreatessc.ParseRatioCreateSSC()

        PRC.parseratiocreatesssc(quickdictprint(IS.fetch_parseincome(keytest)),
                                 quickdictprint(PS.fetch_parsebalance(keytest)))

        parseratiodict = PRC.parseratiocreatesssc(IS.fetch_parseincome(keytest), PS.fetch_parsebalance(keytest))
        quickdictprint(parseratiodict)

if __name__ == '__main__':
    unittest.main()
