import shelve
import dotenv
import os
dotenv.load_dotenv(dotenv_path=r'C:\SSC\SimpleStockChecker_REV1\venv\.env')
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')


class ShelverSSC:
    def __init__(self, shelvename: 'str'):
        self.permstorpathssc = ROOT_VAR_SSC
        self.shelvename = shelvename

    def add_singleshelf(self, path, key, value):
        try:
            with shelve.open(path) as addss:
                addss[key] = value
        except Exception as er:
            print("Exception in ShelverSSC: method 'add_singleshelf' ")
            print(er)

    def pull_shelverssc(self, shelvename, gradesystemname="DEFAULT"):
        try:
            with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
                if gradesystemname in sscshelvemanager.keys():
                    tempsscshelv = sscshelvemanager[gradesystemname]
                    sscshelvemanager.close()
                    return tempsscshelv
                else:
                    sscshelvemanager.close()
                    return 0
        except Exception as er:
            print("Exception in ShelverSSC: method 'pull_shelverssc'")
            print(er)

    def inkeys_shelvercorekeysssc(self, shelvename, keyname):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            if keyname in sscshelvemanager.keys():
                return 1
            else:
                return 0

    def pull_shelvercorekeysssc(self, shelvename):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            tempkey_list = [key for key in sscshelvemanager.keys()]
            sscshelvemanager.close()
            return tempkey_list

    def pull_shelvesubcorekeys(self, shelvename, corenamessc):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            tempkey_list = [key for key in sscshelvemanager[corenamessc].keys()]
            sscshelvemanager.close()
            return tempkey_list

    def pull_shelvesubelementkeys(self, shelvename, corenamessc, subitemnamessc):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            templist = sscshelvemanager[corenamessc][subitemnamessc]
            sscshelvemanager.close()
            return templist

    def add_shelvecoreelementssc(self, shelvename: str, keywordssc: str, data, *args, **kwargs):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            sscshelvemanager[keywordssc] = data
            sscshelvemanager.close()

    def del_shelvecoreelementssc(self, shelvename: 'str', keywordssc: 'str'):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            del sscshelvemanager[keywordssc]
            sscshelvemanager.close()

    def add_shelvesubcoreelementssc(self, shelvename: 'str', systemkeywordssc: 'str', subcoreelementid: 'str', data,
                                    *args, **kwargs):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            sscshelvemanager[systemkeywordssc] = {subcoreelementid: data}
            sscshelvemanager.close()

    def del_shelvesubcoreelementssc(self, shelvename: 'str', systemkeywordssc: 'str', subcoreelementid: 'str',
                                    *args, **kwargs):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            tempshelvedict = sscshelvemanager[systemkeywordssc]
            if isinstance(tempshelvedict, dict):
                if subcoreelementid in tempshelvedict.keys():
                    del tempshelvedict[subcoreelementid]
                    sscshelvemanager[systemkeywordssc] = tempshelvedict
                    sscshelvemanager.close()
                    return 1
                else:
                    sscshelvemanager.close()
                    return 0
            else:
                sscshelvemanager.close()
                return 0

    def add_shelvesubelement(self, shelvename: 'str', systemkeywordssc: 'str', coremetricssc: 'str', *args, **kwargs):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            tempcopy = sscshelvemanager[systemkeywordssc][coremetricssc]
            if isinstance(tempcopy, dict):
                for key in kwargs.keys():
                    tempcopy[key] = kwargs[key]
                sscshelvemanager[systemkeywordssc][coremetricssc] = tempcopy
                sscshelvemanager.close()
                return 1
            elif isinstance(tempcopy, list):
                if args:
                    for value in args:
                        tempcopy.append(value)
                    sscshelvemanager[systemkeywordssc][coremetricssc] = tempcopy
                    sscshelvemanager.close()
                    return 1
            else:
                return 0

    def del_shelvesubelement(self, shelvename: 'str', keywordssc: 'str', coremetricssc: 'str', *args, **kwargs):
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            tempcopy = sscshelvemanager[keywordssc][coremetricssc]
            errstring = ""
            if isinstance(tempcopy, dict):
                for key in args:
                    if key in tempcopy.keys():
                        del tempcopy[key]
                    else:
                        errstring += str(key) + ', '
                        continue
                sscshelvemanager[keywordssc][coremetricssc] = tempcopy
                sscshelvemanager.close()
                return 1
            elif isinstance(tempcopy, list):
                for item in args:
                    if item in tempcopy:
                        tempcopy.pop(tempcopy.index(item))
                    else:
                        errstring += str(item) + ', '
                        continue
                sscshelvemanager[keywordssc][coremetricssc] = tempcopy
                sscshelvemanager.close()
                return 1
            else:
                sscshelvemanager.close()
                return 0, errstring

    def fetchpeek(self, path: 'str', keysearch: 'str') -> bool:
        """
        Tests for presence of key in shelf at path
        :param path: string with path of shelve
        :param keysearch: string key value
        :return:
        """
        try:
            with shelve.open(path) as fpshelf_ssc:
                if keysearch in fpshelf_ssc.keys():
                    return True
                else:
                    return False
        except Exception as er:
            print("Exception in ShelverSSC: method 'fetchpeek' ")
            print(er)
