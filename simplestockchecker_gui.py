import tkinter as tk
import simplestockchecker_fetchtool as sscf
import os
from sscpackage import storessc as sst, parsessc as sscp
import tkinter.font as tk_font
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk
import sys
import random
import string
import threading as th
global ticker_entry
ticker_entry = []
global freq
global d_range
global text_c
global stop_thread
global error_file
error_file = None
global r_keyl
r_keyl = []

"""
This is to test branch functionality GIT/Pycharm
"""

def ssc_gui():
    """
    2/4/22 - GD
    GUI for SSC and contents of main program.

    Process Flow: User selects a text file with comma separated ticker symbols.  The text file is partially qualified
    to make sure only ticker symbols entered.

    When a correct list is selected, the 'submit' button unlocks and allows for user to submit for processing.

    The Text box should update with user prompts and progress information.  I attempted to use
    additional threads to allow the user to click "show contents" and "show db" and not have the window lock up.  My
    first exposure to multi-processing and multi-threading...I need more time to figure it out and potentially run
    5 symbols at the same time simultaneously to speed up the processing of large files.  Rapid API allows for a max
    of 5 calls per second.  I may need to alter the database in some way to allow for multiple updates simultaneously.

    Known Errors:
    If user tries to close window before hitting cancel and waiting for the 'all clear' when the program is mid-fetch,
    it will crash.


    """
    global text_c
    global ticker_entry  # Setting the local scope ticker_entry as the global scope variable
    ssc_gui.ticker_list = None  # Setting ssc_gui.ticker_list as none function attribute
    window = tk.Tk()  # Setting window as the main tk.Tk() variable
    window.title("Simple Stock Checker - Rev. Jack Concannon")  # Sets title of window
    window.configure(height="600", width="1800", background="LINEN", padx="10", pady="10")  # configures window size
    window.resizable(True, False)  # makes window not changeable
    window.columnconfigure(0, weight=1)  # sets the column length of window I believe for grid
    window.rowconfigure(0, weight=1)  # sets the row size of window for grid
    fontstyle = tk_font.Font(family="Times New Roman", size=18)  # sets a custom font styling as fontStyle
    fontstyle2 = tk_font.Font(family="Times New Roman", size=14, weight="bold")  # sets a custom font styling
    mainframe = tk.Frame(master=window, padx="5", pady="5", bg="LINEN")  # create tk.Frame object
    mainframe.grid(column=0, row=0, columnspan=1, rowspan=1)  # placing mainframe with grid
    # creates frame object at 0, 0
    label_1 = tk.Label(master=mainframe, text="Please select a text file: ", font=fontstyle2, bg="LINEN")
    label_1.grid(column=0, row=0, columnspan=1, sticky="w", pady="5", padx="5")

    # not used
    prog_msg = tk.StringVar()

    # set remaining GUI Tk.Tkinter widgets
    file_btn = tk.Button(master=mainframe, text="Browse", name="file", font=fontstyle2)
    file_btn.grid(column=1, row=0, columnspan=1, padx="5", pady="5", sticky="ne")
    label_spc = tk.Label(master=mainframe, text=str("-" * 130) + "\n", bg="LINEN")
    label_spc.grid(column=0, columnspan=2, row=1)
    sfile_btn = tk.Button(master=mainframe, text="Show File Contents")
    sfile_btn.grid(column=0, row=2, columnspan=1, sticky="w")
    show_db_btn = tk.Button(master=mainframe, text="Show DB")
    show_db_btn.grid(column=1, row=2, columnspan=1, sticky="e")
    text_c = tk.Text(master=mainframe, height="12", width=75, state="disabled", wrap="none")
    text_c.grid(column=0, row=3, columnspan=2, pady="5", padx="5")
    text_cscrollh = tk.Scrollbar(master=mainframe, orient="horizontal")
    text_cscrollh.grid(column=0, row=4, columnspan=2, sticky="nsew")
    text_cscrollv = tk.Scrollbar(master=mainframe, orient="vertical")
    text_cscrollv.grid(column=2, row=3, rowspan=1, sticky="nes")
    text_cscrollv.config(command=text_c.yview)
    text_cscrollh.config(command=text_c.xview)
    text_c.configure(xscrollcommand=text_cscrollh.set, yscrollcommand=text_cscrollv.set)
    exit_btn = tk.Button(master=mainframe, text="CLOSE", font=fontstyle)
    exit_btn.grid(column=0, row=5, columnspan=1, sticky="w")
    cancel_btn = tk.Button(master=mainframe, text="CANCEL", font=fontstyle)
    cancel_btn.grid(column=0, row=5, columnspan=1, sticky="e")


    # setting a tkk style for the submit_click button
    s = ttk.Style()
    s.configure('my.TButton', font=('Times New Roman', 18))

    def text_update(msg):
        """
        This function uses 'msg' passed in argument to alter contents of text_c
        :param msg: any text arrangement accepted by a tk.Text widget
        :return:
        """
        text_c.config(state="normal")
        text_c.delete("1.0", "end")
        text_c.insert("1.0", str(msg))
        text_c.config(state="disabled")

    def rkey():
        """
        This is a random key generator to label threads for the purpose of tracing and destroying threads mid-program
        in the future if that is possible.
        :return: 8 digit random key - rkeyval
        """
        global r_keyl
        rkeyval = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        r_keyl.append(rkeyval)
        return rkeyval

    def fileopn(event):
        """
        This function is linked to the "Browse" button established above.  It allows the user to
        choose a text file with a list of comma separated stock ticker symbols.

        It sets the global 'ticker_entry' as Python list
        It also sets ssc_gui.ticker_list function attribute to ticker_entry
        :param event:
        :return: ticker_entry - although not necessary
        """
        global ticker_entry
        global error_file
        global stop_thread

        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        fd_raw = fd.askopenfile(filetypes=filetypes)  # this is the open file function saving the chosen file as fd_raw

        # The following code is going to parse the file to ensure it is just a list of comma separated tickers
        flag = True
        if fd_raw is not None:  # I believe I can just use if fd_raw
            fd_l = [x for x in fd_raw.readlines()][0]
            fd_check = fd_l.replace(" ", "").split(",")  # Remove spaces and split into lists by comma separators
            for y in fd_check:
                # Check to make sure that there are no ticker symbols with more than 5 characters
                if len(y) > 5:
                    flag = False
                    error_file = fd_check
                    break
                elif len(y) == 0:
                    flag = False
                    error_file = fd_check
                    break
                else:
                    continue
            if flag:
                ticker_entry = fd_check
                stop_thread = False

                # Update ssc_gui function attribute - ticker_entry
                ssc_gui.ticker_list = ticker_entry
                text_update("You have chosen a valid list - click submit to continue processing")

                # Enable submit click when a minimum list of tickers is given
                if len(ticker_entry) >= 1:
                    okbutton.state(["!disabled"])
                else:
                    okbutton.state(["disabled"])

            else:
                text_update("There are invalid ticker symbols present, please retry")

            showinfo(
                title="Selected File",
                message=fd_raw.name
            )

        else:
            text_update("You need to choose a valid file to continue.")

        return ticker_entry

    file_btn.bind("<Button-1>", fileopn)  # binding the button file_btn to the fileopn function with press event

    def show_contents(event):
        """
        This function updates the text_c - tk.Text widget to show the contents of variable ticker_entry
        :param event:
        :return:
        """
        global ticker_entry
        global error_file

        if ticker_entry:
            text_update(ticker_entry)
        elif error_file:
            text_update(error_file)
        else:
            text_update("You must first choose a file before displaying its contents.")

    sfile_btn.bind("<Button-1>", show_contents)  # This binds button sfile_btn to function show_contents

    def cancel_click(event):
        """
        This function cancels the current submission of ticker_entry list after it runs through the end of the
        process.
        :return:
        """

        global stop_thread
        stop_thread = True
        text_update("Operation cancelling")

        if thread_list:
            exit_btn['state'] = 'disabled'
        else:
            exit_btn['state'] = 'normal'
            pass

    cancel_btn.bind("<Button-1>", cancel_click)  # this binds cancel_btn with cancel_click function upon event

    def submit_click():
        """
        This function is meant to start a thread with the main code elements of the remaining SSC program.
        Upon clicking the SUBMIT button, if a ticker_entry list is present, it will send it to the fetch tool
        attribute, parsetool attribute and storetool attribute.
        :return:
        """
        global ticker_entry
        exit_btn['state'] = 'disabled'

        if okbutton.instate(["!disabled"]):
            try:
                if ticker_entry:
                    print("Inside if ticker_entry True")
                    okbutton.state(["disabled"])
                    ssc_gui.ticker_list = ticker_entry
                    text_update("Ticker List Successfully Enterred")
                    window.update()

                    """
                    Place for main program to run on submit click
                    """

                    lchanger = ticker_entry[:]  # Copy of list
                    eloglist = []  # Instantiating an error log list

                    # while loop pops through lchanger list
                    count = 0
                    while lchanger:
                        global stop_thread
                        count += 1
                        print("This is top level count:  " + str(count))

                        if stop_thread:
                            print("made it into stop_thread")
                            for y in th.enumerate():
                                if y.daemon:
                                    okbutton['state'] = 'disabled'
                                    text_update("Process Cancelled - Close Button Now Active")
                                    stop_thread = False
                                    exit_btn['state'] = 'normal'
                                    break
                                else:
                                    continue
                            break

                        try:
                            x = lchanger.pop(0)  # pops first value in lchanger into variable x

                            text_update("Starting API Fetch with Ticker Symbol: " + str(x))  # updates text with current
                            window.update()

                            sscf.get_financials(x)  # passes in x to get_financials, starting main program

                            # this if/else checks to see if the get_financials function updated the files
                            # the function will fail if these two files have no information
                            if os.path.getsize("balancesheets.json") and os.path.getsize("incomestatements.json") > 100:

                                sscp.parsetool()  # Calls .parsetool() takes the two JSON files, formats to Python Dict

                                sscp.grade_tool(sscp.parsetool.bsheets, sscp.parsetool.isheets, sscp.parsetool.idict,
                                                sscp.parsetool.bdict)  # passes parsetool attributes to grade_tool

                                print(str(sscf.get_financials.ticker_entryf))
                            else:
                                text_update("Error with balancesheets.json and/or incomestatements.json for: " + str(x))

                            sst.log_entry(x, sscf.res_direct)

                        except Exception as Ex:
                            print("Error in ssc_gui submit_click :: " + str(Ex))
                            eloglist.append(x)
                            with open("elog.txt", "w") as elog:
                                for x in eloglist:
                                    elog.writelines(str(x) + " \n")

                                elog.close()
                            pass

                        continue

                    window.update()
                    exit_btn['state'] = 'normal'

                else:
                    text_update("File Error - No Stock Ticker List Defined")
                    print("Error in submit click if/else")

            except Exception as Er:
                print(Er)
                print("Exception in GUI Try/Submit")
                text_update("File Error - No Stock Ticker List Defined")
                pass

        else:
            print("we made it to else")

        return ticker_entry

    # Trying to see if I can store reference to this thread in a module level variable for close button functionality
    global thread_list
    thread_list = []

    def sub_threader():
        thread_list.append(th.Thread(target=submit_click, name=rkey(), daemon=True).start())

    okbutton = ttk.Button(master=mainframe, text="SUBMIT", style='my.TButton',
                          command=sub_threader)

    okbutton.grid(column=1, row=5, columnspan=1, sticky="e")

    # okbutton.config(state="disabled")
    okbutton.state(["disabled"])

    def exit_click(event):
        """
        This function is linked to the CLOSE button.  This function is meant to stop all program processes,
        join the thread to the main process and sys.exit()...work in progress...
        :param event:
        :return:
        """
        print(str(exit_btn['state']))
        if exit_btn['state'] == 'normal':
            print(len(th.enumerate()))
            if len(th.enumerate()) > 1:
                for x in th.enumerate():
                    print(x.name)
                    if x.daemon:
                        x.join()
                        print("Thread Joined")
                    else:
                        continue
            else:
                pass

        if exit_btn['state'] == 'normal':
            window.destroy()
            sys.exit()
        else:
            pass

    exit_btn.bind("<Button-1>", exit_click)  # this line of code binds the exit_btn to the exit_click function

    def show_db(event):
        """
        This function pulls the table information from the MySQL database and updates Text_c to show
        the contents of the database for review.
        :param event:
        :return:
        """
        try:
            if sst.show_db():
                results = sst.show_db()
                newline_results = ""
                for row in results:
                    newline_results += str(row) + "\n"
                text_update(str(newline_results))
            else:
                text_update("Database Not Yet Linked: Contact Grover")
        except Exception as Er:
            text_update("Database Not Yet Linked: Contact Grover")
            pass

    show_db_btn.bind("<Button-1>", show_db)  # this binds show_db_btn to show_db function

    for x in th.enumerate():
        print(str(x))
    window.mainloop()
    return ticker_entry

# Calls self to initiate program
ssc_gui()
