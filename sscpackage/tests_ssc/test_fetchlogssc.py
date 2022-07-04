import unittest
import fetchlogssc

class TestFetchLog(unittest.TestCase):
    def test_fetchlogwrite(self):
        FS = fetchlogssc.FetchLogSSC()
        FS.ssc_fetchlogwrite("TEST")
        with open("../storage/fetchlog.txt", 'r') as fl:
            res = fl.readline()
            fl.close()
        self.assertEqual(res, "TEST")
        del FS

    def test_fetchlogclear(self):
        FS = fetchlogssc.FetchLogSSC()
        FS.ssc_fetchlogclear()
        with open("../storage/fetchlog.txt", 'r') as fl:
            res = fl.readline()
            fl.close()

        print(res)
        self.assertEqual("", res)


if __name__ == '__main__':
    unittest.main()
