import unittest
import gradeparsecombinessc

class myTestGradeParse(unittest.TestCase):
    def test_gradeparsecombinessc(self):
        testidgradeparsecombo = 'x1jU288DK5DRjWf'
        testtickergradeparsecombo = 'MSFT'
        testansone = ['MSFT__x1jU288DK5DRjWf']
        testanstwo = ['AR', 'baldat', 'incdat', 'Industry', 'Sector', 'valdat']
        GPD = gradeparsecombinessc.GradeParseCombineSSC()
        combocopy = GPD.gradeparsecombinessc(testtickergradeparsecombo, testidgradeparsecombo)
        testresone = [key for key in combocopy.keys()]
        print(testresone)
        testrestwo = [key for key in combocopy[testresone[0]].keys()]
        print(testrestwo)

        self.assertEqual(testresone, testansone)
        self.assertEqual(testrestwo, testanstwo)
