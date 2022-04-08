import tkinter as tk
from tkinter import *
from tkinter import ttk
import tcl
from tkinter import filedialog as fd
#import simplestockchecker_storetool as SST
import tkinter.font as tkFont
"""
widgets: 
tk.Label
tk.Button
tk.Entry
tk.Text
tk.Frame

#1/2/2022

FRAME WIDGET - ATTRIBUTES

def __init__(self,
             master: Misc | None = ...,
             cnf: Dict[str, Any] | None = ...,
             *,
             background: str = ...,
             bd: str | float = ...,
             bg: str = ...,
             border: str | float = ...,
             borderwidth: str | float = ...,
             class_: str = ...,
             colormap: Literal["new", ""] | Misc = ...,
             container: bool = ...,
             cursor: str | Tuple[str] | Tuple[str, str] | Tuple[str, str, str] | Tuple[str, str, str, str] = ...,
             height: str | float = ...,
             highlightbackground: str = ...,
             highlightcolor: str = ...,
             highlightthickness: str | float = ...,
             name: str = ...,
             padx: str | float = ...,
             pady: str | float = ...,
             relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             takefocus: int | Literal[""] | (str) -> bool | None = ...,
             visual: str | Tuple[str, int] = ...,
             width: str | float = ...) -> None
             
# LABEL WIDGET ATTRIBUTES

def __init__(self,
             master: Misc | None = ...,
             cnf: Dict[str, Any] | None = ...,
             *,
             activebackground: str = ...,
             activeforeground: str = ...,
             anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = ...,
             background: str = ...,
             bd: str | float = ...,
             bg: str = ...,
             bitmap: str = ...,
             border: str | float = ...,
             borderwidth: str | float = ...,
             compound: Literal["top", "left", "center", "right", "bottom", "none"] = ...,
             cursor: str | Tuple[str] | Tuple[str, str] | Tuple[str, str, str] | Tuple[str, str, str, str] = ...,
             disabledforeground: str = ...,
             fg: str = ...,
             font: Any = ...,
             foreground: str = ...,
             height: str | float = ...,
             highlightbackground: str = ...,
             highlightcolor: str = ...,
             highlightthickness: str | float = ...,
             image: _Image | str = ...,
             justify: Literal["left", "center", "right"] = ...,
             name: str = ...,
             padx: str | float = ...,
             pady: str | float = ...,
             relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             state: Literal["normal", "active", "disabled"] = ...,
             takefocus: int | Literal[""] | (str) -> bool | None = ...,
             text: float | str = ...,
             textvariable: Variable = ...,
             underline: int = ...,
             width: str | float = ...,
             wraplength: str | float = ...) -> None
             
# tk.TEXT Attributes

tkinter.Text def __init__(self,
             master: Misc | None = ...,
             cnf: Dict[str, Any] | None = ...,
             *,
             autoseparators: bool = ...,
             background: str = ...,
             bd: str | float = ...,
             bg: str = ...,
             blockcursor: bool = ...,
             border: str | float = ...,
             borderwidth: str | float = ...,
             cursor: str | Tuple[str] | Tuple[str, str] | Tuple[str, str, str] | Tuple[str, str, str, str] = ...,
             endline: int | Literal[""] = ...,
             exportselection: bool = ...,
             fg: str = ...,
             font: Any = ...,
             foreground: str = ...,
             height: str | float = ...,
             highlightbackground: str = ...,
             highlightcolor: str = ...,
             highlightthickness: str | float = ...,
             inactiveselectbackground: str = ...,
             insertbackground: str = ...,
             insertborderwidth: str | float = ...,
             insertofftime: int = ...,
             insertontime: int = ...,
             insertunfocussed: Literal["none", "hollow", "solid"] = ...,
             insertwidth: str | float = ...,
             maxundo: int = ...,
             name: str = ...,
             padx: str | float = ...,
             pady: str | float = ...,
             relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             selectbackground: str = ...,
             selectborderwidth: str | float = ...,
             selectforeground: str = ...,
             setgrid: bool = ...,
             spacing1: str | float = ...,
             spacing2: str | float = ...,
             spacing3: str | float = ...,
             startline: int | Literal[""] = ...,
             state: Literal["normal", "disabled"] = ...,
             tabs: str | float | Tuple[str | float, ...] = ...,
             tabstyle: Literal["tabular", "wordprocessor"] = ...,
             takefocus: int | Literal[""] | (str) -> bool | None = ...,
             undo: bool = ...,
             width: int = ...,
             wrap: Literal["none", "char", "word"] = ...,
             xscrollcommand: str | (float, float) -> Any = ...,
             yscrollcommand: str | (float, float) -> Any = ...)
             
#TK Button ATtributes

tkinter.Button def __init__(self,
             master: Misc | None = ...,
             cnf: Dict[str, Any] | None = ...,
             *,
             activebackground: str = ...,
             activeforeground: str = ...,
             anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = ...,
             background: str = ...,
             bd: str | float = ...,
             bg: str = ...,
             bitmap: str = ...,
             border: str | float = ...,
             borderwidth: str | float = ...,
             command: str | () -> Any = ...,
             compound: Literal["top", "left", "center", "right", "bottom", "none"] = ...,
             cursor: str | Tuple[str] | Tuple[str, str] | Tuple[str, str, str] | Tuple[str, str, str, str] = ...,
             default: Literal["normal", "active", "disabled"] = ...,
             disabledforeground: str = ...,
             fg: str = ...,
             font: Any = ...,
             foreground: str = ...,
             height: str | float = ...,
             highlightbackground: str = ...,
             highlightcolor: str = ...,
             highlightthickness: str | float = ...,
             image: _Image | str = ...,
             justify: Literal["left", "center", "right"] = ...,
             name: str = ...,
             overrelief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             padx: str | float = ...,
             pady: str | float = ...,
             relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             repeatdelay: int = ...,
             repeatinterval: int = ...,
             state: Literal["normal", "active", "disabled"] = ...,
             takefocus: int | Literal[""] | (str) -> bool | None = ...,
             text: float | str = ...,
             textvariable: Variable = ...,
             underline: int = ...,
             width: str | float = ...,
             wraplength: str | float = ...) -> None
             
#Tk.Check Button Attributes
tkinter.Checkbutton def __init__(self,
             master: Misc | None = ...,
             cnf: Dict[str, Any] | None = ...,
             *,
             activebackground: str = ...,
             activeforeground: str = ...,
             anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = ...,
             background: str = ...,
             bd: str | float = ...,
             bg: str = ...,
             bitmap: str = ...,
             border: str | float = ...,
             borderwidth: str | float = ...,
             command: str | () -> Any = ...,
             compound: Literal["top", "left", "center", "right", "bottom", "none"] = ...,
             cursor: str | Tuple[str] | Tuple[str, str] | Tuple[str, str, str] | Tuple[str, str, str, str] = ...,
             disabledforeground: str = ...,
             fg: str = ...,
             font: Any = ...,
             foreground: str = ...,
             height: str | float = ...,
             highlightbackground: str = ...,
             highlightcolor: str = ...,
             highlightthickness: str | float = ...,
             image: _Image | str = ...,
             indicatoron: bool = ...,
             justify: Literal["left", "center", "right"] = ...,
             name: str = ...,
             offrelief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             offvalue: Any = ...,
             onvalue: Any = ...,
             overrelief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             padx: str | float = ...,
             pady: str | float = ...,
             relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             selectcolor: str = ...,
             selectimage: _Image | str = ...,
             state: Literal["normal", "active", "disabled"] = ...,
             takefocus: int | Literal[""] | (str) -> bool | None = ...,
             text: float | str = ...,
             textvariable: Variable = ...,
             tristateimage: _Image | str = ...,
             tristatevalue: Any = ...,
             underline: int = ...,
             variable: Variable | Literal[""] = ...,
             width: str | float = ...,
             wraplength: str | float = ...) -> None
             
#tk.RadioButton Attributes

tkinter.Radiobutton def __init__(self,
             master: Misc | None = ...,
             cnf: Dict[str, Any] | None = ...,
             *,
             activebackground: str = ...,
             activeforeground: str = ...,
             anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = ...,
             background: str = ...,
             bd: str | float = ...,
             bg: str = ...,
             bitmap: str = ...,
             border: str | float = ...,
             borderwidth: str | float = ...,
             command: str | () -> Any = ...,
             compound: Literal["top", "left", "center", "right", "bottom", "none"] = ...,
             cursor: str | Tuple[str] | Tuple[str, str] | Tuple[str, str, str] | Tuple[str, str, str, str] = ...,
             disabledforeground: str = ...,
             fg: str = ...,
             font: Any = ...,
             foreground: str = ...,
             height: str | float = ...,
             highlightbackground: str = ...,
             highlightcolor: str = ...,
             highlightthickness: str | float = ...,
             image: _Image | str = ...,
             indicatoron: bool = ...,
             justify: Literal["left", "center", "right"] = ...,
             name: str = ...,
             offrelief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             overrelief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             padx: str | float = ...,
             pady: str | float = ...,
             relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             selectcolor: str = ...,
             selectimage: _Image | str = ...,
             state: Literal["normal", "active", "disabled"] = ...,
             takefocus: int | Literal[""] | (str) -> bool | None = ...,
             text: float | str = ...,
             textvariable: Variable = ...,
             tristateimage: _Image | str = ...,
             tristatevalue: Any = ...,
             underline: int = ...,
             value: Any = ...,
             variable: Variable | Literal[""] = ...,
             width: str | float = ...,
             wraplength: str | float = ...) -> None
             
#tk.Canvas Attributes

tkinter.Canvas def __init__(self,
             master: Misc | None = ...,
             cnf: Dict[str, Any] | None = ...,
             *,
             background: str = ...,
             bd: str | float = ...,
             bg: str = ...,
             border: str | float = ...,
             borderwidth: str | float = ...,
             closeenough: float = ...,
             confine: bool = ...,
             cursor: str | Tuple[str] | Tuple[str, str] | Tuple[str, str, str] | Tuple[str, str, str, str] = ...,
             height: str | float = ...,
             highlightbackground: str = ...,
             highlightcolor: str = ...,
             highlightthickness: str | float = ...,
             insertbackground: str = ...,
             insertborderwidth: str | float = ...,
             insertofftime: int = ...,
             insertontime: int = ...,
             insertwidth: str | float = ...,
             name: str = ...,
             offset: Any = ...,
             relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             scrollregion: Tuple[str | float, str | float, str | float, str | float] | Tuple = ...,
             selectbackground: str = ...,
             selectborderwidth: str | float = ...,
             selectforeground: str = ...,
             state: Literal["normal", "disabled"] = ...,
             takefocus: int | Literal[""] | (str) -> bool | None = ...,
             width: str | float = ...,
             xscrollcommand: str | (float, float) -> Any = ...,
             xscrollincrement: str | float = ...,
             yscrollcommand: str | (float, float) -> Any = ...,
             yscrollincrement: str | float = ...) -> None
             
#tk.Entry Attributes

tkinter.Entry def __init__(self,
             master: Misc | None = ...,
             cnf: Dict[str, Any] | None = ...,
             *,
             background: str = ...,
             bd: str | float = ...,
             bg: str = ...,
             border: str | float = ...,
             borderwidth: str | float = ...,
             cursor: str | Tuple[str] | Tuple[str, str] | Tuple[str, str, str] | Tuple[str, str, str, str] = ...,
             disabledbackground: str = ...,
             disabledforeground: str = ...,
             exportselection: bool = ...,
             fg: str = ...,
             font: Any = ...,
             foreground: str = ...,
             highlightbackground: str = ...,
             highlightcolor: str = ...,
             highlightthickness: str | float = ...,
             insertbackground: str = ...,
             insertborderwidth: str | float = ...,
             insertofftime: int = ...,
             insertontime: int = ...,
             insertwidth: str | float = ...,
             invalidcommand: () -> bool | str | List[str] | Tuple[str, ...] = ...,
             invcmd: () -> bool | str | List[str] | Tuple[str, ...] = ...,
             justify: Literal["left", "center", "right"] = ...,
             name: str = ...,
             readonlybackground: str = ...,
             relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"] = ...,
             selectbackground: str = ...,
             selectborderwidth: str | float = ...,
             selectforeground: str = ...,
             show: str = ...,
             state: Literal["normal", "disabled", "readonly"] = ...,
             takefocus: int | Literal[""] | (str) -> bool | None = ...,
             textvariable: Variable = ...,
             validate: Literal["none", "focus", "focusin", "focusout", "key", "all"] = ...,
             validatecommand: () -> bool | str | List[str] | Tuple[str, ...] = ...,
             vcmd: () -> bool | str | List[str] | Tuple[str, ...] = ...,
             width: int = ...,
             xscrollcommand: str | (float, float) -> Any = ...)
             
#tk.Grid.grid() Attributes

def grid_configure(self,
                   cnf: Mapping[str, Any] | None = ...,
                   *,
                   column: int = ...,
                   columnspan: int = ...,
                   row: int = ...,
                   rowspan: int = ...,
                   ipadx: str | float = ...,
                   ipady: str | float = ...,
                   padx: str | float | Tuple[str | float, str | float] = ...,
                   pady: str | float | Tuple[str | float, str | float] = ...,
                   sticky: str = ...,
                   in_: Misc = ...,
                   **kw: Any) -> None

"""


