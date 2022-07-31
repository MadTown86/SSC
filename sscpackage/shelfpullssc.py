"""
This class will simplify accessing a shelves information.  It should have been created first and inherited into the
parse and fetch ssc.
"""
import shelve

class ShelfPullSSC:
    def pullshelfssc(self, pathshelfssc):
        """
        Input shelve path, return shelve
        :param pathshelfssc:
        :return: shelve at path
        """
        with shelve.open(pathshelfssc) as psssc:
            if psssc.keys():
                ret = dict(psssc)
                psssc.close()
                return ret
            else:
                psssc.close()
                return 0

    def pullshelfkeylistssc(self, pathshelfssc):
        """
        Input shelve path, return list of keys at shelve
        :param pathshelfssc:
        :return: list of keys in shelve
        """
        with shelve.open(pathshelfssc) as psssc:
            if psssc.keys():
                ret = [keypsssc for keypsssc in psssc.keys()]
                psssc.close()
                return ret
            else:
                psssc.close()
                return 0

    def pullvalueinshelfssc(self, pathshelfssc, keyshelfssc):
        """
        Input shelf path and key variable, return value of key in shelf
        :param pathshelfssc: path to shelve
        :param keyshelfssc: key variable in shelve
        :return:
        """
        with shelve.open(pathshelfssc) as psssc:
            if psssc.keys():
                if keyshelfssc in psssc.keys():
                    retvalssc = psssc[keyshelfssc]
                    psssc.close()
                    return retvalssc
                else:
                    psssc.close()
                    return 0
