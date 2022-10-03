"""
This will start tkinter gui
"""
import asyncio
import itertools
import random
import string
import sys
import threading as th
import time
import tkinter as tk
import tkinter.font as tk_font
# The Rest
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo

import schedule

import fetchssc
import fetchstarterssc
import fetchstarterssc as sscf
import gradestarterssc
import parsessc
# sscpackage imports
from sscpackage import storessc as sst

# TODO: check into 'globals' use on guistarterssc
global freq
global d_range
global text_c
global stop_thread
global error_file
global r_keyl  # At least need this one
global schedule_bool
schedule_bool = True

r_keyl = []
error_file = None


class GuiStarterSSC(object):
    global_schedule = True
    thread_list: [th.Thread] = []
    end_fetchstart = False
    end_parsestart = False
    end_gradestart = False
    cancel_start = False
    guissc_instcount = 0

    @staticmethod
    def schedule_boolfalse():
        global schedule_bool
        schedule_bool = False

    @staticmethod
    def schedule_booltrue():
        global schedule_bool
        schedule_bool = True

    @staticmethod
    def schedule_init():
        global schedule_bool
        while schedule_bool:
            schedule.run_pending()
            time.sleep(1)
        else:
            schedule.clear()

    th.Thread(target=schedule_init, daemon=True).start()

    @staticmethod
    def cancel_init():
        fetchstarterssc.FetchStarterSSC.cancel_fetch()
        parsessc.ParseStart.parse_canceler()
        gradestarterssc.GradeStartSSC.cancel_grade()
        GuiStarterSSC.schedule_boolfalse()

    @staticmethod
    def reset_init():
        fetchstarterssc.FetchStarterSSC.reset_fetch()
        parsessc.ParseStart.reset_parse()
        gradestarterssc.GradeStartSSC.reset_grade()
        GuiStarterSSC.schedule_booltrue()
        GuiStarterSSC.schedule_init()
        th.Thread(target=GuiStarterSSC.schedule_init(), daemon=True).start()

    @staticmethod
    def fetch_instcount():
        return GuiStarterSSC.guissc_instcount

    def __init__(self):
        self.ticker_list = []
        GuiStarterSSC.guissc_instcount += 1

    def start_gui_ssc(self):
        global text_c
        global ticker_entry  # Setting the local scope ticker_entry as the global scope variable
        window = tk.Tk()  # Setting window as the main tk.Tk() variable
        window.title("Simple Stock Checker - Rev. 1.1-a.1")  # Sets title of window
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
            global error_file
            global stop_thread

            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            )

            fd_raw = fd.askopenfile(
                filetypes=filetypes)  # this is the open file function saving the chosen file as fd_raw

            # Validate Chosen List
            flag = True
            if fd_raw:
                fd_l = [x for x in fd_raw.readlines()][0]
                for char in fd_l:
                    chars_notwant = itertools.chain(string.digits, string.punctuation, string.whitespace)
                    if char in chars_notwant:
                        fd_l.replace(char, "")
                fd_check = fd_l.replace(" ", "").split(",")
                for y in fd_check:
                    # Ticker Symbols <= 5
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

                    # ticker_list to set and remove quotations
                    setticker_list = set()
                    for ticker in ticker_entry:
                        temp_ticker = ticker.replace('"', '')
                        setticker_list.add(temp_ticker)

                    # Update ssc_gui function attribute - ticker_entry
                    self.ticker_list = sorted(setticker_list)
                    print(bool(self.ticker_list))
                    text_update(msg="You have chosen a valid list - click submit to continue processing",
                                header="")

                    # Enable submit click when a minimum list of tickers is given
                    if len(self.ticker_list) >= 1:
                        okbutton.state(["!disabled"])
                    else:
                        okbutton.state(["disabled"])

                else:
                    text_update(msg="There are invalid ticker symbols present, please retry", header="")

                showinfo(
                    title="Selected File",
                    message=fd_raw.name
                )

            else:
                text_update(msg="You need to choose a valid file to continue.", header="")

            return

        file_btn.bind("<Button-1>", fileopn)  # binding the button file_btn to the fileopn function with press event

        def show_contents(event):
            """
            This function updates the text_c - tk.Text widget to show the contents of variable ticker_entry
            :param event:
            :return:
            """

            if self.ticker_list:
                text_update(self.ticker_list)
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

            text_update("Cancel pressed...please wait for current process to finish before closing application")

            GuiStarterSSC.cancel_start = True
            GuiStarterSSC.cancel_init()

            if GuiStarterSSC.thread_list:
                exit_btn['state'] = 'disabled'
            else:
                exit_btn['state'] = 'normal'
                GuiStarterSSC.reset_init()
                text_update(msg="Cancel Successful:  Please select new list or close.", header="")
                GuiStarterSSC.cancel_start = False
                pass

        cancel_btn.bind("<Button-1>", cancel_click)  # this binds cancel_btn with cancel_click function upon event

        def text_update(msg, header: str = "- DEFAULT -"):
            """
            This function uses 'msg' passed in argument to alter contents of text_c
            :param msg: any text arrangement accepted by a tk.Text widget
            :return:
            """
            text_c.config(state="normal")
            text_c.delete("1.0", "end")
            text_c.insert("1.0", str(f'STATUS MESSAGE: {header} -> {msg}'))
            text_c.config(state="disabled")

        def submit_click():
            """
            This function is meant to start a thread with the main code elements of the remaining SSC program.
            Upon clicking the SUBMIT button, if a ticker_entry list is present, it will send it to the fetch tool
            attribute, parsetool attribute and storetool attribute.
            :return:
            """
            exit_btn['state'] = 'disabled'

            if okbutton.instate(["!disabled"]):
                try:
                    if self.ticker_list:
                        okbutton.state(["disabled"])
                        text_update("LIST SUBMIT", "Ticker List Successfully Enterred")
                        window.update()

                        """
                        Place for main program to run on submit click
                        """

                        # Begin main algorithm
                        if not GuiStarterSSC.cancel_start:
                            print("Ticker List")
                            FS = sscf.FetchStarterSSC(self.ticker_list)
                            schedule.every(1).seconds.do(lambda: text_update(header=FS.pull_header(), msg=FS.pull_runlist()))
                            schedule.run_pending()
                            asyncio.run(FS._fetch_cycle())
                            schedule.clear()
                        print("After Fetch")
                        GuiStarterSSC.end_fetchstart = True
                        if GuiStarterSSC.cancel_start:
                            GuiStarterSSC.schedule_boolfalse()
                            schedule.clear()
                            exit_btn['state'] = 'normal'

                        if not GuiStarterSSC.cancel_start:
                            PS = parsessc.ParseStart()
                            schedule.every(1).seconds.do(
                                lambda: text_update(header=PS.pull_parseheader(), msg=PS.parse_runfetch()))
                            schedule.run_pending()
                            PS.ssc_parselogstart(fetchssc.FetchSSC.pull_fetchfaillist())
                            schedule.clear()
                        print("After Parse")
                        GuiStarterSSC.end_parsestart = True
                        if GuiStarterSSC.cancel_start:
                            GuiStarterSSC.schedule_boolfalse()
                            schedule.clear()
                            exit_btn['state'] = 'normal'

                        if not GuiStarterSSC.cancel_start:
                            print("Just Before Grade Start")
                            # TODO: unsuported operand type(s) for /: 'float' and 'tuple' - check into
                            GS = gradestarterssc.GradeStartSSC()
                            print("After Instantiation of GS")
                            schedule.every(1).seconds.do(lambda: text_update(header=GS.pull_gradeheader(), msg=GS.get_runitem()))
                            print("After Grade schedule lambda")
                            schedule.run_pending()
                            print("After schedule.run_pending")
                            GS.gradestartssc()
                            schedule.clear()

                        text_update("Ticker List Processed - Click 'Show DB' Button for Grade", "")


                        GuiStarterSSC.end_gradestart = True
                        if GuiStarterSSC.cancel_start:
                            GuiStarterSSC.schedule_boolfalse()
                            schedule.clear()
                            exit_btn['state'] = 'normal'

                        

                        # TODO: Create a stop process to terminate fetch/parse actions

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

        # TODO: Need to check to see if I still need to create multiple threads to handle the freezing issue on the GUI

        def sub_threader():
            GuiStarterSSC.thread_list.append(th.Thread(target=submit_click, name=rkey(), daemon=True).start())

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
            schedule.clear()
            GuiStarterSSC.schedule_boolfalse()
            print(str(exit_btn['state']))
            if exit_btn['state'] == 'normal':
                print(len(th.enumerate()))
                if len(th.enumerate()) > 1:
                    for x in th.enumerate():
                        print(x.name)
                        if x is not th.main_thread():
                            x.join()
                            print(f'THREAD JOINED: {x.name}')
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
            ST = sst.StoreSSC()

            """
            This function pulls the table information from the MySQL database and updates Text_c to show
            the contents of the database for review.
            :param event:
            :return:
            """
            try:
                if ST.show_db():
                    results = ST.show_db()
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

        if GuiStarterSSC.guissc_instcount == 1:
            window.mainloop()
        return

    # start_gui_ssc = staticmethod(start_gui_ssc)


if __name__ == "__main__":
    GSSC = GuiStarterSSC()
    GSSC.start_gui_ssc()
