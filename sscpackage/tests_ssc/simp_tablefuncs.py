import mysql
from mysql.connector import connect, Error
import os
import inspect
import textwrap


class Simp_TableFuncs:
    def create_commit(self, commitstr, host='localhost', database='sscdb'):
        try:
            with mysql.connector.connect(
                    host=host,
                    user=str(os.getenv("DB_USER")),
                    password=str(os.getenv("DB_PASS")),
                    database=database,
            ) as connection:
                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(commitstr)
                    connection.commit()

        except mysql.connector.Error as e:
            print("Error in create_table")
            print(e)

        finally:
            connection.close()

    def create_table(self, tablename='test', uniquekey=True, *args, **kwargs):
        """
        This method assembles the MySQL string to establish a table using mysql.connector.

        :param tablename:
        :param uniquekey: defaults to True and creates an ID column with unique key
        :param args:
        :param kwargs: These key, value pairs become 'column': 'datatype'
        :return: returns the string to pass into mysql.connector cursor.execute
        """

        tablevarbody = ''
        if uniquekey == True:
            tablevarbody += 'id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,'
        else:
            pass

        columnvals = {**kwargs}
        for columnname in columnvals.keys():
            tablevarbody += ' ' + str(columnname) + ' ' + str(columnvals[columnname]).upper() + ','

        tablevarbody = tablevarbody[0:-1]

        ctable_assemblyvar = """CREATE TABLE {tname} ({tablevarbody});""".format(tname=tablename, tablevarbody=tablevarbody)

        return ctable_assemblyvar

    def delete_table(self, tnamedel):
        delstr = """DROP TABLE IF EXISTS {tnamedel};""".format(tnamedel=tnamedel)
        self.create_commit(delstr)

    def create_sqlfunc(self, sql, tableexists=True):
        if tableexists == True:
            checkfunc = """CREATE FUNCTION tableExistsOrNot (_tableName VARCHAR(255))
            RETURNS BOOLEAN
            DETERMINISTIC
            BEGIN
             IF 
             (SELECT COUNT(*)FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = _tableName) = 1
             THEN
             RETURN TRUE;
              ELSE
                RETURN FALSE;
                END IF;
            END;"""
            self.create_commit(checkfunc)
        else:
            self.create_commit(sql)

    def runfunc(self, tablename='logentry', funcname='tableExistsOrNot'):
        table_check = """
        SELECT {funcname}({tablename});
        """.format(funcname=funcname, tablename=tablename)
        self.create_commit(table_check)


    def funcdrop(self, funcname, tableexistsf=True):
        if tableexistsf == True:
            executestatement = """DROP FUNCTION IF EXISTS tableExistsOrNot;"""
            self.create_commit(executestatement)
        else:
            self.create_commit('DROP FUNCTION IF EXISTS {funcname};'.format(funcname=funcname))


if __name__ == '__main__':
    TS1 = Simp_TableFuncs()
    TS1.funcdrop(None)
    TS1.create_sqlfunc(None)
    print(TS1.runfunc())




