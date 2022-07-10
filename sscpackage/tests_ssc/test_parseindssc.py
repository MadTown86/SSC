import unittest
import shelve
import parseindssc

def quickdeleteop(path):
    with shelve.open(path) as funcdelshelf:
        for key in funcdelshelf.keys():
            del funcdelshelf[key]
        funcdelshelf.close()

def shelveexist(path):
    with shelve.open(path) as funcshelf:
        if funcshelf.keys():
            return True
        else:
            return False

class MyTestCase(unittest.TestCase):
    def test_parseindustry(self):
        test_parseindustrydatapath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_parse_sector.json'
        test_parseinduniquename = 'Test1__Test2__Test3__Test4'
        PIND = parseindssc.ParseIndustry()

        quickdeleteop(PIND.setpathssc_parsesscind)

        self.assertFalse(shelveexist(PIND.setpathssc_parsesscind))

        with open(test_parseindustrydatapath) as fd:
            PIND.parseindustry(test_parseinduniquename, fd.read())
            fd.close()

        with shelve.open(PIND.setpathssc_parsesscind) as indshelf:
            for key in indshelf.keys():
                if test_parseinduniquename == key:
                    testvaluetwoind = True
                    break
                else:
                    testvaluetwoind = False
            indshelf.close()

        self.assertTrue(testvaluetwoind)

        quickdeleteop(PIND.setpathssc_parsesscind)
        self.assertFalse(shelveexist(PIND.setpathssc_parsesscind))

        del PIND

    def test_fetch_parseindustry(self):
        test_parseindtimestampid = 'Test4'
        test_parseindustrydatapath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_parse_sector.json'
        test_parseinduniquename = 'Test1__Test2__Test3__Test4'

        PIND = parseindssc.ParseIndustry()
        with shelve.open(PIND.setpathssc_parsesscind) as fd:
            for key in fd:
                del fd[key]
            fd.close()

        with shelve.open(PIND.setpathssc_parsesscind) as fd:
            if fd.keys():
                testfetchvaloneparse = True
            else:
                testfetchvaloneparse = False

            self.assertFalse(testfetchvaloneparse)
            fd.close()

        with open(test_parseindustrydatapath) as fileopen:
            PIND.parseindustry(test_parseinduniquename, fileopen.read())
            fileopen.close()

        testvalparseindtwo = PIND.fetch_parseindustry(test_parseindtimestampid)
        testvalparseindtwoanswer = 'Software—Infrastructure'
        self.assertEqual(testvalparseindtwo, testvalparseindtwoanswer)

        with shelve.open(PIND.setpathssc_parsesscind) as fd:
            for key in fd.keys():
                del fd[key]
            fd.close()



if __name__ == '__main__':
    unittest.main()
