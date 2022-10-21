import gradesheetprintssc


class GradeValRatioSSC(gradesheetprintssc.GradeSheetPrintSSC):
    def __init__(self):
        super().__init__()
        self.gradeprinterdict = {}
        self.limitchecklist = ["Market Cap (intraday)", "Price/Sales (ttm)"]

    def grade_valratiossc(self, ticker, parsecombo, uniqueid, awardsystem):
        # TODO: The ValRatioSSC needs a more in-depth grading mechanism than simple '>' '<' YoY system
        """
        27 Total Base Points - 9 metrics at 1 for 3 year comparisons

        NOTES FOR GRADING:
        Enterprise Value = "Theoretical Measure of a Company's Total Value"
        f(x) = Common Shares + Preferred Shares + Market Value of Debt + Minority Interest - Cash and Equivalents

        Minority Interest = Non-Controlling (Minority) Interest - aka ownership

        :param ticker:
        :param parsecombo:
        :param uniqueid:
        :param awardsystem:
        :return:
        """
        try:
            localvalratiodict = parsecombo["valdat"]
            valratiopointbook = {}

            for rationame in self.limitchecklist:
                pointsper = awardsystem["VALMETRICS"][rationame]["points"]
                weightval = awardsystem["VALMETRICS"][rationame]["weight"]
                respointrunner = 0

                for old_index in range(len(localvalratiodict[rationame]) - 1, 0, -1):
                    oldery = localvalratiodict[rationame][old_index]
                    recenty = localvalratiodict[rationame][old_index - 1]
                    listforkey = [
                        rationame,
                        "YEAR",
                        localvalratiodict[rationame].index(recenty),
                        "|",
                        localvalratiodict[rationame].index(oldery),
                    ]

                    if recenty > oldery:
                        respointrunner += pointsper
                        inlineGVALvar = ">"
                    else:
                        inlineGVALvar = "<"

                    valforgrade = [recenty, inlineGVALvar, oldery, "POINTS", pointsper]
                    self.gradeprinterdict[str(listforkey)] = valforgrade

                valratiopointbook[rationame] = {
                    "Base Points": (pointsper * (len(localvalratiodict) - 1))
                    * weightval,
                    "Current Points": respointrunner * weightval,
                }

            self.setinstancepath(ticker, uniqueid)
            self.setsheetnamesscgr(ticker)
            self.gradeprinterssc(**self.gradeprinterdict)
            self.sectionprinttoexcel()
            return self.sectionendprinttoexcel(**valratiopointbook)
        except Exception as er:
            print("Exception in GradeValRatioSSC: ")
            print(er)


if __name__ == "__main__":
    import gradeparsecombinessc
    import awardsystemssc

    testlogvaridssc = "TSLA__yyXr8pbeOrad9fH"
    ticker, uniqueid = testlogvaridssc.split("__")
    AWS = awardsystemssc.AwardSystemSSC()
    awardsystempassin = AWS.fetchawardsystem("Industry", "Sector")

    GPSSC = gradeparsecombinessc.GradeParseCombineSSC()
    gradeparsecombo = GPSSC.gradeparsecombinessc(ticker, uniqueid)[
        "TSLA__yyXr8pbeOrad9fH"
    ]

    for item in gradeparsecombo["valdat"].items():
        print(item)

    GVAL = GradeValRatioSSC()
    GVAL.printprimer("INCASRATIO", ticker, uniqueid, "SECTOR", "INDUSTRY")
    GVAL.grade_valratiossc(ticker, gradeparsecombo, uniqueid, awardsystempassin)
