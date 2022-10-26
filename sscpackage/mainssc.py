"""
Rev. 1.1-a.1
Main control program - SSC
"""
import fetchlogssc
import guistarterssc


class ControlBoardSSC:
    """
    This class starts the GUI.
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
