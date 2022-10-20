"""
Create 'hand-made' list of ratios from income statements and balance sheet elements, e.g. "Current Ratio"
"""


class ParseRatioCreateSSC:
    def parseratiocreatesssc(self, incomedictssc, balancedictssc):
        """

        :param incomedictssc: intended for data from ParseIncSSC
        :param balancedictssc: intended for data from ParseBalSSC
        :param incdatqual: may not be needed
        :param baldatqual: may not be needed
        :return:
        """

        try:
            try:
                dictratiossclamb = {
                    "Current Ratio": lambda totalcurrentassetsx, totalcurrentliabilitiesy: totalcurrentassetsx
                    / totalcurrentliabilitiesy
                    if totalcurrentassetsx != 0 and totalcurrentliabilitiesy != 0
                    else 0,

                    "Acid Test Ratio": lambda totalcurrentassetsx, inventoryy, totalcurrentliabilitiesz: (
                        totalcurrentassetsx - inventoryy
                    )
                    / totalcurrentliabilitiesz
                    if totalcurrentassetsx != 0
                    and inventoryy != 0
                    and totalcurrentliabilitiesz != 0
                    else 0,

                    "Cash Ratio": lambda cashx, totalcurrentliabilitiesy: cashx
                    / totalcurrentliabilitiesy
                    if cashx != 0 and totalcurrentliabilitiesy != 0
                    else 0,

                    "Debt Ratio": lambda totalliabilitiesx, totalassetsy: totalliabilitiesx
                    / totalassetsy
                    if totalliabilitiesx != 0 and totalassetsy != 0
                    else 0,

                    "Debt To Equity Ratio": lambda totalstockholderequity, totalliabilities: totalliabilities
                    / totalstockholderequity
                    if totalliabilities != 0 and totalstockholderequity != 0
                    else 0,

                    "Operating Cash Flow": lambda operatingincome, interestexpense: operatingincome
                    / interestexpense
                    if operatingincome != 0 and interestexpense != 0
                    else 0,

                    "Interest Coverage Ratio": lambda netincome, totalassets: netincome
                    / totalassets
                    if netincome != 0 and totalassets != 0
                    else 0,

                    "Return On Assets Ratio": lambda totalstockholderequity, netincome: netincome
                    / totalstockholderequity
                    if netincome != 0 and totalstockholderequity != 0
                    else 0,

                    "Book Value Per Share": lambda treasurystock, otherstockholderquity, totalstockholderquity, commonstock: (
                        totalstockholderquity - treasurystock - otherstockholderquity
                    )
                    / commonstock
                    if commonstock != 0
                    else 0,
                }
            except Exception as er:
                print('Exception in "parseratiocreatessc" - dictratiossclamb')
                print(er)

            dictratiosscverbal = {
                "Current Ratio": ["Total Current Assets", "Total Current Liabilities"],
                "Acid Test Ratio": [
                    "Total Current Assets",
                    "Inventory",
                    "Total Current Liabilities",
                ],
                "Cash Ratio": ["Cash", "Total Current Liabilities"],
                "Debt Ratio": ["Total Liabilities", "Total Assets"],
                "Debt To Equity Ratio": [
                    "Total Stockholder Equity",
                    "Total Liabilities",
                ],
                "Operating Cash Flow": ["Operating Income", "Interest Expense"],
                "Interest Coverage Ratio": ["Net Income", "Total Assets"],
                "Return On Assets Ratio": ["Total Stockholder Equity", "Net Income"],
                "Book Value Per Share": [
                    "Treasury Stock",
                    "Other Stockholder Equity",
                    "Total Stockholder Equity",
                    "Common Stock",
                ],
            }

            finalratiodictssc = {}
            interimratiodictssc = {}

            varnamepulltemplist = {}

            # Loop through ratios
            for key in dictratiossclamb.keys():
                calctemplistforzipper = []

                # Loop through each required variable name for ratio
                for varname in dictratiosscverbal[key]:

                    # Logic test to see if variable name present in income statements or balance sheets
                    if varname in incomedictssc.keys():

                        # Create copy of variable value from income dictionary
                        datatemplistssc = incomedictssc[varname]
                        varnamepulltemplist[str(varname)] = [datatemplistssc]
                        calctemplistforzipper.append(datatemplistssc)
                        continue

                    elif varname in balancedictssc.keys():
                        datatempballistssc = balancedictssc[varname]
                        varnamepulltemplist[str(varname)] = [datatempballistssc]
                        calctemplistforzipper.append(list(datatempballistssc))
                        continue

                interimratiodictssc[key] = calctemplistforzipper

            for ratio in dictratiossclamb.keys():
                resssc = []
                for iteration in list(zip(*interimratiodictssc[ratio])):
                    resssc.append(dictratiossclamb[ratio](*iteration))
                finalratiodictssc[ratio] = resssc

            return finalratiodictssc
        except Exception as er:
            print("Exception in ParseRatioSSC: method 'parseratiocreatessc' ")
            print(er)


if __name__ == "__main__":
    import gradeparsecombinessc

    ticker = "NVDA"
    logidssc = "Y8bdxbfeWiliz3B"
    GS = gradeparsecombinessc.GradeParseCombineSSC()
    parsecombo = GS.gradeparsecombinessc(ticker, logidssc)["NVDA__Y8bdxbfeWiliz3B"]
    PS = ParseRatioCreateSSC()
    incomedictssc = parsecombo["incdat"]
    balancedictssc = parsecombo["baldat"]
    incqualdat = parsecombo["incdatqual"]
    baldatqual = parsecombo["baldatqual"]
    restestssc = PS.parseratiocreatesssc(
        incomedictssc=incomedictssc,
        balancedictssc=balancedictssc,
    )
