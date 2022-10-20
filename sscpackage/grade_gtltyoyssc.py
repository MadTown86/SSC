"""
Grade the Income Statements
"""
import grade_gtltyoyssc
import gradesheetprintssc


class GTLTYoYSSC(gradesheetprintssc.GradeSheetPrintSSC):
    """
    This class grades the Income Statement and Balance Sheet Statement Data, awarding points when the oldest+1 year is
    greater than the oldest year.

    The point increment awarded is determined by the passed in 'awardsystemssc' that can be altered based on user choice
    and/or altered to reflect the ideal company outlook based on Sector/Industry.
    """
    def __init__(self):
        super().__init__()
        self.sectionname = 'GTLT'
        self.increasingsections = ["Total Revenue", "Net Income", "Gross Margin", "Operating Margin", "Net Margin",
                                   "Gross Profit", "EBIT", "Operating Income", "Net Income From Continuing Ops",
                                   "Income Before Tax", "Research & Development", "Total Assets", "Retained Earnings"]
        self.printerdictssc = {}
        self.gradestore = {}
    try:
        def gtltmetricsgradessc(self, ticker, parsecombossc, uniqueidssc, awardsystemssc):
            """

            :param ticker: Ticker symbol passed in from 'gradecollectionssc'
            :param parsecombossc: A dictionary of financial information, from 'gradeparsecombinessc'
            :param uniqueidssc: A unique id generated and paired with each ticker symbol and stored in shelve and log
            :param awardsystemssc: A default awardsystem, can be changed
            :return:
            """
            runningtotalgtlt = {}
            localawardsectiongtlt = awardsystemssc['GTLT']
            localincdatssc = parsecombossc['incdat']
            localbaldatssc = parsecombossc['baldat']
            localavoidmetricgtltinc = parsecombossc["incdatqual"]
            localavoidmetricgtltbal = parsecombossc["baldatqual"]
            runsectorssc = parsecombossc["Sector"]
            runindustryssc = parsecombossc["Industry"]
            self.printprimer(self.sectionname, ticker, uniqueidssc, runsectorssc, runindustryssc)

            # This is 'pre-screening' the data sets to ensure that variables/data for a certain year are available first
            try:
                def isenoughdatassc(nameval):
                    if nameval in localavoidmetricgtltinc.keys():
                        inlinecount = len(localavoidmetricgtltinc[nameval])
                        if inlinecount >= 2:
                            return nameval, inlinecount, "incdat"
                        else:
                            return False
                    elif nameval in localavoidmetricgtltbal.keys():
                        inlinecount = len(localavoidmetricgtltbal[nameval])
                        if inlinecount >= 2:
                            return nameval, inlinecount, "baldat"
                        else:
                            return False
                    elif nameval in localincdatssc:
                        inlinecount = len(localincdatssc[nameval])
                        return nameval, inlinecount, "incdat"
                    elif nameval in localbaldatssc.keys():
                        inlinecount = len(localbaldatssc[nameval])
                        return nameval, inlinecount, "baldat"
                    else:
                        return False
            except Exception as er:
                print("Exception in 'isenoughdatassc' function: ")
                print(er)

            # Initiates the main grading loop
            try:
                def increasinggtltssc(nameval, count, statement):
                    """
                    The total points awarded for this section should be 39 with default awardsystem in place

                    :param nameval:
                    :param count:
                    :param statement:
                    :return:
                    """
                    # Pulls points to award as 'pointsper' and weight as 'weightind'
                    pointsper = int(localawardsectiongtlt[nameval]["points"])
                    weightind = int(localawardsectiongtlt[nameval]["weight"])
                    respointrunner = 0
                    if statement == "incdat":
                        sourcevalsinc = localincdatssc[nameval]
                        for old_index in range(len(localincdatssc[nameval]) - 1, 0, -1):
                            oldyear = localincdatssc[nameval][old_index]
                            newyear = localincdatssc[nameval][old_index - 1]
                            keyforprint = [nameval, "Year", str(sourcevalsinc.index(newyear)), "|", "Year",
                                           str(sourcevalsinc.index(oldyear))]

                            # With default 'awardsystem' all points awarded are 1
                            if newyear > oldyear:
                                respointrunner += pointsper
                                inlinesymbol = ">"
                            else:
                                inlinesymbol = "<"

                            valueforprint = [newyear, inlinesymbol, oldyear, "POINTS", respointrunner, "POINTVAL",
                                             pointsper]

                            self.printerdictssc[str(keyforprint)] = valueforprint

                        # Optional 'weight' can be attributed to alter overall weight/score of individual metric
                        respointrunner *= weightind
                        restotpoints = 1 * (count - 1)
                        restotpoints *= weightind
                        runningtotalgtlt[nameval] = {"Base Points": restotpoints, "Current Points": respointrunner}

                    elif statement == "baldat":
                        sourcevalsbal = localbaldatssc[nameval]
                        for old_index in range(len(localbaldatssc[nameval]) - 1, 0, -1):
                            oldyear = localbaldatssc[nameval][old_index]
                            newyear = localbaldatssc[nameval][old_index - 1]
                            keyforprint = [nameval, "Year", str(sourcevalsbal.index(newyear)), "|", "Year",
                                           str(sourcevalsbal.index(oldyear))]

                            if newyear > oldyear:
                                respointrunner += pointsper
                                inlinesymbol = ">"
                            else:
                                inlinesymbol = "<"

                            valueforprint = [newyear, inlinesymbol, oldyear, "POINTS", respointrunner, "POINTVAL",
                                             pointsper]

                            self.printerdictssc[str(keyforprint)] = valueforprint

                        respointrunner *= weightind
                        restotpoints = 1 * (count - 1)
                        restotpoints *= weightind
                        runningtotalgtlt[nameval] = {"Base Points": restotpoints, "Current Points": respointrunner}

                    return runningtotalgtlt
            except Exception as er:
                print("Exception in 'increasinggtltssc' : ")
                print(er)

            try:
                for nameval in self.increasingsections:
                    if isenoughdatassc(nameval):
                        valueholderlist = [*isenoughdatassc(nameval)]
                        if len(valueholderlist) == 3:
                            self.gradestore.update(increasinggtltssc(*valueholderlist))
                    else:
                        continue
            except Exception as er:
                print("Exception during Loop Structure in gtltmetricsgrade function: ")
                print(er)

            self.gradeprinterssc(**self.printerdictssc)
            self.sectionprinttoexcel()

            return self.sectionendprinttoexcel(**self.gradestore)
    except Exception as er:
        print("Exception in GTLTYOYSSC: Outermost Scope ")
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

    GTLT = grade_gtltyoyssc.GTLTYoYSSC()
    GTLT.gtltmetricsgradessc(ticker, gradeparsecombo, uniqueid, awardsystempassin)

    # TODO: add testing
