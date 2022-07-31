import unittest
import shelfpullssc



class MyTestCase(unittest.TestCase):
    def test_shelfpullssc(self):
        pathtoshelve = 'C:\\SSC\\SimpleStockChecker_REV1\\sscpackage\\storage\\testshelvessc'

        first_resssc = {'First Key': {'FK1': 'FV1', 'FK2': 'FV2'}, 'Second Key': {'FK22': 'FV22', 'FK23': 'FV23'}}
        second_resssc = ['First Key', 'Second Key']
        third_resssc = {'FK1': 'FV1', 'FK2': 'FV2'}
        keyfortestssc = 'First Key'

        SV = shelfpullssc.ShelfPullSSC()
        self.assertEqual(SV.pullshelfssc(pathtoshelve), first_resssc)
        self.assertEqual(SV.pullshelfkeylistssc(pathtoshelve), second_resssc)
        self.assertEqual(SV.pullvalueinshelfssc(pathtoshelve, keyfortestssc), third_resssc)


if __name__ == '__main__':
    unittest.main()
