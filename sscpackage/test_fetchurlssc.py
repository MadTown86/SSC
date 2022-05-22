import unittest
from unittest.mock import patch
from unittest.mock import call
import shelve

import sscpackage.fetchurlssc
from sscpackage.fetchurlssc import FetchUrlSSC as FSSC


def dictprinter(d):
    for key in d.keys():
        labelr = "This is KEY: %s,  This is VALUE: %s" % (key, d[key])
        print(labelr)
    return

class Test_FetchRulSSC(unittest.TestCase):
    @patch('os.path.exists')
    def test_checkpaths(self, mock_os_path_exists):
        test_callarglist = [call("fetchurlshelfdb.bak"), call("fetchurlshelfdb.dat"), call("fetchurlshelfdb.dir")]
        LocalFetchClassInstance = FSSC()
        LocalFetchClassInstance.checkpaths()
        mock_os_path_exists.assert_has_calls(test_callarglist, mock_os_path_exists.call_args_list)
        self.assertEqual(True, LocalFetchClassInstance.checkpaths())

        del LocalFetchClassInstance, test_callarglist

    def test_fetchshelfinitialize(self):
        """
        Having trouble using a mock with shelve, going to have to actually access shelf to see values and make sure
        method initializes the fetch url dictionary
        :return:
        """

        FSSC1 = sscpackage.fetchurlssc.FetchUrlSSC()
        FSSC1.fetchshelfinitialize()
        with shelve.open(FSSC1.pathnamefetchurls) as test_fd:
            tempbank_testfsi = test_fd[FSSC1.shelfkey]
            self.assertEqual(str(tempbank_testfsi), str(FSSC1.fetch_apidict))
            test_fd.close()
        del FSSC1


    def test_addfetchssc(self):

        FSSC2 = sscpackage.fetchurlssc.FetchUrlSSC()
        FSSC2.addfetchssc()
        with shelve.open(FSSC2.pathnamefetchurls) as testadd_fd:
            tempbank_testadd = dict(testadd_fd[FSSC2.shelfkey])
            dictprinter(tempbank_testadd)
            default_valueassert = False
            if FSSC2.addfetchnamessc in tempbank_testadd.keys():
                default_valueassert = True
            else:
                pass
            testadd_fd.close()

        self.assertEqual(default_valueassert, True)







if __name__ == '__main__':
    unittest.main()
