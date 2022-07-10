class FetchLogSSC:
    def __init__(self):
        self.fetchlogpath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\fetchlog.txt'


    def ssc_fetchlogwrite(self, fetchstorename):
        with open(self.fetchlogpath, 'w') as fl:
            fl.write(fetchstorename)

            fl.close()

    def ssc_fetchlogclear(self):
        with open(self.fetchlogpath, 'w') as fl2:
            fl2.truncate()
            fl2.close()

    def ssc_logfetch(self):
        logfetch_retval = []
        with open(self.fetchlogpath, 'r') as fl3:
            for logentry in fl3.readlines():
                logfetch_retval.append(logentry)

            fl3.close()
        return logfetch_retval