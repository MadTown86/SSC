import fetchlogssc
import fetchshelfssc_mod
import fetchssc
import parsearssc
import parsebalancessc_sub
import parseincomessc_sub
import parseindssc_sub
import parsesectorssc_sub
import parsessc
import parsevalssc_sub


class ParseStartSub(parsessc.ParseStart):
    def __init__(self):
        super().__init__()

    def ssc_parselogstart(self, ticker_fail):
        """
        1. opens log file with stored list of current keys
        2. for loop through list to access fetchstore shelve and pull data
        3. Filter data into respective instance variables for parsing.
        """

        ticker_faillist = fetchssc.FetchSSC.pull_tickerfail()

        FS_SSC = fetchshelfssc_mod.FetchShelfSSC()
        shelvecopy_fromapi = FS_SSC.fetchdbpull()
        del FS_SSC

        FLOG = fetchlogssc.FetchLogSSC()
        local_logcopy = FLOG.ssc_logfetch()
        del FLOG

        PI_SSC = parseincomessc_sub.ParseIncomeSSC_Sub()
        PB_SSC = parsebalancessc_sub.ParseBalance_Sub()
        PVAL_SSC = parsevalssc_sub.ParseValSSC_Sub()
        PAR_SSC = parsearssc.ParseAr()
        PSEC_SSC = parsesectorssc_sub.ParseSec_Sub()
        PIND_SSC = parseindssc_sub.ParseIndustry_Sub()

        tag_container = {}
        tag_container["url_income"] = "inctag"
        tag_container["url_balance"] = "baltag"
        tag_container["url_val"] = "valtag"
        tag_container["url_ar"] = "artag"
        tag_container["url_sectordata"] = "sectag"

        def indsec(tag):
            PSEC_SSC.parsesector(tag, shelvecopy_fromapi[tag]),
            PIND_SSC.parseindustry(tag, shelvecopy_fromapi[tag])

        dict_tagswitchboard = {
            "inctag": lambda logentrylamb: PI_SSC.parseincome(
                logentrylamb, shelvecopy_fromapi[logentrylamb]
            ),
            "baltag": lambda logentrylamb: PB_SSC.parsebalance(
                logentrylamb, shelvecopy_fromapi[logentrylamb]
            ),
            "valtag": lambda logentrylamb: PVAL_SSC.parseval(
                logentrylamb, shelvecopy_fromapi[logentrylamb]
            ),
            "artag": lambda logentrylamb: PAR_SSC.parsear(
                logentrylamb, shelvecopy_fromapi[logentrylamb]
            ),
            "sectag": lambda logentrylamb: indsec(logentrylamb),
        }
        print(f"TICKER FAIL LIST: {ticker_fail}")

        for logentry in local_logcopy:
            if len(logentry.split("__")) == 4:
                ticker, tag, selfid, uniqueid = logentry.split("__")
                print(f"PARSESTART: {ticker}")
                if logentry not in ticker_fail:
                    ParseStartSub.set_parserun(logentry.split('__')[0])
                    if ParseStartSub.parse_cancel:
                        break
                    else:
                        (dict_tagswitchboard[tag_container[tag]](logentry))
                else:
                    continue

        del PI_SSC
        del PB_SSC
        del PSEC_SSC
        del PAR_SSC
        del PVAL_SSC
        del PIND_SSC