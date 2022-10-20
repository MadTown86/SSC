import asyncio
from sscpackage.fetchssc import FetchSSC
import dotenv
import os

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')

class FetchStarterSSC:
    """
    This class accepts the tickerlist from user input as an arg, then starts parsing with asyncio and a maximum of 5
    concurrent fetches (max simultaneous RapidAPI will allow for my payment level)

    Control Flow:
    From: guistarterssc
    To: fetchssc
    On Cancel: returns to guistarterssc
    """
    runlist_tickers = []
    fetch_cancel = False
    fetch_header = "FETCH TICKERS: "
    init_once = False

    @staticmethod
    def pull_header():
        return FetchStarterSSC.fetch_header

    @staticmethod
    def update_header(arg_header):
        FetchStarterSSC.fetch_header = str(arg_header)

    @staticmethod
    def update_runlist(onetic: str, *args) -> None:
        del FetchStarterSSC.runlist_tickers
        if onetic:
            FetchStarterSSC.runlist_tickers = onetic
        else:
            FetchStarterSSC.runlist_tickers = [x for x in args]

    @staticmethod
    def pull_runlist():
        return FetchStarterSSC.runlist_tickers

    @staticmethod
    def cancel_fetch():
        print("entered cancel_fetch :: ")
        FetchStarterSSC.fetch_cancel = True
        print(FetchStarterSSC.fetch_cancel)

    @staticmethod
    def reset_fetch():
        FetchStarterSSC.fetch_cancel = False

    def __init__(self, tickerlist: list):
        self.tickerlist = tickerlist
        self.fetch_cancel = False
        self.runninglist = []
        FetchStarterSSC.init_once = True

    async def _fetch_cycle(self, *args, **kwargs):
        tickerlistvar_fetchssc = self.tickerlist[:]
        while tickerlistvar_fetchssc:
            print(tickerlistvar_fetchssc)
            if FetchStarterSSC.fetch_cancel:
                print("Broke Chain - FetchStarter")
                break
            if len(tickerlistvar_fetchssc) >= 5:
                ticker_runlist = []
                if FetchStarterSSC.fetch_cancel:
                    print("Broke Chain - FetchStarter")
                    break
                ticker_runlist.append(tickerlistvar_fetchssc[:5])
                FetchStarterSSC.update_runlist(ticker_runlist)
                await asyncio.gather(
                    FetchSSC().rapid_fetch(tickerlistvar_fetchssc.pop(0)),
                    FetchSSC().rapid_fetch(tickerlistvar_fetchssc.pop(0)),
                    FetchSSC().rapid_fetch(tickerlistvar_fetchssc.pop(0)),
                    FetchSSC().rapid_fetch(tickerlistvar_fetchssc.pop(0)),
                    FetchSSC().rapid_fetch(tickerlistvar_fetchssc.pop(0)),
                )
            else:
                if FetchStarterSSC.fetch_cancel:
                    print("Broke Chain - FetchStarter")
                    break
                ticker_runlist = tickerlistvar_fetchssc[0]
                FetchStarterSSC.update_runlist(onetic=ticker_runlist)
                await asyncio.gather(FetchSSC().rapid_fetch(tickerlistvar_fetchssc.pop(0)))
            await asyncio.sleep(1)


if __name__ == "__main__":
    test_pathfile = ROOT_VAR_SSC + "storageticker_sixlist.txt"
    with open(test_pathfile, 'r') as tpf:
        FS = FetchStarterSSC(tpf.read().split(", "))
        asyncio.run(FS._fetch_cycle())
