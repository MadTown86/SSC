"""
This starts the grade cycle
"""
import fetchlogssc
import gradecollectionssc
import gradeparsecombinessc


class GradeStartSSC():
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
        try:
            print("1")
            FS_SSC = fetchlogssc.FetchLogSSC()
            print("2")
            local_logforticker = FS_SSC.ssc_logfetch()
            print("3")
            print(local_logforticker)
            clean_copyssc = set()
            for val in local_logforticker:
                splitcopy = val.split("__")
                clean_copyssc.add(splitcopy[0] + "__" + splitcopy[3])
            print("4")
            for val in clean_copyssc:
                print(val)
            for item in clean_copyssc:
                    if not GradeStartSSC.grade_cancel:
                        ticker, entrysscgs = item.split("__")
                        print(ticker)
                        print(entrysscgs)
                        GradeStartSSC.set_runitem(ticker)
                        print("After GradeStartSSC runitem set")
                        PCOMBO = gradeparsecombinessc.GradeParseCombineSSC()
                        print("After gradeparsecombinessc")
                        parsecomb_passin = PCOMBO.gradeparsecombinessc(ticker=ticker, logfileidssc=entrysscgs)
                        GCOL_SSC = gradecollectionssc.GradeCollectionSSC(ticker=ticker,
                                                                         uniqueidssc=entrysscgs,
                                                                         parsecombossc=parsecomb_passin)
                        print("After creation of grade collection object")
                        print(gradecollectionssc.GradeCollectionSSC.return_inst_count())
                        GCOL_SSC.gradecollectionssc()
                        print("After GCOL_SSC.gradecollectionssc()")
                        FS_SSC.ssc_logcompletewrite(ticker, entrysscgs)
        except Exception as er:
            print("Exception in GradeStarterSSC: function 'gradestartssc' ")
            print(er)


if __name__ == "__main__":
    GSS = GradeStartSSC()
    GSS.gradestartssc()
