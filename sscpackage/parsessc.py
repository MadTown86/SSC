import fetchshelfssc_mod
import fetchlogssc
import parseincomessc
import parsebalancessc
import parsearssc
import parsesectorssc
import parseindssc
import parsevalssc


class ParseStart:

    def ssc_parselogstart(self):
        """
        1. opens log file with stored list of current keys
        2. for loop through list to access fetchstore shelve and pull data
        3. Filter data into respective instance variables for parsing.
        """

        FS_SSC = fetchshelfssc_mod.FetchShelfSSC()
        shelvecopy_fromapi = FS_SSC.fetchdbpull()
        del FS_SSC

        FLOG = fetchlogssc.FetchLogSSC()
        local_logcopy = FLOG.ssc_logfetch()
        del FLOG

        PI_SSC = parseincomessc.ParseIncome()
        PB_SSC = parsebalancessc.ParseBalance()
        PVAL_SSC = parsevalssc.ParseVal()
        PAR_SSC = parsearssc.ParseAr()
        PSEC_SSC = parsesectorssc.ParseSector()
        PIND_SSC = parseindssc.ParseIndustry()

        inctag = "url_income"
        baltag = "url_balance"
        valtag = "url_val"
        artag = "url_ar"
        sectag = "url_sector"
        tag_container = [inctag, baltag, valtag, artag, sectag]

        def indsec(tag):
            PSEC_SSC.parsesector(tag, shelvecopy_fromapi[tag]),
            PIND_SSC.parseindustry(tag, shelvecopy_fromapi[tag])

        dict_tagswitchboard = {inctag: lambda logentrylamb:
        PI_SSC.parseincome(logentrylamb, shelvecopy_fromapi[logentrylamb]),

                               baltag: lambda logentrylamb:
                               PB_SSC.parsebalance(logentrylamb, shelvecopy_fromapi[logentrylamb]),

                               valtag: lambda logentrylamb:
                               PVAL_SSC.parseval(logentrylamb, shelvecopy_fromapi[logentrylamb]),

                               artag: lambda logentrylamb:
                               PAR_SSC.parsear(logentrylamb, shelvecopy_fromapi[logentrylamb]),

                               sectag: lambda logentrylamb: indsec(logentrylamb)
                               }

        for logentry in local_logcopy:
            for tag in tag_container:
                if tag in logentry:
                    (dict_tagswitchboard[tag])(logentry)
                    break
                else:
                    continue

        del PI_SSC
        del PB_SSC
        del PSEC_SSC
        del PAR_SSC
        del PVAL_SSC
        del PIND_SSC
