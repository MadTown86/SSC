"""
Rev. 1.1-a.1
Main control program - SSC
"""
import fetchlogssc
import guistarterssc


def gui_ssc_instantiate():
    print(guistarterssc.GuiStarterSSC.fetch_instcount())
    if guistarterssc.GuiStarterSSC.fetch_instcount() > 0:
        pass
    else:
        fetchlogssc.FetchLogSSC.ssc_fetchlogclear()
        guistarterssc.GuiStarterSSC().start_gui_ssc()


gui_ssc_instantiate()


def cancel_schedule():
    if guistarterssc.GuiStarterSSC.cancel_start:
        pass


class ControlBoardSSC():
    """
    Main Control Flow:
    1. guistarter
    FROM GUI - INPUT CHOSEN
    2.
    """
    main_cancelf = False

    @staticmethod
    def clearlog():
        fetchlogssc.FetchLogSSC.ssc_fetchlogclear()

    def __init__(self):
        self.gui = guistarterssc.GuiStarterSSC()


if __name__ == "__main__":
    CS = ControlBoardSSC()
    CS.gui.start_gui_ssc()
