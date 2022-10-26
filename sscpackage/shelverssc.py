import shelve
import dotenv
import os
import sscerrors

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")


class ShelverSSC:
    """
    Class original purpose was to provide shelve functionality to parsing/grading classes that required shelve creation
    and maintenance.


    """

    def __init__(self, shelvename: str):
        self.permstorpathssc = ROOT_VAR_SSC
        self.shelvename = shelvename

    def add_singleshelf(self, path: str, key: str, value: str) -> None:
        # Creates a shelve at path and adds one key: value pair
        with shelve.open(path) as addss:
            addss[key] = value

    def pull_shelverssc_award(
        self, shelvename: str, gradesystemname="DEFAULT"
    ) -> shelve:
        # returns the awardsystem at shelvename
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            if gradesystemname in sscshelvemanager.keys():
                tempsscshelv = sscshelvemanager[gradesystemname]
                sscshelvemanager.close()
                return tempsscshelv
            else:
                raise sscerrors.NoShelveException

    def pull_shelvercorekeysssc(self, shelvename: str) -> list:
        #
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            if sscshelvemanager:
                return sscerrors.get_keysshelve(sscshelvemanager)
            else:
                raise sscerrors.EmptyShelveException

    def add_shelvecoreelementssc(
        self, shelvename: str, keywordssc: str, data, *args, **kwargs
    ) -> None:
        # Add data at shelvename[keywordssc]
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            sscshelvemanager[keywordssc] = data

    def del_shelvecoreelementssc(self, shelvename: "str", keywordssc: "str") -> None:
        with shelve.open(self.permstorpathssc + shelvename) as sscshelvemanager:
            del sscshelvemanager[keywordssc]

    def add_shelvesubelement(
        self,
        shelvename: "str",
        systemkeywordssc: "str",
        coremetricssc: "str",
        *args,
        **kwargs
    ) -> bool:
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

    def fetchpeek(self, path: "str", keysearch: "str") -> bool:
        #
        try:
            with shelve.open(path) as fpshelf_ssc:
                if keysearch in fpshelf_ssc.keys():
                    return True
                else:
                    return False
        except sscerrors.EmptyShelveException as er:
            print("Exception in ShelverSSC: method 'fetchpeek' ")
            print(er)
