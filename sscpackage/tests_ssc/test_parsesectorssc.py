import unittest
import parsesectorssc
import shelve


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
    def test_parsesectorssc(self):

        test_parsesectorsscdatapath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_parse_sector.json'
        test_parsesectoruniquename = 'Test1__Test2__Test3__Test4'
        PSEC = parsesectorssc.ParseSector()

        quickdeleteop(PSEC.setpathssc_parsesscsec)

        self.assertFalse(shelveexist(PSEC.setpathssc_parsesscsec))

        with open(test_parsesectorsscdatapath) as fd:
            PSEC.parsesector(test_parsesectoruniquename, fd.read())
            fd.close()

        with shelve.open(PSEC.setpathssc_parsesscsec) as secshelf:
            for key in secshelf.keys():
                if test_parsesectoruniquename == key:
                    testvaluetwoind = True
                    break
                else:
                    testvaluetwoind = False
            secshelf.close()

        self.assertTrue(testvaluetwoind)

        quickdeleteop(PSEC.setpathssc_parsesscsec)
        self.assertFalse(shelveexist(PSEC.setpathssc_parsesscsec))

        del PSEC


def test_fetch_parsesectorssc(self):
    test_parsesectimestampid = 'Test4'
    test_parsesectorsscdatapath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_parse_sector.json'
    test_parsesectoruniquename = 'Test1__Test2__Test3__Test4'

    PSEC = parsesectorssc.ParseSector()
    with shelve.open(PSEC.setpathssc_parsesscsec) as fd:
        for key in fd:
            del fd[key]
        fd.close()

    with shelve.open(PSEC.setpathssc_parsesscsec) as fd:
        if fd.keys():
            testfetchvaloneparse = True
        else:
            testfetchvaloneparse = False

        self.assertFalse(testfetchvaloneparse)
        fd.close()

    with open(test_parsesectorsscdatapath) as fileopen:
        PSEC.parsesector(test_parsesectoruniquename, fileopen.read())
        fileopen.close()

    testvalparsesectwo = PSEC.fetch_parsesector(test_parsesectimestampid)
    testvalparsesectortwoanswer = 'Technology'
    self.assertEqual(testvalparsesectwo, testvalparsesectortwoanswer)

    with shelve.open(PSEC.setpathssc_parsesscsec) as fd:
        for key in fd.keys():
            del fd[key]
        fd.close()


if __name__ == '__main__':
    unittest.main()
