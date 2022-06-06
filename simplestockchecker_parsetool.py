import json
import simplestockchecker_fetchtool as sscf
import sys
import os
import os.path
import time
import datetime as dt
import unittest
import unittest.mock

"""
4/30/22 - Branch Start - Change To OOP Structure
"""

def dictpull(arg, header):
    """
    No Need for this to be a class, a recurse function
    :param arg:
    :param header:
    :return:
    """
    if isinstance(arg, dict):
        for b in arg.keys():
            if b == header:
                return arg[b]
            elif isinstance(arg[b], dict):
                return dictpull(arg[b], header)
            else:
                continue
    else:
        for z in arg:
            return dictpull(arg, header)

def safe_open_w(path):
    """
    Open "path" for writing, creating any parent directories as needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')

class GradeSSC:
    def __init__(self):
        pass


    def grade_tool(self, bsheets_zip: "list", isheets_zip: "list", isheets_dict: "dict", bsheets_dict: "dict") -> "str":
        """
        8/14/2021
        Author: GD

        This function is going to take the returned variables from 'parsetool' as its arguments.

        The expected form of the arguments are lists of 4 value tuples that contain financial data for public traded companies
        The data 'should' remain chronological within the tuple pairs so that they may be iterated and processed for grading

        :param bsheets_zip:
        :param isheets_zip:
        :return: grade
        """

        path_gs = "C:/SSC/SSC_GRADESHEETS/"
        pre_fix = "_" + str(sscf.get_financials.ticker_entryf) + "_" + \
                  str(int(str(time.time()).replace('.', ''))) + "_" + "GradeS.json"

        # Copy from above def statements in parse_tool.  Didn't want to alter and make top level



        self.grade_tool.erlist = []  # This will store the errors/missing data from the analysis for review
        erlist = []


        self.grade_tool.arlist = [] #  This will store the initial analyst grades

        self.grade_tool.tp = 0 # this is going to store the total points and increment as the various factors pass logical pathways

        self.grade_tool.ar_dict_strip = [] # this stores the ar - analyst ratings dictionaries wrapped in a list to store or pull to analyze

        bdict = bsheets_dict
        idict = isheets_dict

        self.grade_tool.g = 0 # This may be redundant as well, using a function attribute to store the following gv variable

        gv = 0 # GV is going to be the variable that increments the awarded points

        in_sheets = self.parsetool.isheets # This stores the function variables isheets and bsheets in local variables, which may be a redundancy to look at
        bal_sheets = self.parsetool.bsheets

        # This is to simplify the typing of new line escape - should have done this sooner
        brn = "\n"
        brl = ("-" * 80)
        """
        This is the beginning of the actual grading requirements script starting first with income statement metrics
        
        This tool adds points to the total grade if a category exists within the data
        """
        """
        1/22/22 - GD
        Updating the grade tool to be more transparent.  Also writing a "grade sheet" to file that will give a 
        visual representation of how the stock was graded for analysis and error checking
        """

        """
        
        
        
        GRADE SECTION 1:
        
        
        
        """

        # This write to file code is meant to be temporary to error check and prove out the grading system
        with safe_open_w(path_gs + pre_fix) as f:
            # Header line - Ticker / Date
            header = "Grade Sheet - " + str(sscf.get_financials.ticker_entryf) + "  :  " + str(dt.datetime.now())

            # Write header to file
            f.write(brn*2)
            f.write(brl)
            f.writelines(brn + header + brn + brl + brn + brn)
            f.write("SECTOR DESIGNATOR:  " + str(self.parsetool.sector).upper() + (brn * 2))
            f.write("INDUSTRY DESIGNATOR:  " + str(self.parsetool.industry).upper() + (brn * 2))
            f.write(brl + brn + "BEGINNING OF SECTION 1: KEY METRICS" + brn + brl + brn +brn)


            # Process list of key metrics, accumulate grade points and write to gradesheet section 1
            l_rev = ["Total Revenue", "Net Income", "Gross Margin", "Operating Margin", "Net Margin"]
            for x in l_rev:
                f.write("\n\n")
                f.write(x + "  :  ")
                if x not in [y for y in idict.keys()]:

                    erlist.append(x)
                    continue
                else:
                    self.grade_tool.tp += 6  # add 6 points to total for each loop
                    flag = 0
                    l_ishell = idict[x]
                    # check for zero values
                    for y in l_ishell:
                        if float(y) == 0:
                            flag += 1

                    if flag == 0:
                        if l_ishell[0] > l_ishell[1] and l_ishell[2]:
                            gv += 6
                            f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year > Prior Two :::: +6 POINTS\n")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                    + str(l_ishell[3]) + "  ***\n")
                            continue
                        # If latest year is greater than prior 1 year and less than 2nd get 5 points
                        elif (l_ishell[0] > l_ishell[1]) and (l_ishell[0] < l_ishell[2]):
                            gv += 5
                            f.write(str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year > Prior Year, but < Two Years Prior :::: +5 POINTS\n")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                    + str(l_ishell[3]) + "  ***\n")
                            continue
                        # Cutting company slack if performance is volatile, still a chance they may come out on top
                        elif (l_ishell[0] < l_ishell[1]) and (l_ishell[0] > l_ishell[2]):
                            gv += 3
                            f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year < Prior Year, but > Two Years Prior ::::: + 3 POINTS\n")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                    + str(l_ishell[3]) + "  ***\n")
                            continue
                        # Company is declining year over year
                        else:
                            gv += 0
                            f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year < Prior Two Years ::::: + 0 POINTS")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                    + str(l_ishell[3]) + "  ***\n")
                            continue
                    elif flag == 1:
                        if l_ishell[0] > l_ishell[1] and l_ishell[2]:
                            gv += 6
                            f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year > Prior Two Years  :::: +6 POINTS\n")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                    + "  ***\n")
                            continue
                        # If latest year is greater than prior 1 year and less than 2nd get 5 points
                        elif (l_ishell[0] > l_ishell[1]) and (l_ishell[0] < l_ishell[2]):
                            gv += 5
                            f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year > Prior Year, but < Two Years Prior  :::: +5 POINTS\n")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                    + "  ***\n")
                            continue
                        # Cutting company slack if performance is volatile, still a chance they may come out on top
                        elif (l_ishell[0] < l_ishell[1]) and (l_ishell[0] > l_ishell[2]):
                            gv += 3
                            f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year < Prior Year, but > Two Years Prior\n")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                    + "  ***\n")
                            continue
                        # Company is declining year over year
                        else:
                            gv += 0
                            f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year < Prior Two Years\n")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                    + "  ***\n")
                            continue
                    # Only 2 years of financial documents
                    elif flag == 2:
                        if l_ishell[0] > l_ishell[1]:

                            gv += 6
                            f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year > Prior Year  :::: +6 POINTS\n")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  '
                                    + "  ***\n")
                            continue
                        else:
                            gv += 0
                            f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                            f.write("Most Recent Year < Prior Year\n")
                            f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  '
                                    + "  ***\n")
                            continue
                    # Only 1 or less years of financial documents/information - section removed
                    elif flag > 2:
                        self.grade_tool.tp -= 6
                        f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                        f.write("Not Enough Information - No Grade\n")
                        continue

            f.write(brn + brn + brl)
            f.write("\nEND OF FIRST SECTION - NEAR LINE 534\n")
            f.write(brl + "\n\n")

            f.write(brl + "\nBEGINNING SECTION 2: PROFITS & RESEARCH\n" + brl + (brn * 2))

            # L1 is a hard-coded list of index positions for certain variables
            # 1/22 This needs to be changed to a dynamic list that searches the data and populates
            l_1 = ["Gross Profit", "EBIT", "Operating Income", "Net Income From Continuing Ops", "Income Before Tax",
                  "Research & Development"]
            # All Variables You Want Increasing YoY
            # Total of 20 points possible

            for x in l_1:
                f.write("\n\n")
                f.write(x + "   :   ")
                if x not in [y for y in idict.keys()]:
                    erlist.append(x)
                    continue
                else:
                    l_ishell = idict[x]
                    self.grade_tool.tp += 2  # add 2 points to total
                    """
                    If the latest year revenue is greater than the prior 2 years get a full 2 points
                    """
                    if l_ishell[0] > l_ishell[1] and l_ishell[2]:
                        gv += 2
                        f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                        f.write("Most Recent Year > Prior Two Years ::::: + 2 POINTS\n")
                        f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                + "  ***\n")
                        continue
                    elif (l_ishell[0] > l_ishell[1]) and (l_ishell[0] < l_ishell[2]):
                        gv += 1.5
                        f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                        f.write("Most Recent Year > Prior Year Only ::::: + 1 POINT\n")
                        f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                + "  ***\n")
                        continue
                    elif (l_ishell[0] < l_ishell[1]) and (l_ishell[0] > l_ishell[2]):
                        gv += .5
                        f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                        f.write("Most Recent Year < Prior Year > 2 Years ::::: + .5 POINTS\n")
                        f.write("***  " + str(l_ishell[0]) + ',  ' + str(l_ishell[1]) + ',  ' + str(l_ishell[2]) + ',  '
                                + "  ***\n")
                        continue
                    else:
                        f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                        f.write("Most Recent Year > Prior Two Years\n")
                        gv += 0
                        continue
            print("Line 493")
            f.write("\n\n" + brl + "\nEND OF SECTION 2 - NEAR LINE 585\n" + brl + "\n\n")

            """
            1/23/22 - GD
            Goal is to create a new dictionary with same structure as before with one change.  Change is all variables are
            stored as a percentage of that years total revenue, then judging increase/decrease becomes more meaningful YoY
            New dictionary will be called idict_ratio
            """
            idict_ratio = {}
            for key in [y for y in idict.keys()]:
                idict_ratio[key] = [idict[key][x] / idict["Total Revenue"][x] for x in range(len(idict["Total Revenue"]))]

            l_3 = ["Selling, General & Administrative", "Other Operating Expenses", "Interest Expense",
                                    "Total Operating Expenses", "Cost Of Revenue", "Total Other Income Expense Net"]

            f.write("\n\n" + brl)

            f.write("\nBEGINNING OF SECTION 3: METRICS AS PERCENTAGE OF TOTAL REVENUE & GENERAL\n")
            f.write(brl + "\n\n")
            #  All expenses that you want reducing as a percentage of total revenue YoY
            for x in l_3:
                if x not in [y for y in idict_ratio.keys()]:
                    erlist.append(x)
                    continue
                else:
                    l_ishell = idict_ratio[x]
                    f.write(brn*2)
                    f.write(str(x) + "  :  ")
                    self.grade_tool.tp += 2
                    if l_ishell[0] < l_ishell[1] and l_ishell[2]:
                        gv += 2
                        f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                        f.write("Current Year < Prior 2 Years ::::: + 2 POINTS\n")
                    elif l_ishell[0] < l_ishell[1] or l_ishell[2]:
                        gv += 1
                        f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                        f.write("Current Year < 1 Year Prior or 2 ::::: + 1 POINT\n")
                    else:
                        f.write("Metric increasing, not decreasing ::::: + 0 POINTS\n")
                        f.write("No Points Awarded\n")
                        continue

            f.write("\n\n")
            l_4 = ["Total Assets", "Retained Earnings"]
            # total of 2 bonus points possible
            for x in l_4:
                if x not in [y for y in idict_ratio.keys()]:
                    erlist.append(x)
                    continue
                else:
                    i_ishell = idict_ratio[x]
                    f.write(str(x) + "  :  \n")
                    #  Not adding grade to total points - considering this section a 'bonus'
                    if i_ishell[0] > i_ishell[1] and i_ishell[2]:
                        gv += 1
                        f.write("GRADE::: " + str(gv) + ' / ' + str(self.grade_tool.tp) + "\n")
                        f.write("Metric Current Year > Prior 2 Years ::::: + 1 POINT\n")
                    else:
                        f.write("No Bonus Points Awarded\n\n")
                        continue

            f.write(brn + brn + brl + brn)
            f.write("END OF SECTION 3: METRICS AS PERCENTAGE OF TOTAL REVENUE & GENERAL - NEAR LINE 636\n")
            f.write(brl + brn+ brn)


            f.write(brl + "\nBEGIN SECTION 4: FINANCIAL RATIOS\n")
            f.write(brl + brn + brn)

            # This variable declaration is redundant, possible to just use bdict/idict.  Less typing.
            b = bdict
            inc1 = idict

            """
            1/26/2022 - GD
            I feel the need to alter this section.  Instead of creating a gate to check for zero division at each financial 
            ratio, should I do the error checking as above...  Create a flag that stores the years of missing financial data 
            and then only grade based on the years available or skip.  In line checking has less overall code though...
            2/4/22 - Necessary to flag each year individually with 1 or 0.  I have to prepare for spotty data.         
            """

            #2/5/22 - Created these two dictionaries to flag 1 for value available and 0 for not available
            yrsb = {}
            for key in [y for y in bdict.keys()]:
                temp_list = []
                for x in bdict[key]:
                    if float(x) == 0:
                        temp_list.append(0)
                    else:
                        temp_list.append(1)
                yrsb[key] = temp_list

            yrsi = {}
            for key in [y for y in idict.keys()]:
                temp_list = []
                for x in idict[key]:
                    if float(x) == 0:
                        temp_list.append(0)
                    else:
                        temp_list.append(1)
                yrsi[key] = temp_list

            #The following two file writes are temporary for checking if lists output correctly
            with open("tempyrsb.txt", 'w') as tempyrsb:
                tempyrsb.truncate()
                json.dump(yrsb, tempyrsb, indent=5, separators=(", ", ": "), sort_keys=False)
                tempyrsb.close()

            with open("tempyrsi.txt", 'w') as tempyrsi:
                tempyrsi.truncate()
                json.dump(yrsi, tempyrsi, indent=5, separators=(", ", ": "), sort_keys=False)
                tempyrsi.close()

            # This dictionary flags years missing in balance sheets
            fl_yrsb = {}
            for key in [y for y in bdict.keys()]:
                flag = 0
                for x in bdict[key]:
                    if float(x) == 0:
                        flag += int(1)
                fl_yrsb[key] = flag

            # This dict flags years missing
            fl_yrsi = {}
            for key in [y for y in idict.keys()]:
                flag = 0
                for x in idict[key]:
                    if float(x) == 0:
                        flag += int(1)
                fl_yrsi[key] = flag

            # This is a counter to display number of fields with full values and write to grade sheet
            count_temp = 0
            for key in fl_yrsb.keys():
                if fl_yrsb[key] == 0:
                    count_temp += 1

            f.write("The Balance Sheet has:   ::  " + str(count_temp) + " full value fields\n")

            # This is a counter to display number of fields with full values and write to grade sheet
            count_temp = 0
            for key in fl_yrsi.keys():
                if fl_yrsi[key] == 0:
                    count_temp += 1

            f.write("The Income Statement has:  ::  " + str(count_temp) + " full value fields\n")
            f.write(brl + brn + brn)

            finrat_dict = {}  # Dictionary storing financial ratio information for available years "Title": []

            # List of financial ratios as a chronological list from ttw to yp-2
            """
            GD - 1/29/22 - Switching from using flags and check at each ratio, to storing all financial
            ratios for available years into a dictionary.  
            Easier to consolidate grading script and view information for analysis.
            
            GD - 2/4/22 - Altering this area to create a temporary list to act as a true/false switch board for available
            years available to parse.
            """
            # Temporary container for qualifying each ratio's data availability
            temp_list = []

            # Current  Ratio - Higher Better
            temp_list = list(map(lambda x, y: bool(x == y), yrsb["Total Current Assets"], yrsb["Total Current Liabilities"]))
            cr_list = []
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    cr_list.append(b["Total Current Assets"][y] /
                                   b["Total Current Liabilities"][y])
                else:
                    cr_list.append(None)

            finrat_dict["Current Ratio"] = cr_list
            f.write("Current Ratios:  :: " + str(cr_list) + "\n")

            # acid-test ratio
            # quick - ratio higher better

            ac_list = []
            temp_list = list(map(lambda x, y, z: bool(x == y and y == z), yrsb["Total Current Assets"],
                                 yrsb["Inventory"],
                                 yrsb["Total Current Liabilities"]))
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    ac_list.append(((b["Total Current Assets"][y] -  b["Inventory"][y]) /
                                    b["Total Current Liabilities"][y]))
                else:
                    ac_list.append(None)

            finrat_dict["Acid Test Ratio"] = ac_list
            f.write("Acid Test Ratio:  :: " + str(ac_list) + "\n")



            temp_list = list(map(lambda x, y: bool(x == y), yrsb["Cash"], yrsb["Total Current Liabilities"]))
            c_list = []
            # Cash Ratio - potentially more important for small companies or new companies
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    c_list.append(b["Cash"][y] / b["Total Current Liabilities"][y])
                else:
                    c_list.append(None)

            finrat_dict["Cash Ratio"] = c_list
            f.write("Cash Ratio:  :: " + str(c_list) + "\n")

            temp_list = list(map(lambda x, y: bool(x == y), yrsb["Total Liabilities"], yrsb["Total Assets"]))
            dr_list = []
            # Debt Ratio - "Investopedia general .4 or lower is better, .6 or higher may make it difficult to borrow"
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    dr_list.append(b["Total Liabilities"][y] / b["Total Assets"][y])
                else:
                    dr_list.append(None)

            finrat_dict["Debt Ratio"] = dr_list
            f.write("Debt Ratios:  :: " + str(dr_list) + "\n")

            # Debt to Equity Ratio - Ivestopedia not be above 2.0, overleveraging and not taking advantage of equity
            temp_list = list(map(lambda x, y: bool(x == y), yrsb["Total Stockholder Equity"], yrsb["Total Liabilities"]))
            dte_list = []
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    dte_list.append(b["Total Liabilities"][y] / b["Total Stockholder Equity"][y])
                else:
                    dte_list.append(None)

            finrat_dict["Debt to Equity Ratio"] = dte_list
            f.write("Debt to Equity Ratio:  :: " + str(dte_list) + "\n")

            # Operating Cash Flow - A clearer picture of just net sales minus operating expenses, excluding non-cash items
            temp_list = list(map(lambda x, y: bool(x == y), yrsb["Total Current Liabilities"], yrsi["Operating Income"]))
            ocflo_list = []
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    ocflo_list.append(inc1["Operating Income"][y] / b["Total Current Liabilities"][y])
                else:
                    ocflo_list.append(None)

            finrat_dict["Operating Cash Flow"] = ocflo_list
            f.write("Operating Cash Flow Ratios:  :: " + str(ocflo_list) + "\n")

            # Interest coverage ratio, ability to pay off interest from fash flows
            temp_list = list(map(lambda x, y: bool(x == y), yrsi["Operating Income"], yrsi["Interest Expense"]))
            icr_list = []
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    icr_list.append(inc1["Operating Income"][y] /  inc1["Interest Expense"][y])
                else:
                    icr_list.append(None)

            finrat_dict["Interest Coverage Ratio"] = icr_list
            f.write("Interest Coverage Ratio:  :: " + str(icr_list) + "\n")

            # Return on assets - sector specific 5% generally good on companys whose operating is machinery/labor intensive
            temp_list = list(map(lambda x, y: bool(x == y), yrsi["Net Income"], yrsb["Total Assets"]))
            roa_list = []
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    roa_list.append(inc1["Net Income"][y] / b["Total Assets"][y])
                else:
                    roa_list.append(None)

            finrat_dict["Return On Assets Ratio"] = roa_list
            f.write("Return On Assets Ratios: :: " + str(roa_list) + "\n")

            # Return on equity - or return on net assets,
            temp_list = list(map(lambda x, y: bool(x == y), yrsb["Total Stockholder Equity"], yrsi["Net Income"]))
            roe_list = []
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    roe_list .append(inc1["Net Income"][y] / b["Total Stockholder Equity"][y])
                else:
                    roe_list.append(None)

            finrat_dict["Return On Equity Ratio"] = roe_list
            f.write("Return on Equity Ratios:  :: " + str(roe_list) + "\n")

            """
            2/5/22 - GD
            Some of the financial document information is irregular.  Some years missing some values and then a 
            different year missing different values.  Example: AMD - book value per share calculation
            """
            # Book Value Per Share or shareholders equity divided by shares outstanding
            temp_list = list(map(lambda x, y, z, i: bool(x == y and y == z and z == i), yrsb["Treasury Stock"],
                                 yrsb["Other Stockholder Equity"], yrsb["Total Stockholder Equity"], yrsb["Common Stock"]))
            bvps_list = []
            for x, y in zip(temp_list, range(len(temp_list))):
                if x:
                    bvps_list.append((b["Total Stockholder Equity"][y] -
                                     b["Treasury Stock"][y] - b["Other Stockholder Equity"][y]) /
                                         b["Common Stock"][y])
                else:
                    bvps_list. append(None)

            finrat_dict["Book Value Per Share"] = bvps_list
            f.write("Book Value Per Share Ratios:  :: " + str(bvps_list) + brn + "\n\n")

            temp_list = []  # Cast the ratio lists from dictionary for grading, I know not necessary to declare in Python

            # Current Ratio Grade
            f.write("::  ::CURRENT RATIO::  ::\n" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Current Ratio"]
            self.grade_tool.tp += 3
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Data in CURRENT RATIO" + brn)
                    pass
                elif float(temp_list[0]) > float(1.20):
                    gv += 1.5
                    f.write("CURRENT RATIO: (" + str(temp_list[0]) + ") > 1.2 ::::: + 1.5 POINTS\n")
                    f.write(brn)
                for x in range(len(temp_list)-1):
                    if temp_list[x] == None or temp_list[x + 1] == None:
                        f.write("Missing Data - CURRENT RATIO" + brn)
                        f.write("Year: " + str(temp_list[x]) + " - or - " + str(temp_list[x + 1]))
                        pass
                    elif float(temp_list[x+1]) < float(temp_list[x]):
                        gv += .5
                        f.write("For Range: " + str(x) + brn)
                        f.write(str(temp_list[x+1]) +" < " + str(temp_list[x]) + "== TRUE" + brn)
                        f.write(".5 POINTS ADDED TO GV")
                        f.write("CURRENT GV:  " + str(gv))
                    else:
                        f.write("Not Increasing YoY - No Points \n")

            f.write(brn*2)

            # Acid-Test Ratio Grade
            f.write("::  ::ACID TEST:  ::" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Acid Test Ratio"]
            self.grade_tool.tp += 3
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Data in ACID TEST" + brn)
                    pass
                elif float(temp_list[0]) > float(1.0):
                    gv += 1.5
                    f.write("ACID TEST RATIO (" + str(temp_list[0]) + ") > 1.0 ::::: + 1.5 POINTS\n")
                    f.write(brn)
                for x in range(len(temp_list)-1):
                    if temp_list[x] == None or temp_list[x + 1] == None:
                        f.write("Missing Data om ACOD TEST" + brn)
                    elif float(temp_list[x+1]) < float(temp_list[x]):
                        gv += .5
                        f.write("For Range: " + str(x) + brn)
                        f.write(str(temp_list[x+1]) +" < " + str(temp_list[x]) + "== TRUE" + brn)
                        f.write(".5 POINTS ADDED TO GV" + brn)
                    else:
                        f.write("POINTS NOT ADDED TO GV - ACID TEST" + brn)

            f.write("Ending GV: " + str(gv) + brn)
            f.write(brn*2)

            # Cash Ratio
            f.write("::  ::CASH RATIO:  ::" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Cash Ratio"]
            self.grade_tool.tp += 3
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Values - Cash Ratio:" + brn)
                    pass
                elif float(temp_list[0]) > float(1.0):
                    gv += 1.5
                    f.write("Cash Ratio > 1.0 ::::: + 1.5 POINTS\n")
                else:
                    f.write("Cash Ratio < 1.0 ::::: + 0 POINTS\n")
                for x in range(len(temp_list)-1):
                    if temp_list[x] == None or temp_list[x + 1] == None:
                        f.write("Missing Data Values in Cash Ratio")
                    elif float(temp_list[x+1]) < float(temp_list[x]):
                        gv += .5
                        f.write(".5 awarded for count: :: " + str(count) + "\n")
                        count += 1

            f.write("Ending GV: " + str(gv) + brn +brn)
            f.write(brn)

            # Debt Ratio
            f.write("::  ::DEBT RATIO:  ::" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Debt Ratio"]
            self.grade_tool.tp += 1.5
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Data in DEBT RATIO" + brn)
                    pass
                elif float(temp_list[0]) < float(.40):
                    gv += 1.5
                    f.write("Debt Ratio < .40 ::::: + 1.5 POINTS\n")
                else:
                    f.write("No Points Awarded - Debt Ratio > .40\n")

            f.write(brn*2)

            # Debt to Equity Ratio
            f.write("::  ::DEBT TO EQUITY RATIO:  ::" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Debt to Equity Ratio"]
            self.grade_tool.tp += 3
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Data in DEBT TO EQUITY RATIO" + brn)
                    pass
                elif float(temp_list[0]) < float(1.0):
                    gv += 1.5
                    f.write("Debt to Equity < 1.0 ::::: + 1.5 POINTS\n")
                for x in range(len(temp_list)-1):
                    if temp_list[x] == None or temp_list[x + 1]:
                        f.write("Missing Data in DEBT TO EQUITY RATIO" + brn)
                    elif float(temp_list[x+1]) < float(temp_list[x]):
                        gv += .5
                        f.write(".5 awarded for count: :: " + str(count) + "\n")
                        count += 1
                    else:
                        f.write("Additional .5 Points Not Rewarded")

            f.write("Endinng GV: " + str(gv))
            f.write(brn*2)

            # Operating Cash Flow Ratio
            f.write("::  ::OPERATING CASH FLOW:  ::" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Operating Cash Flow"]
            self.grade_tool.tp += 3
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Data in OPERATING CASH FLOW:" + brn)
                    pass
                elif float(temp_list[0]) > float(1.0):
                    gv += 1.5
                    f.write("Operating Cash Flow > ::::: + 1.5 POINTS\n")
                for x in range(len(temp_list)-1):
                    if temp_list[x] or temp_list[x + 1] == None:
                        f.write("Missing Data in OPERATING CASH FLOW")
                        pass
                    elif float(temp_list[x+1]) > float(temp_list[x]):
                        gv += .5
                        f.write(".5 awarded for count: :: " + str(count) + "\n")
                        count += 1
                    else:
                        count += 1
                        f.write("No Points Awarded For Count: :: " + str(count) + "\n")


            f.write("Ending GV: " + str(gv) + brn)
            f.write(brn*2)

            # Interest Coverage Ratio
            f.write("::  ::INTEREST COVERAGE RATIO:  ::" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Interest Coverage Ratio"]
            self.grade_tool.tp += 3
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Data in Coverage Rato" + brn)
                    pass
                elif float(temp_list[0]) > float(1.0):
                    gv += 1.5
                    f.write("Interest Coverage Ratio > 1.0 ::::: + 1.5 POINTS\n")
                for x in range(len(temp_list)-1):
                    if temp_list[x] == None or temp_list[x + 1] == None:
                        f.write("Missing Documentation in Coverage ratio" + brn)
                        pass
                    elif float(temp_list[x+1]) > float(temp_list[x]):
                        gv += .5
                        f.write(".5 awarded for count: :: " + str(count) + "\n")
                        count += 1
                    else:
                        f.write("Not Awarded .5 Points for count: :: " + str(count) + brn)
                        count += 1

            f.write("\nEnding GV: " + str(gv))
            f.write(brn*2)

            # Return on Assets
            f.write("::  ::RETURN ON ASSETS:  ::" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Return On Assets Ratio"]
            self.grade_tool.tp += 3
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Data in RETURN ON ASSETS" + brn)
                elif float(temp_list[0]) > float(.15):
                    gv += 1.5
                    f.write("Return On Assets Ratio > .15 ::::: + 1.5 POINTS\n")
                for x in range(len(temp_list)-1):
                    if temp_list[x] == None or temp_list[x + 1] == None:
                        f.write("Missing Data in RETURN ON ASSETS" + brn)
                        pass
                    elif float(temp_list[x+1]) > float(temp_list[x]):
                        gv += .5
                        f.write(".5 awarded for count: :: " + str(count) + "\n")
                        count += 1
                    else:
                        f.write("Not Awarded .5 Points for count: :: " + str(count) + brn)
                        count += 1

            f.write("Ending GV: " + str(gv))
            f.write(brn*2)

            # Return on Equity
            f.write("::  ::RETURN ON EQUITY:  ::" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Return On Equity Ratio"]
            self.grade_tool.tp += 3
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Data in RETURN ON EQUITY" + brn)
                    pass
                elif float(temp_list[0]) > float(.15):
                    gv += 1.5
                    f.write("Return On Equity Ratio > .07 ::::: + 1.5 POINTS\n")
                for x in range(len(temp_list)-1):
                    if temp_list[x] == None or temp_list[x + 1] == None:
                        f.write("Missing Data in Return ON EQUITY" + brn)
                        pass
                    elif float(temp_list[x+1]) > float(temp_list[x]):
                        gv += .5
                        f.write(".5 awarded for count: :: " + str(count) + "\n")
                        count += 1
                    else:
                        f.write("Not Awarded .5 Points for count: :: " + str(count) + brn)
                        count += 1

            f.write("Ending GV: " + str(gv))
            f.write(brn*2)

            # Book Value Per Share
            f.write("::  ::BOOK VALUE PER SHARE:  ::" + brn)
            f.write("Beginning GV:  " + str(gv) + brn)
            temp_list = finrat_dict["Book Value Per Share"]
            self.grade_tool.tp += 3
            count = 1
            if temp_list:
                if temp_list[0] == None:
                    f.write("Missing Data in BOOK VALUE PER SHARE" + brn)
                    pass
                elif float(temp_list[0]) < float(3.0):
                    gv += 1.5
                    f.write("Book Value Per Share < 3.0 ::::: + 1.5 POINTS\n")
                for x in range(len(temp_list)-1):
                    if temp_list[x] == None or temp_list[x + 1] == None:
                        f.write("Missing Data in BOOK VALUE PER SHARE"+ brn)
                        pass
                    elif float(temp_list[x+1]) > float(temp_list[x]):
                        gv += .5
                        f.write(".5 awarded for count: :: " + str(count) + "\n")
                        count += 1
                    else:
                        f.write("Not Awarded .5 Points for count: :: " + str(count) + brn)

            f.write("\n\nEND OF SECTION 4: FINANCIAL RATIOSG\n" + brl + (brn*2))
            f.write("AROUND LINE 1015\n\n")
            f.write(brn + brl + brn + brl + brn + "POINTS AWARDED / TOTAL POINTS UP TO SECTION 4\n")
            f.write("POINTS AWARDED: " + str(gv) + " / " + str(self.grade_tool.tp) + " = TOTAL POINTS\n")
            f.write("DECIMAL VALUE == " + str((gv / self.grade_tool.tp)))
            f.write(brn + brl + (brn*2))


            f.write(brl + "\nBEGINNING SECTION 5: ANALYST UPGRADE/DOWNGRADE" + brn + brl + (brn*2))

            # Storing gv in a function attribute grade_tool.gv
            self.grade_tool.gv = gv

            # This is the weighted value of the grade at 75% of the total possible grade

            # ar_list = Analyst Review List - storing total analyst upgrades/downgrades
            ar_lists = []
            ar_dict = []
            ar_graderaw = 0
            ar_gr_denom = 0
            ar_gr_final = 0

            with open("ardata.json", 'r') as arsheets:
                ardata = json.load(arsheets)
                ardata_dict = ardata
                ar_lists.append([ardata_dict["pageViews"][keys] for keys in ardata_dict["pageViews"] if
                                 not str(ardata_dict["pageViews"][keys]).isnumeric()])
                ar_dict.append([x for x in [ardata_dict["upgradeDowngradeHistory"]["history"]]])
                ar_dict_strip = ar_dict[0][0]

                arsheets.close()

            # This is storing ar_lists of pageviews in a function variable
            self.grade_tool.ar_list = ar_lists

            # This is storing the dictionary of analyst reviews data in a function variable
            self.grade_tool.ar_dict_strip = ar_dict_strip

            # For every good-great rating +2 to ar_graderaw, +1 for neutral
            for x in ar_dict_strip:
                if x["epochGradeDate"] > (time.time() - 31536000):
                    if str(x["toGrade"]) == "Buy" or str(x["toGrade"]) == "Strong Buy" or \
                            str(x["toGrade"]) == "Overweight" or str(x["toGrade"]) == "Market Perform" or \
                            str(x["toGrade"]) == "Outperform":
                        f.write(str(x["firm"]) + "  :::::  " + str(x["toGrade"]) + "  ::")
                        ar_graderaw += 2
                        f.write(str("Analyst Grade Points ::::: + 2 POINTS  ::\n"))
                    elif str(x["toGrade"]) == "Neutral" or str(x["toGrade"]) == "Hold" or \
                            str(x["toGrade"]) == "Perform" or str(x["toGrade"]) == "Equal-Weight":
                        f.write(str(x["firm"]) + "  :::::  " + str(x["toGrade"]) + "  ::")
                        ar_graderaw += 1
                        f.write(str("Analyst Grade Points ::::: + 1 POINT  ::\n"))

                    else:
                        continue
                else:
                    continue

            f.write(str(gv) + " / " + str(self.grade_tool.tp) + "\n\n")
            f.write(brl + brn + "Line 1033" + brn + brl)
            f.write((brn*2) + brl + brn)
            f.write("END OF SECTION 5: ANALYST UPGRADE/DOWNGRADE" + brn + brl + (brn*3))

            f.write(brl + brn + "BEGIN SECTION 6: GRADES AND WEIGHTS\n" + brl + (brn*3))

            # A 'bonus' to the analyst rating points if the market short/mid/longterm trend is upwards
            for x in ar_lists:
                if x == "UP":
                    ar_graderaw += 1
                else:
                    continue

            """
            2/3/22 - GD
            How to weight the grading system and award points is still a work in progress.  Now that I have finished the
            file write portion for Grade Sheets, I can analyze how the grading system is working and alter the system
            as necessary.  For now, I believe I am going to stick to the following weights:
            
            Analyst Ratings: 25%
            All Other Sections: 75%
            """

            # Calculating the total number of analyst ratings within a date range and making denominator
            ar_gr_denom = int(len([x for x in ar_dict_strip if x["epochGradeDate"] >= time.time() - 31536000]))

            # The final grade for analysts - percentage of positive ratings to overall ratings
            ar_gr_final = ar_graderaw / ar_gr_denom

            # Storing the final grade in a function attribute
            self.grade_tool.ar_gr_final = ar_gr_final

            f.write(str(ar_graderaw) + " / " + str(ar_gr_denom * 2) + "\n")

            # Storing decimal of gv /tp
            dec_gr = gv / self.grade_tool.tp

            # Need to change this 2/1/22 - This only makes sense if the grades are weighted by section and given a boost
            # When the analyst section is more positive than not.
            if ar_gr_final >= .55 and ar_gr_final <= .75:
                f.write("\nGRADE AWARDED 5% DUE TO ANALYST RATINGS" + brn + brl + (brn*2))
                if dec_gr <= .95:
                    dec_gr += .05
                elif dec_gr > .95:
                    dec_gr = 1.00

            if ar_gr_final > .75:
                f.write("\nGRADE AWARDED 7% DUE TO ANALYST RATINGS" + brn + brl + (brn*2))
                if dec_gr <= .93:
                    dec_gr += .07
                elif dec_gr > .93:
                    dec_gr = 1.00

            if ar_gr_final < .50:
                f.write("\nGRADE REDUCED BY 5% DUE TO ANALYST RATINGS" + brn + brl + (brn*2))
                if dec_gr >= .64:
                    dec_gr -= .05

            # grade here will store the decimal value of the fraction gv/tp
            self.grade_tool.g = dec_gr
            self.grade_tool.erlist = erlist

            # I am creating this variable to house the A, B, C value until I pass it to the functions attribute
            tg = []

            # Overall Grade Scale
            if int(self.grade_tool.g) >= .94:
                tg.append("A")
            elif int(self.grade_tool.g) < .94 and self.grade_tool.g >= .90:
                tg.append("AB")
            elif int(self.grade_tool.g) < .90 and self.grade_tool.g>= .84:
                tg.append("B")
            elif int(self.grade_tool.g) < .84 and self.grade_tool.g>= 80:
                tg.append("BC")
            elif int(self.grade_tool.g) < .80 and self.grade_tool.g>= .74:
                tg.append("C")
            elif int(self.grade_tool.g) < .74 and self.grade_tool.g>= .70:
                tg.append("CD")
            elif int(self.grade_tool.g) < .70 and self.grade_tool.g>= 64:
                tg.append("D")
            elif int(self.grade_tool.g) < .64:
                tg.append("F")

            self.grade_tool.grade = tg[0]

            f.write((brn*2) + ((brl+brn)*2))
            f.write(brn)
            f.write("GRADE IS: ::::: " + str(tg[0]) + brn + brn + ((brl+brn)*2))
            f.write("\nEND OF GRADE SHEET")

        f.close()

        return gv


    def parsetool(self):

        # bsheets parses 4 separate dictionaries of 'balance sheet financials' : value pairs and combines them into one list
        # the list of arrays only stores the 4 values in chronological order but no 'key' is carried over
        self.parsetool.bsheets = []

        # same as bsheets but for the income statement variables
        self.parsetool.isheets = []

        # function attribute holding
        self.parsetool.valdict = {}

        # This is going to hold the sector value pulled from sectordata.json
        self.parsetool.sector = ""
        self.parsetool.industry = ""

        try:
            with open("sectordata.json", 'r') as sd:
                self.parsetool.sector = dictpull(json.load(sd), "Sector")
                print(str(self.parsetool.sector))
                sd.close()

        except Exception as Er:
            print("try Exception dictpull - sector")
            print(Er)

        try:
            with open("sectordata.json", 'r') as sd:
                self.parsetool.industry = dictpull(json.load(sd), "Industry")
                print(str(self.parsetool.sector))
                sd.close()

        except Exception as Er:
            print("try Exception dictpull - industry")
            print(Er)

        # storing historical valuation information
        # 1/30/22 - Turns out that the information pulled from this API is spotty at best, most often ends up
        # with Empty data, may remove
        with open("valdata.json", 'r') as valsheets:
            vals_data = json.load(valsheets)
            val_dict = dict(vals_data)
            self.parsetool.valdict = val_dict
            valsheets.close()

        # storing analyst review data for parsing, should be possible to avoid this with function variables in fetch tool
        with open("ardata.json", 'r') as arsheets:
            ardata = json.load(arsheets)
            arsheets.close()

        # Open Balancesheets file, strip out values for 4 years and store in a list of lists
        with open("balancesheets.json", 'r') as bsheets:
            bsheets_data = json.load(bsheets)

            bsheets_zip = list(
                                zip(
                                    [bsheets_data["annual_historical_balance_sheets"][0][keys] for keys in
                                     bsheets_data["annual_historical_balance_sheets"][0]],
                                    [bsheets_data["annual_historical_balance_sheets"][1][keys] for keys in
                                     bsheets_data["annual_historical_balance_sheets"][1]],
                                    [bsheets_data["annual_historical_balance_sheets"][2][keys] for keys in
                                     bsheets_data["annual_historical_balance_sheets"][2]],
                                    [bsheets_data["annual_historical_balance_sheets"][3][keys] for keys in
                                     bsheets_data["annual_historical_balance_sheets"][3]],
                                )
            )
            self.parsetool.bsheets = bsheets_zip
            bsheets.close()

        # Open incomestatements file, strip out values for 4 years and store in a list of lists
        with open("incomestatements.json", 'r') as isheets:
            isheets_data = json.load(isheets)

            isheets_zip = list(
                                zip(
                                    [isheets_data["annual_historical_income_statements"][0][keys] for keys in
                                     isheets_data["annual_historical_income_statements"][0]],
                                    [isheets_data["annual_historical_income_statements"][1][keys] for keys in
                                     isheets_data["annual_historical_income_statements"][1]],
                                    [isheets_data["annual_historical_income_statements"][2][keys] for keys in
                                     isheets_data["annual_historical_income_statements"][2]],
                                    [isheets_data["annual_historical_income_statements"][3][keys] for keys in
                                     isheets_data["annual_historical_income_statements"][3]],
                                )
            )
            self.parsetool.isheets = isheets_zip
            isheets.close()

            isheets_keys = []
            bsheets_keys = []

            print("Line 146")

            # This is necessary, because it is storing a list of keys for the creation of the new dictionaries
            for keys in isheets_data["annual_historical_income_statements"][0]:
                isheets_keys.append(keys)

            for keys in bsheets_data["annual_historical_balance_sheets"][0]:
                bsheets_keys.append(keys)

            bsheets_dict = {}
            for x in range(len(bsheets_keys)):
                bsheets_dict[bsheets_keys[x]] = self.parsetool.bsheets[x]

            isheets_dict = {}
            for x in range(len(isheets_keys)):
                isheets_dict[isheets_keys[x]] = self.parsetool.isheets[x]

            self.parsetool.idict = isheets_dict
            self.parsetool.bdict = bsheets_dict

            print("Line 166")
            """
            1/19/22 - GD
            Adding This Section to write isheets and bsheets information to file with a ticker symbol prefix.  I need to 
            analyze and plan for differences in how balance sheets and income statements are formulated for different types 
            of stocks.  Tech Company vs. textile vs. medical/pharma vs. financial, etc.  The initial grade system was based on
            Etsy, which isn't indicative of the other stock sectors/business types.  Meaning, the other business types
            need to have a different financial structure in order to be successful.  If I grade all stocks on Etsy's debt
            /asset structure, then it isn't as accurate an indicator of future success.
            """

            # Paths for JSON files
            """
    
            Writing the dictionaries to files to make it easier to error check the grading system, should be 
            removed in the future.  Information is stored in MySQL database already.
            
            """
            path_twodir = "C:/SSC/SSC_BDICT_IDICT"
            pathdir = "C:/SSC/SSC_JSON"
            path_valdir = "C:/SSC/VALJSON"

            # Make dir if none exists, open
            def safe_open_w(path):

                """
                Open "path" for writing, creating any parent directories as needed.
                """

                os.makedirs(os.path.dirname(path), exist_ok=True)
                return open(path, 'w')

            # Prefixes for file names
            pref = pathdir + '/' + str(sscf.get_financials.ticker_entryf) + str(int(str(time.time()).replace('.', '')))
            pref_2 = path_twodir + '/' + str(sscf.get_financials.ticker_entryf) + str(int(str(time.time()).replace('.', '')))
            pref_3 = path_valdir + '/' + str(sscf.get_financials.ticker_entryf) + str(int(str(time.time()).replace('.', '')))
            in_post = pref + '_inc_' + '.json'  # Using this to double check that names remain constant across multiple tick
            bal_post = pref + '_bal_' + '.json'
            bdict_post = pref_2 + '_bdict_' + '.json'  # Using this to check grading system and that data chronological
            idict_post = pref_2 + '_idict_' + '.json'
            val_post = pref_3 + '_val_' + '.json'

            # Writing financial valuations fetch from API to file (EPS, P/E, P/Sales) - 1/29 found out the API sends Null
            # Information, no longer necessary, need to remove in future
            with safe_open_w(val_post) as f:
                json.dump(val_dict, f, indent=5, separators=(", ", ": "), sort_keys=False)
                f.close()

            # Writing a copy of JSON = idict to file to check against gradesheets
            with safe_open_w(in_post) as f:
                idict_renum = {}
                for x in range(len(self.parsetool.idict.keys())):
                    idict_renum[x] = [x for x in self.parsetool.idict.keys()][x]

                json.dump(idict_renum, f, indent=5, separators=(", ", ": "), sort_keys=False)
                f.close()

            # Writing dictionary of keys by index : key pair
            with safe_open_w(bal_post) as f:
                bdict_renum = {}
                for x in range(len(self.parsetool.bdict.keys())):
                    bdict_renum[x] = [x for x in self.parsetool.bdict.keys()][x]
                json.dump(bdict_renum, f, indent=5, separators=(", ", ": "), sort_keys=False)
                f.close()

            # Writing idict to file
            with safe_open_w(idict_post) as f:
                json.dump(isheets_dict, f, indent=5, separators=(", ", ": "), sort_keys=False)
                f.close()

            # Writing bdict to file
            with safe_open_w(bdict_post) as f:
                json.dump(bsheets_dict, f, indent=5, separators=(", ", ": "), sort_keys=False)
                f.close()

        return bsheets_zip, isheets_zip, isheets_dict, bsheets_dict

class Test_ParseToolSSC_dictpull(unittest.TestCase):
    def test_dictpull(self):
        mock_arg = unittest.mock.MagicMock()
        type(mock_arg).value = unittest.mock.MagicMock(return_value=dict({"TEST LEVEL A": {"TEST LEVEL B": "TLB VAL1",
                                                                          "TEST LEVEL B2": "TLB VAL2",
                                                                          "TEST LEVEL B3": {"TEST LEVEL C":
                                                                            ["TLC VAL1", {"TEST FINAL": "TRUE"}]}}}))
        test_headerdictpull = "TEST FINAL"
        print(test_headerdictpull)
        print(mock_arg.value())
        print(dictpull(mock_arg.value(), test_headerdictpull))


        #self.assertEqual("True", test_dictpullresult, "Review: 'test_dictpull'")



if __name__ == '__main__':
    unittest.main()