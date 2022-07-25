class FetchLogSSC:
    def __init__(self):
        self.fetchlogpath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\fetchlog.txt'


    def ssc_fetchlogwrite(self, fetchstorename):
        with open(self.fetchlogpath, 'a') as fl:
            fl.seek(0, 2)
            fl.write(fetchstorename+", ")
            fl.close()

    def ssc_fetchlogclear(self):
        with open(self.fetchlogpath, 'w') as fl2:
            fl2.truncate()
            fl2.close()

    def ssc_logfetch(self):
        logfetch_retval = []
        with open(self.fetchlogpath, 'r') as fl3:
            fl3.seek(0, 0)
            data = fl3.read().split(", ")
            for logentry in data:
                logfetch_retval.append(logentry)
            fl3.close()
        return logfetch_retval