"""
Class combines all parsed data into a dictionary for access by all grading classes.  Instantiated as a
GradeCollectionSSC.attribute
"""

import json

import parsearssc
import parsebalancessc
import parseincomessc
import parseindssc
import parseratiocreatessc
import parsesectorssc
import parsevalssc


class GradeParseCombineSSC:
    inst_count_gpcssc = 0

    @staticmethod
    def return_instcount_gpcssc():
        return GradeParseCombineSSC.inst_count_gpcssc

    def __init__(self):
        GradeParseCombineSSC.inst_count_gpcssc += 1
        self.parsecombo = {}

    def gradeparsecombinessc(self, ticker, logfileidssc):
        try:
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
                        returndictratiossc[key] = [datadictssc[key][x] / datadictssc["Total Revenue"][x] for x in
                                                   list(range(len(datadictssc["Total Revenue"]))) if not
                                                   isinstance(datadictssc[key][x], str)]
                    return returndictratiossc
            except Exception as er:
                print("Exception in GradeParseCombineSSC: function ratiolisterssc")
                print(er)

            incasratiodict = ratiolisterssc(incdat)

            PRC = parseratiocreatessc.ParseRatioCreateSSC()
            finratiodict = PRC.parseratiocreatesssc(incomedictssc=incdat, balancedictssc=baldat)

            self.parsecombo[corekeycombo] = {"AR": ardat, "baldat": baldat, "incdat": incdat,
                                             "Industry": inddat, "Sector": secdat, "valdat": valdat,
                                             "baldatqual": baldatqual, "incdatqual": incdatqual,
                                             "incasratiodict": incasratiodict, "finratiodict": finratiodict}

            return self.parsecombo
        except Exception as er:
            print("Exception in GradeParseCombineSSC: outer scope")
            print(er)
    def parsec_json(self):
        return json.dumps(self.parsecombo, sort_keys=False)


if __name__ == "__main__":
    import dotenv
    import os

    dotenv.load_dotenv(dotenv_path=r'C:\SSC\SimpleStockChecker_REV1\venv\.env')
    ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')
    import json
    import fetchlogssc
    # TODO: Look into .ENV file and replacing hord-coded paths
    tempfilelocation = ROOT_VAR_SSC
    FLOG = fetchlogssc.FetchLogSSC()
    local_fetchlog = FLOG.ssc_logfetch()
    testdict = {}
    cleanlog = set()
    for entry in local_fetchlog[:-1]:
        temp = entry.split("__")
        ticker = temp[0]
        uniqueid = temp[3]
        cleanlog.add(ticker + "__" + uniqueid)
    test_parsedictcont = {}
    for entry in cleanlog:
        entry_tolist = entry.split("__")
        ticker = entry_tolist[0]
        testlogvaridssc = entry_tolist[1]
        GS = GradeParseCombineSSC()
        testdict = GS.gradeparsecombinessc(ticker, testlogvaridssc)
        test_parsedictcont[entry] = testdict
        with open(tempfilelocation + ticker, 'w') as tp:
            json.dump(testdict, tp, indent=5, separators=(", ", ": "), sort_keys=False)



