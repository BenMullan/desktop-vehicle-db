# file:     dataGrid.py - tabular-grid ui component
# author:   Ben Mullan (2025)

import tkinter; from tkinter import ttk;


class DataGrid (ttk.Treeview):
    """ui-component: grid of tabular data-cells"""


    def __init__(self, _parentComponent :tkinter.Widget, **kwargs) -> None:
        """instanciates the ui-component"""
        super().__init__(master=_parentComponent, **kwargs);
        self.__configureSelf();


    def __configureSelf(self) -> None:
        """initialises the ui-component's properties and children"""
        self.configure(show="headings");


    def clearAllRecords(self) -> None:
        """removes all rows of data"""
        for _row in self.get_children():
            self.delete(_row);