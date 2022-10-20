import gradeparsecombinessc
import parsearssc
import parsebalancessc_sub
import parseindssc_sub
import parseincomessc_sub
import parseratiocreatessc
import parsevalssc_sub
import parsesectorssc_sub


class GradeParseCombineSSCSub(gradeparsecombinessc.GradeParseCombineSSC):
    def __init__(self):
        super().__init__()

    def gradeparsecombinessc(self, ticker, logfileidssc):
        try:
            PAR = parsearssc.ParseAr()
            PBAL = parsebalancessc_sub.ParseBalance_Sub()
            PINC = parseincomessc_sub.ParseIncomeSSC_Sub()
            PIND = parseindssc_sub.ParseIndustry_Sub()
            PSEC = parsesectorssc_sub.ParseSec_Sub()
            PVAL = parsevalssc_sub.ParseValSSC_Sub()

            ardat = PAR.fetch_parsear(logfileidssc)
            baldat = PBAL.fetch_parsebalance(logfileidssc)
            incdat = PINC.fetch_parseincome(logfileidssc)
            inddat = PIND.fetch_parseindustry(logfileidssc)
            secdat = PSEC.fetch_parsesector(logfileidssc)
            valdat = PVAL.fetchparseval(logfileidssc)

            del PAR, PBAL, PINC, PIND, PSEC, PVAL

            corekeycombo = ticker + "__" + logfileidssc

            try:

                def incbalqualssc(datadictssc):
                    returndictqualssc = {}
                    for key in datadictssc.keys():
                        templist = []
                        for val in range(len(datadictssc[key])):
                            if datadictssc[key][val] != 0:
                                continue
                            else:
                                templist.append(val)
                                continue
                        if templist:
                            returndictqualssc[key] = templist
                        else:
                            continue

                    return returndictqualssc

            except Exception as er:
                print("Exception in ParseCombineSSC: incbalqualssc")
                print(er)

            baldatqual = incbalqualssc(baldat)
            incdatqual = incbalqualssc(incdat)

            try:

                def ratiolisterssc(datadictssc):
                    returndictratiossc = {}
                    for key in datadictssc.keys():
                        returndictratiossc[key] = [
                            datadictssc[key][x] / datadictssc["Total Revenue"][x]
                            for x in list(range(len(datadictssc["Total Revenue"])))
                            if not isinstance(datadictssc[key][x], str)
                        ]
                    return returndictratiossc

            except Exception as er:
                print("Exception in GradeParseCombineSSC: function ratiolisterssc")
                print(er)

            incasratiodict = ratiolisterssc(incdat)

            PRC = parseratiocreatessc.ParseRatioCreateSSC()
            finratiodict = PRC.parseratiocreatesssc(
                incomedictssc=incdat, balancedictssc=baldat
            )

            self.parsecombo[corekeycombo] = {
                "AR": ardat,
                "baldat": baldat,
                "incdat": incdat,
                "Industry": inddat,
                "Sector": secdat,
                "valdat": valdat,
                "baldatqual": baldatqual,
                "incdatqual": incdatqual,
                "incasratiodict": incasratiodict,
                "finratiodict": finratiodict,
            }

            return self.parsecombo
        except Exception as er:
            print("Exception in GradeParseCombineSSC: outer scope")
            print(er)

if __name__ == "__main__":