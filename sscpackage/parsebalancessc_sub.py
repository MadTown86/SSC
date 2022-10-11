import parsebalancessc
import dictpullssc
from sscpackage import fetchshelfssc_mod
import json

import dotenv
import os

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')


class ParseBalance_Sub(parsebalancessc.ParseBalance):
    def __init__(self):
        super().__init__()

    def parsebalance(self, uniquename: 'str', pb_rawdata: dict) -> None:
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidpb = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                                uniquesplitlist[3]

            DS = dictpullssc.DictPullSSC()
            pulled_balance = DS.dictpullssc(pb_rawdata, "balanceSheetHistory")

            pulled_balance = pulled_balance['balanceSheetStatements']

            output_dict = {}

            keybin = [x for x in pulled_balance[0].keys() if x != "maxAge"]
            extrabin = []
            for index in range(1, 4):
                for key in pulled_balance[index].keys():
                    if key in keybin:
                        continue
                    elif key == 'maxAge':
                        continue
                    else:
                        extrabin.append(key)

            print(extrabin)
            for key in keybin:
                temp_list = []
                if key in pulled_balance[0].keys():
                    temp_list.append(pulled_balance[0][key]['raw'])
                else:
                    temp_list.append(0)
                if key in pulled_balance[1].keys():
                    temp_list.append(pulled_balance[1][key]['raw'])
                else:
                    temp_list.append(0)
                if key in pulled_balance[2].keys():
                    temp_list.append(pulled_balance[2][key]['raw'])
                else:
                    temp_list.append(0)
                if key in pulled_balance[3].keys():
                    temp_list.append(pulled_balance[3][key]['raw'])
                else:
                    temp_list.append(0)
                output_dict[key] = temp_list

            if extrabin:
                for key in extrabin:
                    temp_list = []
                    if key in pulled_balance[0].keys():
                        temp_list.append(pulled_balance[0][key]['raw'])
                    else:
                        temp_list.append(0)
                    if key in pulled_balance[1].keys():
                        temp_list.append(pulled_balance[1][key]['raw'])
                    else:
                        temp_list.append(0)
                    if key in pulled_balance[2].keys():
                        temp_list.append(pulled_balance[2][key]['raw'])
                    else:
                        temp_list.append(0)
                    if key in pulled_balance[3].keys():
                        temp_list.append(pulled_balance[3][key]['raw'])
                    else:
                        temp_list.append(0)
                    output_dict[key] = temp_list

            print(ticker)
            print(key)
            print(idssc)
            print(timestampidpb)

            FST_SSC_PB = fetchshelfssc_mod.FetchShelfSSC(fetchstoreshelf=self.setpathssc_parsesscpb)
            FST_SSC_PB.fetchstore(ticker=ticker, key=key, idssc=idssc, fetch_data=output_dict,
                                  timestampidfs=timestampidpb)
            del FST_SSC_PB

        except Exception as Er:
            print("Exception in ParseBalance.parsebalance  ::  ")
            print(str(Er))


if __name__ == "__main__":
    import fetchshelfssc_mod
    FS = fetchshelfssc_mod.FetchShelfSSC()
    localdb = FS.fetchdbpull()
    bal_keylist = [key for key in FS.fetchdbpull().keys() if "url_balance" in key]
    PS = ParseBalance_Sub()
    for key in bal_keylist:
        print(key)
        PS.parsebalance(key, localdb[key])

    uniquetimestampbin = []
    for key in bal_keylist:
        ticker, var1, var2, uniqueid = key.split("__")
        uniquetimestampbin.append(uniqueid)

    fetchbin = []
    for uniqueid in uniquetimestampbin:
        PS.fetch_parsebalance(uniqueid)

    for key, value in fetchbin[0].items():
        print(f'KEY:::{key} >>>>> VALUE:::: {value}')


