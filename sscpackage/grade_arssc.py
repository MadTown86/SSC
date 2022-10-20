import time

import gradesheetprintssc

time.time

SECONDS_PER_YEAR = 365.25 * 24 * 60 * 60

"""
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
"""


class GradeArSSC(gradesheetprintssc.GradeSheetPrintSSC):
    def __init__(self):
        super().__init__()


    def grade_arssc(self, ticker, parsecombo, uniqueid, awardsystemssc):
        try:
            localardict = parsecombo["AR"]
            localawardsys = awardsystemssc["ARMETRICS"]
            runningtally = 0
            total_count_analysts = 0
            printer_sourcebin = {}
            total_count_dict = {}

            for dictnest in localardict:
                if dictnest["epochGradeDate"] > time.time() - SECONDS_PER_YEAR:
                    total_count_analysts += 1
                    if dictnest["toGrade"] in localawardsys.keys():
                        runningtally += localawardsys[dictnest["toGrade"]]["points"]
                        printer_sourcebin[str(dictnest["firm"])] = [dictnest["toGrade"],
                                                                    localawardsys[dictnest["toGrade"]]["points"]]

            total_count_analysts *= localawardsys["Buy"]["points"]

            total_count_dict["ARGRADE"] = {"Base Points": total_count_analysts, "Current Points": runningtally}

            self.setinstancepath(ticker, uniqueid)
            self.setsheetnamesscgr(ticker)
            self.gradeprinterssc(**printer_sourcebin)
            self.sectionprinttoexcel()

            return self.sectionendprinttoexcel(**total_count_dict)
        except Exception as er:
            print("Exception In Grade_ARSSC: grade_arssc: ")
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

    GAR = GradeArSSC()
    GAR.grade_arssc(ticker, gradeparsecombo, uniqueid, awardsystempassin)
