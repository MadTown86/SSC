import shelve
import dotenv
import os
dotenv.load_dotenv(dotenv_path=r'C:\SSC\SimpleStockChecker_REV1\venv\.env')
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')


class FetchLogSSC:
    _fetchlogpath = ROOT_VAR_SSC + "fetchlog"
    @staticmethod
    def ssc_fetchlogclear():
        with shelve.open(FetchLogSSC._fetchlogpath) as flc:
            if flc.keys():
                for key in flc:
                    del flc[key]
            if flc.keys():
                return 0
            else:
                return 1

    def __init__(self):
        self.logname = "fetchlog"
        self.logfinish = "fetchlogfinished"
        pass

    def ssc_fetchlogwrite(self, fetchstorename):
        #Put in Store
        with shelve.open(FetchLogSSC._fetchlogpath) as shelvelog:
            if shelvelog.keys():
                if self.logname in shelvelog.keys():
                    temp_log = list(shelvelog[self.logname])
                    if fetchstorename not in temp_log:
                        temp_log.append(fetchstorename)
                        shelvelog[self.logname] = temp_log
            else:
                temp_log = []
                temp_log.append(fetchstorename)
                shelvelog[self.logname] = [x for x in temp_log]


    def ssc_logfetch(self):
        with shelve.open(FetchLogSSC._fetchlogpath) as fl3:
            if fl3.keys():
                if fl3[self.logname]:
                    return fl3[self.logname]
                else:
                    return 0

    def ssc_logcompletewrite(self, ticker, uniqueid):
        transfer_tocomplete = []
        with shelve.open(FetchLogSSC._fetchlogpath) as fl4:
            if fl4.keys():
                if fl4[self.logname]:
                    log_listlocal = fl4[self.logname]
                    for indexno in range(len(log_listlocal-1)):
                        if ticker and uniqueid in log_listlocal[indexno]:
                            print(log_listlocal[indexno])
                            transfer_tocomplete.append(log_listlocal.pop(log_listlocal[indexno]))
                        else:
                            continue
            if transfer_tocomplete:
                if self.logfinish not in fl4.keys():
                    fl4[self.logfinish] = transfer_tocomplete
                else:
                    tempcopy = fl4[self.logfinish]
                    for item in transfer_tocomplete:
                        if item not in tempcopy:
                            tempcopy.append(item)
                    fl4[self.logfinish] = tempcopy






if __name__ == "__main__":



    FLOG2 = FetchLogSSC()
    printoutput = FLOG2.ssc_logfetch()
    for line in printoutput:
        print(line)






