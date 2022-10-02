import json

import awardsystemssc
import grade_arssc
import grade_finalssc
import grade_finratiossc
import grade_gtltratioyoyssc
import grade_gtltyoyssc
import grade_valratiossc
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
        print("GCC8")
        self.storeclass = storessc.StoreSSC()
        self.ticker: str = ticker
        self.uniqueidssc = uniqueidssc
        self.parsecombossc = parsecombossc[ticker + "__" + uniqueidssc]
        print("GCC1")
        self.gradesectionone = grade_gtltyoyssc.GTLTYoYSSC()
        print("GCC2")
        self.gradesectiontwo = grade_gtltratioyoyssc.GTLTYoYRatioSSC()
        print("GCC3")
        self.gradesectionthree = grade_valratiossc.GradeValRatioSSC()
        print("GCC4")
        self.gradesectionfour = grade_arssc.GradeArSSC()
        print("GCC5")
        self.gradesectionfive = grade_finratiossc.GradeFinRatioSSC()
        print("GCC6")
        self.finalgrade = grade_finalssc.GradeFinalSSC()
        print("GCC7")
        self.awardsystem = awardsystemssc.AwardSystemSSC().fetchawardsystem(industry=self.parsecombossc["Industry"],
                                                                            sector=self.parsecombossc["Sector"])

    def grade_cancel_flag(self):
        self.grade_cancel = True

    def gradecollectionssc(self):
        pointbin = []
        try:
            print("GC1")
            # GTLTYoYSSC()
            pointbin.append(self.gradesectionone.gtltmetricsgradessc(self.ticker, self.parsecombossc, self.uniqueidssc,
                                                                     self.awardsystem))
        except Exception as er:
            print("Exception Point: gradecollectionsssc - gtltmetricsgradessc")
            print(er)

        try:
            print("GC2")
            # GradeFinRatio()
            pointbin.append(self.gradesectionfive.grade_finratiossc(self.ticker, self.parsecombossc, self.uniqueidssc,
                                                                    self.awardsystem))
        except Exception as er:
            print("Exception Point: gradecollectionssc - grade_finratiossc")
            print(er)

        try:
            print("GC3")
            # GTLTYoYRatioSSC()
            pointbin.append(self.gradesectiontwo.grade_gtltyoyratiossc(self.ticker, self.parsecombossc, self.uniqueidssc,
                                                                       self.awardsystem))
        except Exception as er:
            print("Exception Point: gradecollectionssc - grade_gtltyoyratiossc")
            print(er)

        try:
            print("GC4")
            # GradeValSSC
            pointbin.append(self.gradesectionthree.grade_valratiossc(self.ticker, self.parsecombossc, self.uniqueidssc,
                                                                     self.awardsystem))
        except Exception as er:
            print("Exception Point: gradecollectionssc - grade_valratiossc")
            print(er)

        try:
            print("GC5")
            # GradeArSSC
            pointbin.append(self.gradesectionfour.grade_arssc(self.ticker, self.parsecombossc, self.uniqueidssc,
                                                              self.awardsystem))
        except Exception as er:
            print("Exception Point: gradecollectionssc - grade_arssc")
            print(er)

        print("GC6")

        try:
            self.finalgrade.grade_final_ssc(pointbin)
        except Exception as er:
            print("Exception in GradeCollectionSSC: attribute 'self.finalgrade.grade_final_ssc'")
            print(er)
        print("GC7")

        try:
            self.storeclass.db_chksetup()
        except Exception as er:
            print(er)
        print("GC8")

        try:
            self.storeclass.log_entry(parsecombo=self.parsecombossc,
                                      grade_ssc=str(self.finalgrade.final_grade_ssc), ticker_entry=str(self.ticker),
                                      points=self.finalgrade.awardedpoints, basepoints=self.finalgrade.totalpoints)
        except Exception as er:
            print("Exception in GradeCollectionSSC: attribute 'storeclass.log_entry' ")
            print(er)
        print("GC10")
        return pointbin


if __name__ == "__main__":
    import gradeparsecombinessc

    testbin_tickers = [
        "AAPL__iUQNePAoVeFQIPV",
        "NVDA__HH12TPwnMth9Tet",
        "GME__AlabRmFaJP9IXEH",
        "GE__DRLihsPscNaTz0Q",
        "FORD__VyjP8walEhZzDRh"
    ]


    def mini_collectiontest(testlogvaridssc):
        pointvarbinssc = []
        ticker, uniqueid = testlogvaridssc.split("__")
        print(ticker, uniqueid)
        print(GradeCollectionSSC.return_inst_count())
        GS = gradeparsecombinessc.GradeParseCombineSSC()
        print(GradeCollectionSSC.return_inst_count())
        passindict = GS.gradeparsecombinessc(ticker, uniqueid)
        Gcollect = GradeCollectionSSC(ticker, passindict, uniqueid)
        pointvarbinssc = Gcollect.gradecollectionssc()
        print(pointvarbinssc)
        del pointvarbinssc


    for uniquekey in testbin_tickers:
        mini_collectiontest(uniquekey)
        import gradeparsecombinessc
