import shelve
import dotenv
import os
import time

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")


class FetchLogSSC:
    _fetchlogpath = ROOT_VAR_SSC + "fetchlog"

    @staticmethod
    def ssc_fetchlogclear():
        try:
            with shelve.open(FetchLogSSC._fetchlogpath) as flc:
                if flc.keys():
                    for key in flc:
                        del flc[key]
                if flc.keys():
                    return 0
                else:
                    return 1
        except Exception as er:
            print("Exception in fetchlogssc -> ssc_fetchlogclear")
            print(er)

    def __init__(self):
        self.logname = "fetchlog"
        self.logfinish = "fetchlogfinished"
        self.logdelete = "fetchlogdeleted"

    def ssc_fetchlogwrite(self, fetchstorename):
        # Put in Store
        try:
            with shelve.open(FetchLogSSC._fetchlogpath) as shelvelog:
                if shelvelog.keys():
                    if self.logname in shelvelog.keys():
                        temp_log = shelvelog[self.logname]
                        if fetchstorename not in temp_log:
                            temp_log.append(fetchstorename)
                            shelvelog[self.logname] = temp_log
                        else:
                            pass
                    else:
                        shelvelog[self.logname] = [fetchstorename]
                else:
                    shelvelog[self.logname] = [fetchstorename]
        except Exception as er:
            print("Exception in fetchlogssc -> ssc_fetchlogwrite")
            print(er)

    def ssc_logfetch(self):
        try:
            with shelve.open(FetchLogSSC._fetchlogpath) as fl3:
                if fl3.keys():
                    if self.logname in fl3.keys():
                        return fl3[self.logname]
                    else:
                        fl3[self.logname] = []
                        return fl3[self.logname]
                fl3[self.logname] = []
                return fl3[self.logname]
        except Exception as er:
            print("Exception in fetchlogssc -> ssc_logfetch")
            print(er)

    def ssc_logcompletewrite(self, ticker, uniqueid):
        try:
            transfer_tocomplete = []
            with shelve.open(FetchLogSSC._fetchlogpath) as fl4:
                if fl4.keys():
                    if fl4[self.logname]:
                        log_listlocal = [x for x in fl4[self.logname]]
                        for indexno in range(len(log_listlocal) - 1):
                            if ticker and uniqueid in log_listlocal[indexno]:
                                print(log_listlocal[indexno])
                                transfer_tocomplete.append(log_listlocal.pop(indexno))
                            else:
                                continue
                        fl4[self.logname] = log_listlocal

                if transfer_tocomplete:
                    if self.logfinish not in fl4.keys():
                        fl4[self.logfinish] = transfer_tocomplete
                    else:
                        tempcopy = fl4[self.logfinish]
                        for item in transfer_tocomplete:
                            if item not in tempcopy:
                                tempcopy.append(item)
                        fl4[self.logfinish] = tempcopy
        except Exception as er:
            print("Exception in fetchlogssc -> ssc_logcompletewrite")
            print(er)

    def ssc_fetchlogdeleted(self, ticker, uniqueid):
        try:
            transfer_todelete = []
            with shelve.open(FetchLogSSC._fetchlogpath) as fl4:
                if fl4.keys():
                    if fl4[self.logname]:
                        log_listlocal = [x for x in fl4[self.logname]]
                        log_listdel = log_listlocal[:]
                        print(f"LOG LIST LOCAL - ssc_fetchlog: {log_listlocal}")
                        for indexno in range(len(log_listlocal) - 1):
                            print(indexno)
                            if ticker and uniqueid in log_listlocal[indexno]:
                                print(log_listlocal[indexno])
                                transfer_todelete.append(
                                    log_listdel.pop(
                                        log_listdel.index(log_listlocal[indexno])
                                    )
                                )
                            else:
                                continue
                        fl4[self.logname] = log_listdel

                if transfer_todelete:
                    if self.logdelete not in fl4.keys():
                        fl4[self.logdelete] = transfer_todelete
                    else:
                        tempcopy = fl4[self.logdelete]
                        for item in transfer_todelete:
                            if item not in tempcopy:
                                tempcopy.append(item)
                        fl4[self.logfinish] = tempcopy
        except Exception as er:
            print("Exception in fetchlogssc -> ssc_fetchlogdeleted")
            print(er)

    def ssc_logdelete_testadd(self, value):
        try:
            with shelve.open(FetchLogSSC._fetchlogpath) as fl8:
                if fl8.keys():
                    if self.logdelete in fl8.keys():
                        if fl8[self.logdelete]:
                            temp_list = fl8[self.logdelete]
                            temp_list.append(value)
                            fl8[self.logdelete] = temp_list
                        else:
                            fl8[self.logdelete] = value
                    else:
                        fl8[self.logdelete] = value
                else:
                    fl8[self.logdelete] = value

        except Exception as er:
            print("Exception in fetchlogssc -> ssc_logdelete_testadd")
            print(er)

    def ssc_logdelete_fetch(self):
        try:
            with shelve.open(FetchLogSSC._fetchlogpath) as fl6:
                if fl6.keys():
                    if self.logdelete in fl6.keys():
                        return fl6[self.logdelete]
                    else:
                        fl6[self.logdelete] = []
                        return fl6[self.logdelete]
                else:
                    fl6[self.logdelete] = []
                    return fl6[self.logdelete]

        except Exception as er:
            print("Exception in fetchlogssc -> ssc_logdeletefetch")
            print(er)

    def ssc_logdelete_purge(self):
        try:
            with shelve.open(FetchLogSSC._fetchlogpath) as fl7:
                if fl7.keys():
                    if fl7[self.logdelete]:
                        del fl7[self.logdelete]
                        fl7[self.logdelete] = []
                    if fl7[self.logdelete]:
                        return 0
                    else:
                        return 1
                else:
                    fl7[self.logdelete] = []
        except Exception as er:
            print("Exception in fetchlogssc-> ssc_logdeletepurge")
            print(er)

    def ssc_logcomplete_testwrite(self, testentry: str):
        try:
            temp_copy = []
            with shelve.open(FetchLogSSC._fetchlogpath) as fl6:
                if fl6.keys():
                    if self.logfinish in fl6.keys():
                        temp_copy = fl6[self.logfinish]
                        temp_copy.append(testentry)
                        fl6[self.logfinish] = temp_copy
                    else:
                        fl6[self.logfinish] = [testentry]
                else:
                    fl6[self.logfinish] = [testentry]
        except Exception as er:
            print("Exception in fetchlogssc -> ssc_logcomplete_testwrite")
            print(er)

    def ssc_logcompletefetch(self):
        """

        :return:
        """
        try:
            with shelve.open(FetchLogSSC._fetchlogpath) as fl5:
                if fl5.keys():
                    if fl5[self.logfinish]:
                        return fl5[self.logfinish]
                    else:
                        return 0
        except Exception as er:
            print("Exception in fetchlogssc -> ssc_logcompletefetch")
            print(er)

    def ssc_logcompletepurge(self) -> None:
        """
        Clears shelve at self.logfinish path
        *Mainly for testing purposes
        :return:
        """
        try:
            with shelve.open(FetchLogSSC._fetchlogpath) as fl6:
                if fl6.keys():
                    if self.logfinish in fl6.keys():
                        del fl6[self.logfinish]
                        fl6[self.logfinish] = []
                else:
                    fl6[self.logfinish] = []
        except Exception as er:
            print("Exception in fetchlogssc -> ssc_logcompletepurge")
            print(er)


if __name__ == "__main__":
    FLOG2 = FetchLogSSC()
    printoutput = FLOG2.ssc_logfetch()
    for line in printoutput:
        print(line)
