# SSC
Learning Exercise : Stock Screener

Author: Grover Donlon Date: 6/16/2022

About: This program was/is a learning exercise for me to increase my understanding of JSON, MySQL and how to use Python's Tkinter. Now that I am changing the program over to a class structure, it is furthering my understanding of classes, OOP, unit testing and as a byproduct the unittest python package, specifically unittest.Mock and unittest.mock.patch.

Description: This program allows the user to select a text file containing comma separated stock ticker symbols. The symbols are used to send fetch requests to RapidAPI to retrieve historic and current financial documentation in the form of JSON strings.

The program isolates balance sheet, income statement, review, and sector data. Examples can be found in files "balancesheets.json", "incomestatements.json", and "sectordata.json" and "ardata.json". It reorganizes the data into a more iterable format, performs a crude grading algorithm and then stores a log entry in a mysql database.

Usage: The program was originally written as a large script with four files "simplestockchecker_fetchtool.py", "simplestockchecker_gui.py", "simplestockchecker_parsetool.py", and "simplestockchecker_storetool.py".

The 'main' file that you would start to run the program, originally, was "simplestockchecker_gui.py". However, the program is currently broken in its current form as of 6/16/22, while I convert the existing script structure into a class structure.

To use the program in its original form, you would have to roll back the commits or extract the original commit from this repository (aka the original 4 files above before edits). In addition, you need to create a server on localhost for simplicity (or alter the '...storetool.py' file and change the variable name to an existing server you have set up). Then ensure that you have environment variables "DB_USER" and "DB_PASS" set appropriately for your local server.

In Progress: To view progress towards changing over to a class structure, view the directory "\sscpackage" and "\sscpackage\tests_ssc"
