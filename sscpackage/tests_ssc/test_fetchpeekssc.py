import unittest
import shelfpeekssc


class MyTestCase(unittest.TestCase):

    def test_shelfpeekssc(self):
        """
        Provides a hardcoded unit test for shelfpeekssc method
        :return:
        """
        testkeytrue = "KEYTEST1"
        testkeyfalse = "KEYFALSETEST"
        testpath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_shelfpeekssc'

        SHELFPEEKSSC = shelfpeekssc.FetchPeekSSC()
        testres1 = SHELFPEEKSSC.fetchpeek(path=testpath, keysearch=testkeytrue)
        self.assertTrue(testres1)
        testres2 = SHELFPEEKSSC.fetchpeek(path=testpath, keysearch=testkeyfalse)
        self.assertFalse(testres2)


if __name__ == '__main__':
    unittest.main()
