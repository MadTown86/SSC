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
        pass

    def ssc_fetchlogwrite(self, fetchstorename):
        #Put in Store
        with shelve.open(FetchLogSSC._fetchlogpath) as shelvelog:
            if shelvelog.keys():
                if self.logname in shelvelog.keys():
                    temp_log = list(shelvelog[self.logname])
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

