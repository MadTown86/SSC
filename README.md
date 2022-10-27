# Simple Stock Checker (SSC)

-Learning Exercise : Simple Stock Checker  
-Date: 10/24/2022  
-Author: GD  

---

## Goal:

>The purpose of this application is to grade stocks automatically based on fetched financial information.  Over time, using regression analysis, one could gauge whether the grading algorithm had a positive correlation with upward price movement.  (Example: 'A' grade bin of stocks has strongest correlation with upward price movement at 1mo, 2mo, 3mo intervals).  Tweak the grading algorithm until positive correlation could be reasonably assured.  Speculate accordingly.

---

## Introduction

>The user selects a .txt file of ticker symbols as input and outputs a grade into a local MySQL database and an xlsx gradesheet into ..\sscpackage\storage\excelstorage.
>
>The application has a GUI for ease of file selection.  The GUI has additional basic functionality, such as reviewing the selected files contents and displaying the contents of the MySQL database, as well as updating the text box with status information.  
>
>After a file is selected and the user clicks 'submit', the app fetches historical financial documents from RapidApi.  The data fetched includes Balance Sheets, Income Statements, Financial Ratios, Analyst Ratings, Industry and Sector information.  SSC reorganizes the data, grades it and outputs the grade and all core associated information into a local mySQL database.
>
---

## Known Issues and Future Plans  
- The multi-threading of the GUI needs correction, the cancel and close button functionality often crash the application.
- After a list of ticker symbols is graded without issue, the GUI needs to reset to allow for another list to be selected.
- The grading system needs to be proven and shaped towards Industry and Sector specifics
- Require a way to visually check and alter a 'awardsystem' due to frequent need to alter

---
## Setup Instructions:

In order to get this application to function locally from within an IDE.  You will need to update the following items on your local machine:

1. Root Locations and .ENV file  
2. API Key Registration and additional Environment Variables  
3. Create or Associate a MySQL Server  

---

### 1. Root Locations and .ENV file  
>
> #### Update environment variables  
>    a. "LO_ROOT" = location of .ENV file within sscpackage - update this in your local machine environment variables
>    ```python
>    dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
>    ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")
>    ```
>
>    b. "CORE_DIR_STORE" = path to the ".sscpackage\storage\" folder on your local machine - update this in the .ENV file
>    ```python
>    "CORE_DIR_STORE" = "yourpathhere.\sscpackage\storage\"
>    ```
>    

### 2. API Key Registration and additional Environment Variables  
>
>a. Sign up for a personal free account on *[RapidApi](rapidapi.com)  
>
>b. Create an 'application' in your rapidapi.com account
>
>![Image from RapidApi](https://i.imgur.com/gOtBpta.png "Image of location of unique key from within account settings on RapidApi")
>
>c. Make note of your securitykey and create environment variable "RAPI_key"
>
>```python
>headers = {
>     "x-rapidapi-host": "yh-finance.p.rapidapi.com",
>     "x-rapidapi-key": os.getenv("RAPI_key"),
>}
>```


### 3. Create or Associate a MySQL Server  
>
>a. Create a server with [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)  
>
>Or use other software that can create an appropriate 'host' location for pythons mysql.connector  
>
>b. Create local machine environment variables for "localhost", "DB_USER", "DB_PASS"
>```python
>host=os.getenv("localhost"),
>user=os.getenv("DB_USER"),
>password=os.getenv("DB_PASS")
>```


---

## Run Instructions  
1. Find and run if '__name__ == "__main__":' section of module 'mainssc.py'
>```python
>if __name__ == "__main__":
>    CS = ControlBoardSSC()
>    CS.gui.start_gui.ssc()
>```
>
>
>*Example Image of GUI*  
>
>![GUI Example](https://i.imgur.com/226sAIp.png "Click 'browse' and select a file") 
>
2. Click 'browse' and select a file with comma separated ticker symbols  
>
>![TickerList](https://i.imgur.com/VVFswN5.png "Only alphanumerical characters and commas")  
>
3. Click 'Submit' button and program should run through list of ticker symbols and final outcome will be stored in local database  
>
>![MySqlWorkbench](https://i.imgur.com/Ieo616i.png "Table logentry shows the grades and stores parsed data and unique run id")
>
>Otherwise click on the 'show db' button on the GUI to check stored values  
>![GUIShowDB Button](https://i.imgur.com/x87dIWu.png "Show DB Button Pulls Data from the MySQL Database")  
>
