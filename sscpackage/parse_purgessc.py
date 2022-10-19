import parsevalssc
import parsebalancessc
import parseincomessc
import parseindssc
import parsearssc
import parsesectorssc


class ParsePurgeSSC:
    @staticmethod
    def purgeall():
        PSVAL = parsevalssc.ParseVal()
        PBAL = parsebalancessc.ParseBalance()
        PINC = parseincomessc.ParseIncome()
        PIND = parseindssc.ParseIndustry()
        PAR = parsearssc.ParseAr()
        PARSEC = parsesectorssc.ParseSector()

        PSVAL.parse_valpurge()
        PBAL.parse_balancepurge()
        PINC.parse_incomepurge()
        PIND.parse_indpurge()
        PAR.purge_parsear()
        PARSEC.parse_sectpurge()
