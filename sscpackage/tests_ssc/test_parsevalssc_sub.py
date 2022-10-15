import unittest
from unittest.mock import patch
import parsevalssc_sub
import json
import test_helperfuncs_ssc as hpr

import os
import dotenv
dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')


import sscpackage.fetchshelfssc_mod


class Test_ParseValSub(unittest.TestCase):
    mock_passin = unittest.mock.MagicMock

    @patch("parsevalssc_sub.fetchshelfssc_mod.FetchShelfSSC")
    def test_parseval(self, Mock_FetchSSC):
        with open(ROOT_VAR_SSC + 'test_META_val.json', 'r') as fd:
            test_passin = json.load(fd)

        print(test_passin)
        PSUB = parsevalssc_sub.ParseValSSC_Sub()
        PSUB.parseval("TEST__TEST__TEST__TEST", test_passin)

        Mock_FetchSSC()

        #print(Mock_FetchSSC.called)
        #print(Mock_FetchSSC.call_args_list)

        #print(Mock_FetchSSC.return_value.call_args)

        #hpr.testmock_print(Mock_FetchSSC, 'Mock_Fetch')


if __name__ == '__main__':
    unittest.main()
