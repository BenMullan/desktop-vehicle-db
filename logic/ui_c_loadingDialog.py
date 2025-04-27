# file:     loadingDialog.py - task-in-progress window ui component
# author:   Ben Mullan (2025)

import tkinter; from tkinter import ttk;
from . import (app_constants);


class LoadingDialog (tkinter.Toplevel):
    """ui-component: task-in-progress window"""


    __taskDescription :str = "(no task description)";
    """rendered below the progress-bar on the dialog window"""


    def __init__(self, _parentWindow :tkinter.Misc, _taskDescription :str, **kwargs) -> None:
        """instanciates the ui-component"""

        super().__init__(master=_parentWindow, **kwargs);
        self.withdraw(); # hide dialog, until showDialog() called

        self.__taskDescription = _taskDescription;
        self.__configureSelf();


    def __configureSelf(self) -> None:
        """initialises the ui-component's properties and children"""

        # self.protocol("WM_DELETE_WINDOW", lambda : None); # disable the [x] button
        self.transient(master=self.master);                 # stay on top of parent window
        self.attributes("-topmost", True);                  # make dialog topmost
        self.grab_set();                                    # intercept all window-events

        self.title("Please wait...");
        self.geometry("300x100");
        self.resizable(False, False);

        _progressBar = ttk.Progressbar(
            master=self,
            mode="indeterminate"
        );

        _progressBar.pack(anchor="center", fill=tkinter.X, pady=(25, 5), padx=20);
        _progressBar.start();

        _taskDescriptionLabel = ttk.Label(
            master=self,
            text=self.__taskDescription,
            font=(app_constants.UI_TYPEFACE, 10, "bold")
        );

        _taskDescriptionLabel.pack(anchor="center", pady=(5, 5), padx=5);


    def __centerSelfToParentWindow(self) -> None:
        """centers the dialog relative to the parent Toplevel() window"""

        if self.winfo_viewable(): self.update_idletasks(); # enter message-pump temporarily
        _x = self.master.winfo_rootx() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2);
        _y = self.master.winfo_rooty() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2);
        self.geometry(f"+{_x}+{_y}");


    def showDialog(self) -> None:
        """
        shows access to the dialog until dismissDialog() is called,
        blocking access to the _parentWindow who instanciated it.

        example usage:
            _loadingDialog = ui_c_loadingDialog.LoadingDialog(self, "processing something...");
            _loadingDialog.showDialog();

            def _backgroundTask():
                import time; time.sleep(5);
                _loadingDialog.dismissDialog();

            import threading;
            threading.Thread(target=_backgroundTask, args=()).start();
        """

        # prevent interaction with the parent window
        # self.master.protocol("WM_DELETE_WINDOW", lambda : None);

        # show thyself
        self.deiconify(); self.lift(); self.focus_set(); self.wait_visibility();
        self.after(100, self.__centerSelfToParentWindow);


    def dismissDialog(self) -> None:
        """closes the currently-open loading dialog"""

        if not self.winfo_viewable(): raise RuntimeError("cannot dismissDialog() because the loading-dialog isn't currently shown");

        # re-enable the parent-window's [x] button, & close self
        # self.master.protocol("WM_DELETE_WINDOW", self.master.destroy);

        self.destroy();