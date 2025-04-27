# file:     dataSourceLabel.py - "showing ** vehicles from [vehicles.sqlite]"-label ui component
# author:   Ben Mullan (2025)

import tkinter; from tkinter import ttk, messagebox;
from . import (ui_c_floatingToolTip, db_dbFileManager);


class DataSourceLabel (ttk.Frame):
    """ui-component: data-source text + link label"""


    __UNINITIALISED_TEXTBIT_ :str = "no database-file loaded";
    """[static] shown before a *.sqlite file is loaded from disk"""

    __UNINITIALISED_LINKBIT_ :str = "yet...";
    """[static] shown before a *.sqlite file is loaded from disk"""

    __textBit :ttk.Label;
    """the label showing the [showing * vahicles]-bit"""

    __linkBit :ttk.Label;
    """the label showing the [{sqlite-file-name}]-bit"""


    def __init__(self, _parentComponent :tkinter.Widget, **kwargs) -> None:
        """instanciates the ui-component"""
        super().__init__(master=_parentComponent, **kwargs);
        self.__configureSelf();


    def __configureSelf(self) -> None:
        """initialises the ui-component's properties and children"""

        self.__configureGrid();
        self.configure(style="vdb.normal.TFrame");

        # ╔══════════════════════╦═══════════╗
        # ║ longer text-bit here ║ link here ║
        # ╚══════════════════════╩═══════════╝

        self.__textBit = ttk.Label(
            master=self, #knowthyself
            style="vdb.subtle.TLabel",
            text=DataSourceLabel.__UNINITIALISED_TEXTBIT_
        );

        self.__textBit.grid(column=0, row=0, sticky="nw");

        self.__linkBit = ttk.Label(
            master=self,
            style="vdb.link.TLabel",
            text=DataSourceLabel.__UNINITIALISED_LINKBIT_,
            cursor="hand2"
        );

        self.__linkBit.grid(column=1, row=0, sticky="nw");
        self.__linkBit.bind("<Button-1>", self.__onLinkBitClicked);

        ui_c_floatingToolTip.FloatingToolTip(
            _targetWidget=self.__linkBit,
            _toolTipText="click to see other database-files..."
        );


    def __configureGrid(self) -> None:
        """declares the #columns and #rows"""
        self.grid_columnconfigure(index=(0, 1), weight=1);
        self.grid_rowconfigure(index=0, weight=1);


    def __onLinkBitClicked(self, _event=None) -> None:
        """shows a messagebox, displaying the avaliable *.sqlite files"""

        _currentDatabases_displayString = "\n".join(
            [f"""{" " * 8}• {_dbName}""" for _dbName in db_dbFileManager.DatabaseFileManager.listExistingDatabases_()]
        );

        messagebox.showinfo(
            parent=self,
            title="Databases...",
            message=(
                "These *.sqlite databases...\n\n"
                + _currentDatabases_displayString
                + "\n\n...are available in the /data folder."
                + "\nThe [defaultDatabase] value in the\n`config.ini` file indicates which one to use."
            )
        );


    def setText(self, _numVehiclesShown :int, _dbName :str) -> None:
        """updates the text and link, to reflect the current database-file"""

        self.__textBit.configure(
            text=f"showing {_numVehiclesShown} vehicles from"
        );

        self.__linkBit.configure(
            text=f"{_dbName}.sqlite"
        );