class FetchLogSSC:
    def __init__(self):
        pass

    def ssc_fetchlogwrite(self, fetchstorename):
        with open("fetchlog.txt", 'w') as fl:
            fl.write(fetchstorename)

            fl.close()

    def ssc_fetchlogclear(self):
        with open("fetchlog.txt", 'w') as fl2:
            fl2.truncate()
            fl2.close()

    def ssc_logfetch(self):
        logfetch_retval = []
        with open("fetchlog.txt", 'r') as fl3:
            for logentry in fl3.readlines():
                logfetch_retval.append(logentry)

            fl3.close()
        return logfetch_retval