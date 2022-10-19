import unittest

import shelverssc

import dotenv
import os

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")


class MyTestCase(unittest.TestCase):
    def test_shelfpeekssc(self):
        """
        Provides a hardcoded unit test for shelfpeekssc method
        :return:
        """
        testkeytrue = "KEYTEST1"
        testkeyfalse = "KEYFALSETEST"
        testpath = ROOT_VAR_SSC + "test_shelfpeekssc"

        SHELFPEEKSSC = shelverssc.ShelverSSC()
        testres1 = SHELFPEEKSSC.fetchpeek(path=testpath, keysearch=testkeytrue)
        self.assertTrue(testres1)
        testres2 = SHELFPEEKSSC.fetchpeek(path=testpath, keysearch=testkeyfalse)
        self.assertFalse(testres2)


if __name__ == "__main__":
    unittest.main()
