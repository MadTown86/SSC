import gradesheetprintssc


class GradeFinRatioSSC(gradesheetprintssc.GradeSheetPrintSSC):
    def grade_finratiossc(self, ticker, parsecombo, uniqueid, awardsystem):
        """
        Total Point Max = 36
        :param ticker:
        :param parsecombo:
        :param uniqueid:
        :param awardsystem:
        :return:
        """

        # Current  Ratio - Higher Better
        #   1.5-3.0 + 1
        #   0
        # quick - ratio higher better
        #   around or above 1
        # Cash Ratio - potentially more important for small companies or new companies
        #   greater than 1
        # Debt Ratio - "Investopedia general
        #   .4 or lower is better, .6 or higher may make it difficult to borrow"
        # Debt to Equity Ratio - Investopedia not be above 2.0, over leveraging and not taking advantage of equity
        #   2-2.5
        # Operating Cash Flow - A clearer picture of just net sales minus operating expenses, excluding non-cash items
        #
        # Interest coverage ratio, ability to pay off interest from fash flows
        #   3 or better
        # Return on assets - sector specific 5% generally good on company's whose operating is machinery/labor-intensive
        #   5% good - 20% great
        # Return on equity - or return on net assets,
        #   Sector specific, will need to grade based on sector average
        # Book Value Per Share or shareholders equity divided by shares outstanding
        #   Value under 1 could indicate undervalued stock

        try:
            localvardict = parsecombo['finratiodict']
            runningtotalbin = {}

            fingradedict = {
                "Current Ratio": lambda finval: pg if finval > 1.4 else pn if 1.4 > finval >= 1 else pb,
                "Acid Test Ratio": lambda finval: pg if finval >= .9 else pb,
                "Cash Ratio": lambda finval: pg if finval > 1 else pb,
                "Debt Ratio": lambda finval: pg if finval <= .4 else pb,
                "Debt To Equity Ratio": lambda finval: pg if finval <= 2.0 else pn if 2.5 <= finval > 2 else pb,
                "Operating Cash Flow": lambda finval: pn,  # TODO: need to update to Sector specific grading
                "Interest Coverage Ratio": lambda finval: pg if finval >= 3.0 else pn if 3.0 > finval > 1.0 else pb,
                "Return On Assets Ratio": lambda finval: pg if finval >= .20 else pn if .20 > finval >= .05 else pb,
                "Book Value Per Share": lambda finval: pg if finval < 1.0 else pb
            }

            statementdict = {
                "Current Ratio": ["GOOD: > 1.5", "NEUTRAL: 1.4 > X >= 1", "BAD: X < 1"],
                "Acid Test Ratio": ["GOOD: X >= .9", "BAD: X < .9"],
                "Cash Ratio": ["GOOD: X > 1", "BAD: X < 1"],
                "Debt Ratio": ["GOOD: X <= .4", "BAD: X > .4"],
                "Debt To Equity Ratio": ["GOOD: X <= 2.0", "NEUTRAL: 2.5 <= X > 2", "BAD: X < 2"],
                "Operating Cash Flow": ["NOT YET GRADING"],
                "Interest Coverage Ratio": ["GOOD: X >= 3", "NEUTRAL: 1 < X < 3.0", "BAD: X < 1"],
                "Return On Assets Ratio": ["GOOD: X >= .20", "NEUTRAL: .20 > X >= .05", "BAD: X <= .05"],
                "Book Value Per Share": ["GOOD: X < 1", "BAD: X > 1"]
            }

            printerdictssc = {}

            # Main looping construct for grade_finratio, loops by metric
            for rationame in localvardict.keys():
                finratpoints = 0

                pg = awardsystem['FINRATIOS'][rationame]['pointsgood']
                pn = awardsystem['FINRATIOS'][rationame]['pointsneutral']
                pb = awardsystem['FINRATIOS'][rationame]['pointsbad']

                for yearindex in reversed(range(len(localvardict[rationame]))):
                    localpoints = fingradedict[rationame](localvardict[rationame][yearindex])
                    finratpoints += localpoints
                    fintotpoints = pg * len(localvardict[rationame])  # Sets the total

                    keystatement = [rationame, "|", yearindex, "|", localvardict[rationame][yearindex]]
                    valstatement = ["POINTS AWARDED", localpoints, *statementdict[rationame]]
                    printerdictssc[str(keystatement)] = valstatement

                runningtotalbin[rationame] = {'Base Points': fintotpoints, 'Current Points': finratpoints}

            self.setinstancepath(ticker, uniqueid)
            self.setsheetnamesscgr(ticker)
            self.gradeprinterssc(**printerdictssc)
            self.sectionprinttoexcel()
            return self.sectionendprinttoexcel(**runningtotalbin)
        except Exception as er:

            print("Exception in GradeFinRatioSSC: grade_finratiossc: ")
            print(er)


if __name__ == '__main__':
    import gradeparsecombinessc
    import awardsystemssc

    testlogvaridssc = 'NVDA__Y8bdxbfeWiliz3B'
    ticker, uniqueid = testlogvaridssc.split("__")
    AWS = awardsystemssc.AwardSystemSSC()
    awardsystempassin = AWS.fetchawardsystem("Industry", "Sector")

    GPSSC = gradeparsecombinessc.GradeParseCombineSSC()
    gradeparsecombo = GPSSC.gradeparsecombinessc(ticker, uniqueid)

    GFIN = GradeFinRatioSSC()
    GFIN.printprimer("FINRATIO", ticker, uniqueid, "SECTOR", "INDUSTRY")
    GFIN.grade_finratiossc(ticker, gradeparsecombo, uniqueid, awardsystempassin)
