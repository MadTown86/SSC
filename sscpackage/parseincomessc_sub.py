"""
Sub Class of 'parseincomessc' - To parse YH Finance JSON format instead of Stock Market Data by lattice
"""
import fetchshelfssc_mod
import parseincomessc
import json
import dictpullssc
import parsebalancessc_sub


class ParseIncomeSSC_Sub(parseincomessc.ParseIncome):
    def __init__(self):
        super().__init__()

    def parseincome(self, uniquename: "str", pi_rawdata: json) -> None:
        """
        Converts raw json string to usable format for grading purposes

        :param uniquename: String from fetchlog, acts as key for fetchshelf
        :param pi_rawdata: url_income fetch data from shelve
        :return: None
        """
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidpi = (
                uniquesplitlist[0],
                uniquesplitlist[1],
                uniquesplitlist[2],
                uniquesplitlist[3],
            )

            DS = dictpullssc.DictPullSSC()
            inc_key = "incomeStatementHistory"

            parseinc_wdict = DS.dictpullssc(pi_rawdata, inc_key)
            inner_wdict = parseinc_wdict["incomeStatementHistory"]

            # List for transfering string format to pre-existing format
            keywordtransferbin = {
                "researchDevelopment": "Research & Development",
                "effectOfAccountingCharges": "Effect of Accounting Charges",
                "incomeBeforeTax": "Income Before Tax",
                "minorityInterest": "Minority Interest",
                "netIncome": "Net Interest",
                "sellingGeneralAdministrative": "Selling, General & Administrative",
                "grossProfit": "Gross Profit",
                "ebit": "EBIT",
                "operatingIncome": "Operating Income",
                "otherOperatingExpenses": "Other Operating Expenses",
                "interestExpense": "Interest Expense",
                "extraordinaryItems": "Extraordinary Items",
                "nonRecurring": "Non Recurring",
                "otherItems": "Other Items",
                "incomeTaxExpense": "Income Tax Expense",
                "totalRevenue": "Total Revenue",
                "totalOperatingExpenses": "Total Operating Expenses",
                "costOfRevenue": "Cost Of Revenue",
                "totalOtherIncomeExpenseNet": "Total Other Income Expense Net",
                "discontinuedOperations": "Discontinued Operations",
                "netIncomeFromContinuingOps": "Net Income From Continuing Ops",
                "netIncomeApplicableToCommonShares": "Net Income Applicable To Common Shares",
            }

            output_dict_inc = parsebalancessc_sub.incbal_reformat(
                uniquename, inner_wdict, keywordtransferbin
            )

            fetchstorename = uniquename
            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(
                fetchstoreshelf=self.setpathssc_parsessc
            )
            FST_SSC.fetchstore(
                ticker=ticker, fetch_data=output_dict_inc, fetchstorename=fetchstorename
            )
            del FST_SSC

        except Exception as Er:
            print("Exception in 'ParseIncome.parseincome'  ::  ")
            print(str(Er))
