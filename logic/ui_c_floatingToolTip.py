# file:     floatingToolTip.py - un-mounted-text-label (non-tk-subclassed) ui component
# author:   Ben Mullan (2025)

import tkinter;
from . import (app_constants);


class FloatingToolTip (object):
    """
    ui-component: unmounted description-text

    example: to create a ToolTip on an existing widget:
    _tooltip = FloatingToolTip(_someButton, "click to refresh");
    """


    __TOOLTIP_PIXEL_OFFSET_ :int = -3;
    """[static] the x & y offset from the target widget's top-left"""

    __toolTipWindow :tkinter.Toplevel;
    """the window shown for the tooltip"""

    __targetWidget :tkinter.Widget;
    """the widget to apply the tooltip to, when it's moused-over"""

    __toolTipText :str;
    """a text description for the target-widget"""


    def __init__(self, _targetWidget :tkinter.Widget, _toolTipText :str) -> None:
        """instanciates the ui-component (non-tk-subclassed)"""

        if (_targetWidget is None): raise ValueError("the tool-tip's _targetWidget was None");

        self.__toolTipWindow = None;
        self.__targetWidget = _targetWidget;
        self.__toolTipText = _toolTipText;

        self.__targetWidget.bind("<Enter>", self.__showToolTipWindow);
        self.__targetWidget.bind("<Leave>", self.__hideToolTipWindow);


    def __showToolTipWindow(self, _event :tkinter.Event = None) -> None:
        """ensures the tool-tip isn't already shown"""

        if (self.__toolTipWindow is not None) or (not self.__targetWidget.winfo_ismapped()):
            #raise Exception("the tool-tip can't be shown because its target-widget isn't mounted onto a parent window yet");
            print("(a tool-tip can't be shown because its target-widget isn't mounted onto a parent-window yet)");
            return;

        self.__targetWidget.update_idletasks();

        self.__toolTipWindow = tkinter.Toplevel(master=self.__targetWidget);
        self.__toolTipWindow.attributes("-topmost", True);
        self.__toolTipWindow.wm_overrideredirect(True); # remove window decorations

        self.__toolTipWindow.wm_geometry(
            f"""+{
                self.__targetWidget.winfo_rootx()
                + int(self.__targetWidget.winfo_width() * 0.1)
                + FloatingToolTip.__TOOLTIP_PIXEL_OFFSET_
            }+{
                self.__targetWidget.winfo_rooty()
                + self.__targetWidget.winfo_height()
                + FloatingToolTip.__TOOLTIP_PIXEL_OFFSET_
            }"""
        );

        tkinter.Label(
            master=self.__toolTipWindow,
            text=self.__toolTipText,
            background=app_constants.UI_COLOUR_BACKGROUND_TOOLTIP,
            relief="solid",
            borderwidth=1
        ).pack();


    def __hideToolTipWindow(self, _event :tkinter.Event = None) -> None:
        """ensures the tool-tip window is currently shown"""

        if (self.__toolTipWindow is None): return;

        self.__toolTipWindow.destroy();
        self.__toolTipWindow = None;