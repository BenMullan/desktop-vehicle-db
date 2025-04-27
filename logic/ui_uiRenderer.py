# file:     uiRenderer.py - abstracts the tkinter gui
# author:   Ben Mullan (2025)

import tkinter; from tkinter import ttk;
from . import (app_configProvider, app_constants, app_errorHandling, ui_c_mainWindow);


class UiRenderer (object):
    """provides methods to render the tcl-based gui"""


    __ttkStyles :ttk.Style = None;
    """ui-component styles in the current ttk context"""


    @staticmethod
    def __getUiConfig_() -> dict[str, str]:
        """[static] returns the [userInterface] section of config.ini"""
        return app_configProvider.getGlobalConfig()["userInterface"];


    def runMainWindow(self) -> None:
        """runs the message-pump for the main window, until it"s closed"""

        try:

            print("(rendering main-window...)");
            app_errorHandling.overrideDefaultExceptionHandler();
            tkinter.NoDefaultRoot();

            _mainWindow = ui_c_mainWindow.MainWindow();
            self.__declareTtkStyles(_mainWindow);
            _mainWindow.mainloop(n=0);

        except Exception as _err:

            # the default exception-hook is overridden;
            # forward the exception hence thither.

            raise _err;


    def __declareTtkStyles(self, _mainWindow :tkinter.Tk) -> None:
        """declares ui-styles in the current ttk context"""

        _borderStyle = (
            {"relief" : "solid", "borderwidth" : 2}
            if (UiRenderer.__getUiConfig_()["showDebuggingBorders"].lower() == "true")
            else {}
        );

        self.__ttkStyles = ttk.Style(master=_mainWindow);

        self.__ttkStyles.configure("vdb.link.TLabel",
            foreground  = app_constants.UI_COLOUR_LINK,
            background  = app_constants.UI_COLOUR_BACKGROUND_MAIN,
            font        = (app_constants.UI_TYPEFACE, app_constants.UI_FONTSIZE_MEDIUM, "underline"),
            **_borderStyle
        );

        self.__ttkStyles.configure("vdb.subtle.TLabel",
            foreground  = app_constants.UI_COLOUR_GREY,
            background  = app_constants.UI_COLOUR_BACKGROUND_MAIN,
            font        = (app_constants.UI_TYPEFACE, app_constants.UI_FONTSIZE_MEDIUM),
            **_borderStyle
        );

        self.__ttkStyles.configure("vdb.dialogsubtle.TLabel",
            foreground  = app_constants.UI_COLOUR_GREY,
            background  = app_constants.UI_COLOUR_BACKGROUND_DIALOG,
            font        = (app_constants.UI_TYPEFACE, app_constants.UI_FONTSIZE_MEDIUM),
            **_borderStyle
        );

        self.__ttkStyles.configure("vdb.labelframed.TLabel",
            foreground  = app_constants.UI_COLOUR_OFFBLACK,
            background  = app_constants.UI_COLOUR_BACKGROUND_LBLFRAME,
            font        = (app_constants.UI_TYPEFACE, app_constants.UI_FONTSIZE_MEDIUM),
            **_borderStyle
        );

        self.__ttkStyles.configure("vdb.accented.TLabel",
            foreground  = app_constants.UI_COLOUR_ACCENTBLUE,
            background  = app_constants.UI_COLOUR_BACKGROUND_MAIN,
            font        = (app_constants.UI_TYPEFACE, app_constants.UI_FONTSIZE_MEDIUM),
            **_borderStyle
        );

        self.__ttkStyles.configure("vdb.withIcon.TButton",
            foreground  = app_constants.UI_COLOUR_OFFBLACK,
            background  = app_constants.UI_COLOUR_BUTTONBORDER,
            font        = (app_constants.UI_TYPEFACE, app_constants.UI_FONTSIZE_MEDIUM),
            **_borderStyle
        );

        self.__ttkStyles.map("vdb.withIcon.TButton",
          foreground    = [("pressed", app_constants.UI_COLOUR_OFFBLACK), ("active", app_constants.UI_COLOUR_OFFBLACK)],
          background    = [("pressed", "darkblue"), ("active", "blue")]
        );

        self.__ttkStyles.configure("vdb.normal.TFrame",
            background  = app_constants.UI_COLOUR_BACKGROUND_MAIN,
            **_borderStyle
        );

        self.__ttkStyles.configure("vdb.dialog.TLabelframe",
            background  = app_constants.UI_COLOUR_BACKGROUND_LBLFRAME,
            **_borderStyle
        );

        self.__ttkStyles.configure("vdb.dialog.TLabelframe.Label",
            background  = app_constants.UI_COLOUR_BACKGROUND_LBLFRAME,
            **_borderStyle
        );

        self.__ttkStyles.configure("Treeview.Heading",
            font        = (app_constants.UI_TYPEFACE, app_constants.UI_FONTSIZE_MEDIUM, "underline")
        );