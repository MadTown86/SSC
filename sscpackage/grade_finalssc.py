import gradesheetprintssc


class GradeFinalSSC(gradesheetprintssc.GradeSheetPrintSSC):
    def __init__(self):
        super().__init__()
        self.final_grade_ssc = ""
        self.totalpoints = 0
        self.awardedpoints = 0

    def grade_final_ssc(self, pointbin):
        totalpoints = 0
        awardedpoints = 0
        for currentpoints, basepoints in pointbin:
            totalpoints += basepoints
            awardedpoints += currentpoints

        ratiores = awardedpoints / totalpoints

        self.totalpoints = totalpoints
        self.awardedpoints = awardedpoints

        if ratiores >= 0.94:
            self.final_grade_ssc = "A"
        elif ratiores >= 0.90:
            self.final_grade_ssc = "AB"
        elif ratiores >= 0.84:
            self.final_grade_ssc = "B"
        elif ratiores >= 0.80:
            self.final_grade_ssc = "BC"
        elif ratiores >= 0.74:
            self.final_grade_ssc = "C"
        elif ratiores >= 0.70:
            self.final_grade_ssc = "CD"
        elif ratiores >= 0.64:
            self.final_grade_ssc = "D"
        else:
            self.final_grade_ssc = "F"


if __name__ == "__main__":
    GF = GradeFinalSSC()
    GF.grade_final_ssc([(0, 2), (2, 2), (2, 2)])
    print(GF.final_grade_ssc)
