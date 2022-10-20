import gradesheetprintssc


class GTLTYoYRatioSSC(gradesheetprintssc.GradeSheetPrintSSC):
    def __init__(self):
        super().__init__()
        self.asratioincreasingsections = ["Net Income", "Gross Margin", "Operating Margin", "Net Margin",
                                          "Gross Profit", "EBIT", "Operating Income", "Net Income From Continuing Ops",
                                          "Income Before Tax", "Research & Development"]
        self.asratiodecreasingsections = ["Selling, General & Administrative", "Other Operating Expenses",
                                          "Interest Expense",
                                          "Total Operating Expenses", "Cost Of Revenue",
                                          "Total Other Income Expense Net"]

        self.printerdictssc = {}

    def grade_gtltyoyratiossc(self, ticker, parsecombo, uniqueid, awardsystem):
        """
        16 * 3 = 48

        :param ticker:
        :param parsecombo:
        :param uniqueid:
        :param awardsystem:
        :return:
        """
        try:
            runningtotalgtlt = {}
            localawardsectiongtlt = awardsystem['INCASRATIO']
            localratiodict = parsecombo['incasratiodict']

            def increaseordecrease(identifier):
                if identifier == "increasing":
                    binser = self.asratioincreasingsections
                else:
                    binser = self.asratiodecreasingsections

                for rationame in binser:
                    respointrunner = 0
                    pointsper = localawardsectiongtlt[rationame]["points"]
                    ratioweight = localawardsectiongtlt[rationame]["weight"]

                    for old_index in range(len(localratiodict[rationame]) - 1, 0, -1):
                        oldyear = localratiodict[rationame][old_index]
                        recenty = localratiodict[rationame][old_index - 1]

                        keyforprint = [str(rationame), "Year", str(localratiodict[rationame].index(recenty)), "|", "Year",
                                       str(localratiodict[rationame].index(oldyear))]

                        if identifier == "increasing":
                            if recenty > oldyear:
                                respointrunner += pointsper
                                inlinesymbol = ">"
                            else:
                                inlinesymbol = "<"
                        else:
                            if recenty < oldyear:
                                respointrunner += pointsper
                                inlinesymbol = ">"
                            else:
                                inlinesymbol = "<"

                        valueforprint = [str(recenty), inlinesymbol, str(oldyear), "POINTS", str(respointrunner),
                                         "POINTVAL",
                                         str(pointsper)]

                        self.printerdictssc[str(keyforprint)] = valueforprint

                    respointrunner *= ratioweight
                    restotpoints = 1 * (len(localratiodict[rationame]) - 1)
                    restotpoints *= ratioweight
                    runningtotalgtlt[rationame] = {"Base Points": restotpoints, "Current Points": respointrunner}

            increaseordecrease("increasing")
            increaseordecrease("decreasing")

            self.setinstancepath(ticker, uniqueid)
            self.setsheetnamesscgr(ticker)
            self.gradeprinterssc(**self.printerdictssc)
            self.sectionprinttoexcel()
            return self.sectionendprinttoexcel(**runningtotalgtlt)
        except Exception as er:
            print("Exception In GTLTRatioYoYSSC: ")
            print(er)


if __name__ == "__main__":
    import gradeparsecombinessc
    import awardsystemssc

    testlogvaridssc = 'NVDA__Y8bdxbfeWiliz3B'
    ticker, uniqueid = testlogvaridssc.split("__")
    AWS = awardsystemssc.AwardSystemSSC()
    awardsystempassin = AWS.fetchawardsystem("Industry", "Sector")

    GPSSC = gradeparsecombinessc.GradeParseCombineSSC()
    gradeparsecombo = GPSSC.gradeparsecombinessc(ticker, uniqueid)['NVDA__Y8bdxbfeWiliz3B']

    GTLT = GTLTYoYRatioSSC()
    GTLT.printprimer("INCASRATIO", ticker, uniqueid, "SECTOR", "INDUSTRY")
    GTLT.grade_gtltyoyratiossc(ticker, gradeparsecombo, uniqueid, awardsystempassin)