def guiBuilder():
    root = tk.Tk() # Creating Root Instance - Main Window
    root.title("Simple Stock Checker") # Naming main window
    root.config(height="600", width="1200", background="LINEN", padx="10", pady="10") #Set root height/width bg color
    root.columnconfigure(0, weight=1) #I believe setting the root to only have one column
    root.rowconfigure(0, weight=1) #I believe setting root to only have one row
    root.resizable(False, False) # Setting height/width to not resizable

    mainframe = tk.Frame(root, padx="10", pady="10", bd="5", background="LINEN"
                         ).grid(column=0, row=0, sticky=(N, W, E, S)) #Create a frame widget to span entire root window

    """
    Building mainframe to contain 3 columns and 3 rows similar to matrix
    Row and Col start at 0
    Filling information for entire row first, then moving to next row
    """

    label_1 = tk.Label(master=mainframe, text="Please Select A Text File\n", bg="LINEN").grid(column=0, row=0, columnspan=2)
    browse_btn = tk.Button(master=mainframe, text="Browse", padx="5", pady="5")
    browse_btn.grid(column=0, row=1, columnspan=2, padx="5", pady="5")
    text_1 = tk.Text(master=mainframe, width="50", height="10")
    text_1.grid(column=0, row=2, columnspan=2)

    def fileopn(event):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        fd_003 = fd.askopenfile(title="Browse", filetypes=filetypes, initialdir="/")
        print(type(fd_003))
        return fd_003

    browse_btn.bind("<Button-1>", fileopn)

    root.mainloop()


guiBuilder()