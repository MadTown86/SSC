from mysql.connector import connect, Error
import json
import os
import simplestockchecker_parsetool as sscp
import pandas as pd

"""
Last Update: 2/4/22 - GD
This module 'simplestockchecker_storetool.py' stores information
in the database sscdb, under the table logentry.
"""

def db_chksetup():
    try:
        with connect(
                host="localhost",
                user=str(os.getenv("DB_USER")),
                password=str(os.getenv("DB_PASS")),
        ) as connection:

            db_check="""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.SCHEMATA
            WHERE SCHEMA_NAME = 'sscdb'
            """

            dbtbl_create="""
            CREATE DATABASE sscdb;
            USE sscdb;
            CREATE TABLE logentry (
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

            with connection.cursor(buffered=True) as cursor:
                cursor.execute(db_check)
                if cursor.fetchone()[0] == 1:
                    print("DB Exists")
                else:
                    cursor.execute(dbtbl_create)
                    cursor.commit()

    except Error as e:
        print("Error in ssc_st - TRY1: " + str(e))

# Running to check and instate database upon import into GUI
db_chksetup()


def log_entry(ticker_entry, res_json):
    """
    This function is taking the ticker symbol, fetch data from API, parse data
    and the rest of the information and storing it in a local mysql db with the
    following information.
    DB Name = sscdb
    Table Name = logentry
    :param ticker_entry:
    :param res_json:
    :return: None
    """

    # This portion of the code is going to check for a pre-existing database
    """
    Note: If you want to do testing of this code, you will need to alter the 'host', 'user' and 'password' to reflect
    your local server for all instances.  
    
    The only thing you wouldn't want to change is the name of the db and table, unless you want to further alter the
    remaining SQL Queries.
    
    I used mysql-installer-community-8.0.27.1.msi with mySQL workbench
    """

    # The following sql.connector object adds information from '..._parsetool.py' function attributes to 'logentry'
    try:
        with connect(
            host="localhost",
            user=str(os.getenv("DB_USER")),
            password=str(os.getenv("DB_PASS")),
            database="sscdb",
        ) as connection:

            # The following code is mySQL
            insert_db_table = "INSERT INTO logentry (ticker, fetchdata, idict, bdict, grade, elist, arlist) VALUES(" + '"' \
                              + str(ticker_entry) + '",' + json.dumps(res_json) + ',' \
                              + "'" + json.dumps(sscp.parsetool.idict) + "'" + ',' \
                              + "'" + json.dumps(sscp.parsetool.bdict) + "'" + "," + "'" + sscp.grade_tool.grade + "'" \
                              + "," + "'" + json.dumps(sscp.grade_tool.erlist) + "'" + "," + "'" \
                              + json.dumps(sscp.grade_tool.ar_dict_strip) + "'" + ")"

            show_db_ticker = "SELECT * FROM logentry"
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(insert_db_table)
                connection.commit()

    except Error as e:
        print("Error in ssc_st - TRY2: " + str(e))

    return None


def show_db():
    """
    2/4/22 - GD
    This function is used in ssc_gui.  It is bound to 'show db' tk.button.
    :return: results (response string from API - JSON)
    """
    try:
        with connect(
            host="localhost",
            user=str(os.getenv("DB_USER")),
            password=str(os.getenv("DB_PASS")),
            database="sscdb",
        ) as connection:
            show_db_ticker = "SELECT * FROM logentry"
            with connection.cursor() as cursor:
                cursor.execute(show_db_ticker)
                results = cursor.fetchall()
                connection.commit()

    except Error as e:
        print(e)

    return results


def export_excel():
    """
    2/4/22 - GD
    This function pulls stock grade information from database sscdb -> 'logentry'.

    It uses Pandas data frame to format the sql query stream into row/column format and outputs it to SSC.xlsx
    :return:
    """
    try:
        with connect(
                host="localhost",
                user=str(os.getenv("DB_USER")),
                password=str(os.getenv("DB_PASS")),
                database="sscdb"
        ) as connection:

            query = """
            SELECT id, ticker, logTime, grade FROM logentry"""
            with connection.cursor(buffered=True) as cursor:
                df = pd.read_sql(query, connection)
                df.head()
                df.to_excel('SSC.xlsx', sheet_name='DATA', index=False)

    except Error as e:
        print("Error in ssc_st - 'def export_excel'  :  " + str(e))






