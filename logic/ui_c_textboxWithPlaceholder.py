# file:     textboxWithPlaceholder.py - textbox with greyed-out text ui component
# author:   Ben Mullan (2025)

import tkinter, contextlib; from tkinter import ttk;
from . import (app_constants, ui_c_floatingToolTip);


class TextboxWithPlaceholder (ttk.Entry):
    """ui-component: textbox with greyed-out placeholder text"""


    __PLACEHOLDER_TEXT_COLOUR_          :str = app_constants.UI_COLOUR_GREY;
    __NORMAL_TEXT_COLOUR_               :str = app_constants.UI_COLOUR_OFFBLACK; # prob make a bit darker

    __placeholderText                   :str;
    __textChangeMonitor                 :tkinter.StringVar;
    __internalTextChange_isInProgress   :bool;


    def __init__(self, _parentComponent :tkinter.Widget, _placeholderText :str, **kwargs) -> None:
        """instantiates the ui-component"""

        super().__init__(master=_parentComponent, **kwargs);
        self.__placeholderText = _placeholderText;
        self.__internalTextChange_isInProgress = False;
        self.__textChangeMonitor = tkinter.StringVar(master=self);
        self.configure(textvariable=self.__textChangeMonitor);
        self.__textChangeMonitor.trace_add("write", self.__onTextChanged);

        ui_c_floatingToolTip.FloatingToolTip(self, _placeholderText);
        self.bind("<FocusIn>", self.__clearPlaceholderText);
        self.bind("<FocusOut>", self.__restorePlaceholderText);

        self.__showPlaceholderText();


    @contextlib.contextmanager
    def __surpressInternalTextChange(self):
        """executes the payload without triggering __onTextChanged"""
        self.__internalTextChange_isInProgress = True;
        try: yield;
        finally: self.__internalTextChange_isInProgress = False;


    def __onTextChanged(self, *_unusedArgs) -> None:
        if self.__internalTextChange_isInProgress: return;
        if (super().get() == "") and (self != self.focus_get()): self.__showPlaceholderText();
        else: self["foreground"] = TextboxWithPlaceholder.__NORMAL_TEXT_COLOUR_;


    def __showPlaceholderText(self) -> None:
        with self.__surpressInternalTextChange():
            self.delete(0, tkinter.END);
            super().insert(index=0, string=self.__placeholderText);
            self.icursor(index=0);
            self["foreground"] = TextboxWithPlaceholder.__PLACEHOLDER_TEXT_COLOUR_;


    def __clearPlaceholderText(self, _event=None) -> None:
        with self.__surpressInternalTextChange():
            if (super().get() == self.__placeholderText):
                self.delete(0, tkinter.END);
                self["foreground"] = TextboxWithPlaceholder.__NORMAL_TEXT_COLOUR_;


    def __restorePlaceholderText(self, _event=None) -> None:
        with self.__surpressInternalTextChange():
            if (not super().get()):
                self.delete(0, tkinter.END);
                super().insert(0, self.__placeholderText);
                self["foreground"] = TextboxWithPlaceholder.__PLACEHOLDER_TEXT_COLOUR_;


    def get(self) -> str:
        """returns an empty string if the placeholder-text is shown"""

        return (
            ""
            if (super().get() == self.__placeholderText)
            else super().get()
        );


    def insert(self, index, string):
        """shows the placeholder-text, if the inserted string is empty"""

        if (string == ""):
            self.__showPlaceholderText();
            return;

        if (super().get() == self.__placeholderText):
            self.delete(0, tkinter.END);
            self["foreground"] = TextboxWithPlaceholder.__NORMAL_TEXT_COLOUR_;

        self.__clearPlaceholderText();
        super().insert(index, string);