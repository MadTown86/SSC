"""
Class combines all parsed data into a dictionary for access by all grading classes.  Instatiated as a
GradeCollection.attribute
"""
import parsearssc
import parsebalancessc
import parseincomessc
import parseindssc
import parsesectorssc
import parsevalssc

class GradeParseCombineSSC():
    def gradeparsecombinessc(self, ticker, logfileidssc):
        PAR = parsearssc.ParseAr()
        PBAL = parsebalancessc.ParseBalance()
        PINC = parseincomessc.ParseIncome()
        PIND = parseindssc.ParseIndustry()
        PSEC = parsesectorssc.ParseSector()
        PVAL = parsevalssc.ParseVal()

        ardat = PAR.fetch_parsear(logfileidssc)
        baldat = PBAL.fetch_parsebalance(logfileidssc)
        incdat = PINC.fetch_parseincome(logfileidssc)
        inddat = PIND.fetch_parseindustry(logfileidssc)
        secdat = PSEC.fetch_parsesector(logfileidssc)
        valdat = PVAL.fetchparseval(logfileidssc)

        del PAR, PBAL, PINC, PIND, PSEC, PVAL

        corekeycombo = ticker + "__" + logfileidssc
        parsecombo = {}

        parsecombo[corekeycombo] = {"AR": ardat, "baldat": baldat, "incdat": incdat,
                                    "Industry": inddat, "Sector": secdat, "valdat": valdat}

        return parsecombo





