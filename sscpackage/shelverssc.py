import shelve
import dotenv
import os
import sscerrors

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')


class ShelverSSC:
    def __init__(self, shelvename: 'str'):
        self.permstorpathssc = ROOT_VAR_SSC
        self.shelvename = shelvename

    def add_singleshelf(self, path: str, key: str, value: str) -> None:
        try:
            with shelve.open(path) as addss:
                addss[key] = value
        except Exception as er:
            print("Exception in ShelverSSC: method 'add_singleshelf' ")
            print(er)

    def pull_shelverssc(self, shelvename: str, gradesystemname="DEFAULT") -> shelve:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            if gradesystemname in sscshelvemanager.keys():
                tempsscshelv = sscshelvemanager[gradesystemname]
                sscshelvemanager.close()
                return tempsscshelv
            else:
                raise sscerrors.NoShelveException

    def inkeys_shelvercorekeysssc(self, shelvename: str, keyname: str) -> bool:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            if keyname in sscshelvemanager.keys():
                return True
            else:
                return False

    def pull_shelvercorekeysssc(self, shelvename: str) -> list:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            try:
                return sscerrors.get_keysshelve(sscshelvemanager)
            except sscerrors.EmptyShelveException as er:
                print(er)

    def pull_shelvesubcorekeys(self, shelvename: str, corenamessc: str) -> list:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            try:
                if sscshelvemanager[corenamessc]:
                    return sscerrors.get_keysshelve(sscshelvemanager[corenamessc])
            except sscerrors.EmptyShelveException as er:
                print(er)

    def pull_shelvesubelementkeys(self, shelvename: str, corenamessc: str, subitemnamessc: str) -> list:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            templist = sscshelvemanager[corenamessc][subitemnamessc]
            sscshelvemanager.close()
            return templist

    def add_shelvecoreelementssc(self, shelvename: str, keywordssc: str, data, *args, **kwargs) -> None:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            sscshelvemanager[keywordssc] = data
            sscshelvemanager.close()

    def del_shelvecoreelementssc(self, shelvename: 'str', keywordssc: 'str') -> None:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            del sscshelvemanager[keywordssc]
            sscshelvemanager.close()

    def add_shelvesubcoreelementssc(self, shelvename: 'str', systemkeywordssc: 'str', subcoreelementid: 'str', data,
                                    *args, **kwargs) -> None:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            sscshelvemanager[systemkeywordssc] = {subcoreelementid: data}
            sscshelvemanager.close()

    def del_shelvesubcoreelementssc(self, shelvename: 'str', systemkeywordssc: 'str', subcoreelementid: 'str',
                                    *args, **kwargs) -> bool:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            tempshelvedict = sscshelvemanager[systemkeywordssc]
            if isinstance(tempshelvedict, dict):
                if subcoreelementid in tempshelvedict.keys():
                    del tempshelvedict[subcoreelementid]
                    sscshelvemanager[systemkeywordssc] = tempshelvedict
                    sscshelvemanager.close()
                    return True
                else:
                    sscshelvemanager.close()
                    return False
            else:
                sscshelvemanager.close()
                return False

    def add_shelvesubelement(self, shelvename: 'str', systemkeywordssc: 'str', coremetricssc: 'str', *args, **kwargs) -> bool:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            tempcopy = sscshelvemanager[systemkeywordssc][coremetricssc]
            if isinstance(tempcopy, dict):
                for key in kwargs.keys():
                    tempcopy[key] = kwargs[key]
                sscshelvemanager[systemkeywordssc][coremetricssc] = tempcopy
                sscshelvemanager.close()
                return True
            elif isinstance(tempcopy, list):
                if args:
                    for value in args:
                        tempcopy.append(value)
                    sscshelvemanager[systemkeywordssc][coremetricssc] = tempcopy
                    sscshelvemanager.close()
                    return True
            else:
                return False

    def del_shelvesubelement(self, shelvename: 'str', keywordssc: 'str', coremetricssc: 'str', *args, **kwargs) -> bool:
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
                return True
            elif isinstance(tempcopy, list):
                for item in args:
                    if item in tempcopy:
                        tempcopy.pop(tempcopy.index(item))
                    else:
                        errstring += str(item) + ', '
                        continue
                sscshelvemanager[keywordssc][coremetricssc] = tempcopy
                sscshelvemanager.close()
                return True
            else:
                sscshelvemanager.close()
                return False

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
        except sscerrors.EmptyShelveException as er:
            print("Exception in ShelverSSC: method 'fetchpeek' ")
            print(er)
