import json

import awardsystemssc
import fetchlogssc
import grade_arssc
import grade_finalssc
import grade_finratiossc
import grade_gtltratioyoyssc
import grade_gtltyoyssc
import grade_valratiossc
import gradeparsecombinessc_sub
import storessc


class GradeCollectionSSC:
    """
    Grade Process
        *Note: Work In Progress
        Different Grading Algorithms
    """

    inst_count_collections: int = 0

    @staticmethod
    def return_inst_count():
        return GradeCollectionSSC.inst_count_collections

    def __init__(self, ticker, parsecombossc, uniqueidssc):
        GradeCollectionSSC.inst_count_collections += 1
        self.grade_cancel: bool = False
        self.totalpointsssc = 0
        self.pointsssc = 0
        self.storeclass = storessc.StoreSSC()
        self.ticker: str = ticker
        self.uniqueidssc = uniqueidssc
        self.parsecombossc = parsecombossc[ticker + "__" + uniqueidssc]
        self.gradesectionone = grade_gtltyoyssc.GTLTYoYSSC()
        self.gradesectiontwo = grade_gtltratioyoyssc.GTLTYoYRatioSSC()
        self.gradesectionthree = grade_valratiossc.GradeValRatioSSC()
        self.gradesectionfour = grade_arssc.GradeArSSC()
        self.gradesectionfive = grade_finratiossc.GradeFinRatioSSC()
        self.finalgrade = grade_finalssc.GradeFinalSSC()
        self.fetchlogcomplete = fetchlogssc.FetchLogSSC()
        self.awardsystem = awardsystemssc.AwardSystemSSC().fetchawardsystem(
            industry=self.parsecombossc["Industry"], sector=self.parsecombossc["Sector"]
        )

    def grade_cancel_flag(self):
        self.grade_cancel = True

    def gradecollectionssc(self):
        pointbin = {}

        # GTLTYoYSSC()
        pointbin["GTLT"] = (
            self.gradesectionone.gtltmetricsgradessc(
                self.ticker, self.parsecombossc, self.uniqueidssc, self.awardsystem
            )
        )

        # GradeFinRatio()
        pointbin["FINRATIOS"] = (
            self.gradesectionfive.grade_finratiossc(
                self.ticker, self.parsecombossc, self.uniqueidssc, self.awardsystem
            )
        )

        # GTLTYoYRatioSSC()
        pointbin["INCASRATIO"] = (
            self.gradesectiontwo.grade_gtltyoyratiossc(
                self.ticker, self.parsecombossc, self.uniqueidssc, self.awardsystem
            )
        )

        # GradeValSSC
        pointbin["VALMETRICS"] = (
            self.gradesectionthree.grade_valratiossc(
                self.ticker, self.parsecombossc, self.uniqueidssc, self.awardsystem
            )
        )

        # GradeArSSC
        pointbin["ARMETRICS"] = (
            self.gradesectionfour.grade_arssc(
                self.ticker, self.parsecombossc, self.uniqueidssc, self.awardsystem
            )
        )

        for key, value in pointbin.items():
            print(f'KEY: {key} ---> VALUE: {value}')

        self.finalgrade.grade_final_ssc(pointbin, self.awardsystem)

        self.storeclass.db_chksetup()

        self.storeclass.log_entry(
            parsecombo=self.parsecombossc,
            grade_ssc=str(self.finalgrade.final_grade_ssc),
            ticker_entry=str(self.ticker),
            points=self.finalgrade.awardedpoints,
            basepoints=self.finalgrade.totalpoints,
        )

        return pointbin


if __name__ == "__main__":
    import gradeparsecombinessc_sub
    import fetchlogssc

    FSS = fetchlogssc.FetchLogSSC()


    testbin_tickers = [
        'MSFT__url_balance__1556069093072__bX6sOpMaQ1UaYNX'
    ]


    def mini_collectiontest(testlogvaridssc):
        pointvarbinssc = []
        ticker, tag, instid, uniqueid = testlogvaridssc.split("__")

        FSS.ssc_fetchlogclear()

        FSS.ssc_fetchlogwrite(fetchstorename=ticker + "__" + uniqueid)

        temp_fetchprint = FSS.ssc_logfetch()
        print(temp_fetchprint)

        print(ticker, uniqueid)
        GS = gradeparsecombinessc_sub.GradeParseCombineSSCSub()
        passindict = GS.gradeparsecombinessc(ticker, uniqueid)
        print(passindict)

        Gcollect = GradeCollectionSSC(ticker, passindict, uniqueid)
        pointvarbinssc = Gcollect.gradecollectionssc()
        print(pointvarbinssc)
        del pointvarbinssc

    for uniquekey in testbin_tickers:
        mini_collectiontest(uniquekey)
