import asyncio
from sscpackage.fetchssc import FetchSSC


class FetchStarterSSC:
    """
    This class accepts the tickerlist from user input as an arg, then starts parsing with asyncio and a maximum of 5
    concurrent fetches (max simultaneous RapidAPI will allow for my payment level)
    """

    def __init__(self, tickerlist="MSFT, AMD, TTD, MU, NVDA"):
        self.tickerlist = tickerlist.split(", ")

    async def fetch_cycle(self, *args, **kwargs):
        tickerlistvar_fetchssc = self.tickerlist
        while tickerlistvar_fetchssc:
            if len(tickerlistvar_fetchssc) >= 5:
                await asyncio.gather(
                    FetchSSC(tickerlistvar_fetchssc.pop(0)).rapid_fetch(),
                    FetchSSC(tickerlistvar_fetchssc.pop(0)).rapid_fetch(),
                    FetchSSC(tickerlistvar_fetchssc.pop(0)).rapid_fetch(),
                    FetchSSC(tickerlistvar_fetchssc.pop(0)).rapid_fetch(),
                    FetchSSC(tickerlistvar_fetchssc.pop(0)).rapid_fetch(),
                )
            else:
                for indexno in range(len(tickerlistvar_fetchssc)):
                    await asyncio.gather(FetchSSC(tickerlistvar_fetchssc.pop(0)).rapid_fetch())
            await asyncio.sleep(1)
