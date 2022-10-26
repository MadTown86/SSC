"""
This starts the grade cycle
"""
import fetchlogssc
import gradecollectionssc
import gradeparsecombinessc


class GradeStartSSC:
    grade_cancel = False
    grade_runitem = ""
    grade_header = "GRADE TICKERS - "

    @staticmethod
    def pull_gradeheader():
        return GradeStartSSC.grade_header

    @staticmethod
    def set_gradeheader(arg_head):
        GradeStartSSC.grade_header = str(arg_head)

    @staticmethod
    def set_runitem(arg):
        GradeStartSSC.grade_runitem = arg

    @staticmethod
    def get_runitem():
        return GradeStartSSC.grade_runitem

    @staticmethod
    def cancel_grade():
        print("Cancel_Grade")
        GradeStartSSC.grade_cancel = True
        print(GradeStartSSC.grade_cancel)

    @staticmethod
    def reset_grade():
        GradeStartSSC.grade_cancel = False

    def gradestartssc(self):
        FS_SSC = fetchlogssc.FetchLogSSC()
        local_logforticker = FS_SSC.ssc_logfetch()
        screened_list = set()
        for item in local_logforticker:
            ticker, tag, instid, uniqueid = item.split("__")
            if uniqueid not in screened_list:
                screened_list.add(f"{ticker}__{uniqueid}")
        for item in screened_list:
            if not GradeStartSSC.grade_cancel:
                ticker, uniqueid = item.split("__")
                GradeStartSSC.set_runitem(ticker)
                PCOMBO = gradeparsecombinessc.GradeParseCombineSSC()
                parsecomb_passin = PCOMBO.gradeparsecombinessc(
                    ticker=ticker, logfileidssc=uniqueid
                )
                GCOL_SSC = gradecollectionssc.GradeCollectionSSC(
                    ticker=ticker,
                    uniqueidssc=uniqueid,
                    parsecombossc=parsecomb_passin,
                )
                GCOL_SSC.gradecollectionssc()
                FS_SSC.ssc_logcompletewrite(ticker, uniqueid)


if __name__ == "__main__":
    GSS = GradeStartSSC()
    GSS.gradestartssc()
