import json
import os

import mysql.connector


class StoreSSC:
    """
    Class for checking, storing and fetching data from a local, predefined DB
    """

    def __init__(
        self, host="localhost", user="DB_USER", password="DB_PASS", *args, **kwargs
    ):
        try:
            self.host = host
            self.user = user
            self.password = password
        except Exception as er:
            print("Exception in StoreSSC: constructor ")
            print(er)

    def create_table(self, tablename="test", *args, **kwargs):

        ctable_assemblyvar = """
                        USE sscdb;
                        CREATE TABLE {tname} (
                        {tablevarbody}
                        );
                        """.format(
            tname=tablename, tablevarbody=args
        )
        dbtbl_create = """
                        USE sscdb;
                        CREATE TABLE {0} (
                            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            ticker VARCHAR(5),
                            logTime DATETIME DEFAULT CURRENT_TIMESTAMP,
                            fetchdata LONGBLOB,
                            idict JSON,
                            bdict JSON,
                            grade VARCHAR(2),
                            elist JSON,
                            arlist JSON
                        );"""

    def db_chksetup(self):
        """
        Checks to ensure that the 'sscdb' exists on server 'localhost', if it doesn't, it creates the database and
        table 'logentry'
        Requires - local environment variables for username and password

        *Note: Fails if no server 'localhost' exists.
        :return:
        """
        try:
            with mysql.connector.connect(
                host=self.host,
                user=str(os.getenv(self.user)),
                password=str(os.getenv(self.password)),
            ) as connection:

                db_check = """
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.SCHEMATA
                WHERE SCHEMA_NAME = 'sscdb'
                """

                table_check = """
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = {tablename}"""

                # TODO: Figure out why dbtbl_create doesn't work here but works in workbench
                dbtbl_create = """
                CREATE DATABASE IF NOT EXISTS sscdb;
                USE sscdb;
                CREATE TABLE IF NOT EXISTS logentry (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    ticker VARCHAR(5),
                    logTime DATETIME DEFAULT CURRENT_TIMESTAMP,
                    grade VARCHAR(2),
                    parsecombo JSON,
                    points INT,
                    basepoints INT
                );"""

                with connection.cursor(buffered=True) as cursor:
                    try:
                        cursor.execute(dbtbl_create, multi=True)
                    except Exception as er:
                        print(er)
                        cursor.close()


        except mysql.connector.Error as e:
            print("Error in ssc_st - TRY1: " + str(e))

        finally:
            connection.close()

    # TODO: fix store process, GradeSSC is no longer the default location for stored info.  Use gradecollectionssc.
    def log_entry(self, parsecombo, grade_ssc, ticker_entry, points, basepoints):
        # insert_db_table = "INSERT INTO logentry (ticker, grade, parsecombo) VALUES (%s, %s, %s)"
        # print(insert_db_table)

        combo_json = json.dumps(parsecombo, skipkeys=False)

        try:
            with mysql.connector.connect(
                host=str(os.getenv("localhost")),
                user=str(os.getenv("DB_USER")),
                password=str(os.getenv("DB_PASS")),
                database="sscdb",
            ) as connection:

                show_db_ticker = "SELECT * FROM logentry"
                insert_db_table = (
                    "INSERT INTO logentry (ticker, grade, parsecombo, points, basepoints) "
                    "VALUES (%s, %s, %s, %s, %s)"
                )

                with connection.cursor(prepared=True) as cursor:
                    cursor.execute(
                        insert_db_table,
                        (
                            ticker_entry,
                            grade_ssc,
                            combo_json,
                            points,
                            basepoints,
                        ),
                    )
                    connection.commit()

        except mysql.connector.Error as e:
            print("Error in ssc_st - TRY2: " + str(e))

        finally:
            connection.close()

        return None

    def show_db(self):
        """
        Pulls data on sscdb.
        bound to 'show db' tk.button on user GUI
        :return: results (response string from API - JSON)
        """

        try:
            with mysql.connector.connect(
                host=os.getenv("localhost"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database="sscdb",
            ) as connection:
                show_db_ticker = "SELECT * FROM logentry"
                with connection.cursor() as cursor:
                    cursor.execute(show_db_ticker)
                    results = cursor.fetchall()
                    connection.commit()

        except mysql.connector.Error as e:
            print(e)

        finally:
            connection.close()

        return results


if __name__ == "__main__":
    import gradeparsecombinessc

    S_SSC = StoreSSC()
    S_SSC.db_chksetup()
    # testlogvaridssc = 'Y8bdxbfeWiliz3B'
    # GS = gradeparsecombinessc.GradeParseCombineSSC()
    # testdict = GS.gradeparsecombinessc('NVDA', testlogvaridssc)
    # testdict_json = json.dumps(testdict, skipkeys=False)
    # ticker_testssc = "NVDA"
    # S_SSC.log_entry(parsecombo=testdict_json, grade_ssc="BC", ticker_entry="NVDA")
