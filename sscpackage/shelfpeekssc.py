import shelve

class FetchPeekSSC:
    def fetchpeek(self, path: 'str', keysearch: 'str') -> bool:
        """
        Tests for presence of key in shelf at path
        :param path: string with path of shelve
        :param keysearch: string key value
        :return:
        """
        with shelve.open(path) as fpshelf_ssc:
            if keysearch in fpshelf_ssc.keys():
                return True
            else:
                return False