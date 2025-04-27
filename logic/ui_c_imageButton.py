# file:     imageButton.py - button-with-image ui component
# author:   Ben Mullan (2025)

import tkinter; from tkinter import ttk;


class ImageButton (ttk.Button):
    """ui-component: clickable button with [icon][ {text}]"""


    __iconImage :tkinter.PhotoImage;
    """the icon displayed to the left of the text"""

    __commandToRun :callable;
    """the function to execute when clicked/[Enter]ed/[Space]ed"""


    def __init__(self, _parentComponent :tkinter.Widget, _text :str, _iconFilepath :str, _command :callable, **kwargs) -> None:
        """instanciates the ui-component"""

        _SPACES_BETWEEN_ICON_AND_TEXT :int = 2;
        self.__iconImage :tkinter.PhotoImage = tkinter.PhotoImage(master=_parentComponent, file=_iconFilepath);

        super().__init__(
            master=_parentComponent,
            text=f"""{" " * _SPACES_BETWEEN_ICON_AND_TEXT}{_text}""",
            image=self.__iconImage,
            compound=tkinter.LEFT,
            style="vdb.withIcon.TButton",
            **kwargs
        );

        [
            self.bind(_trigger, self.__onClickedOrEnterPressed) for _trigger in [
                *[f"<Button-{_i}>" for _i in range(1, 4, 1)],
                "<Return>", "<space>"
            ]
        ];

        self.configure(underline=_SPACES_BETWEEN_ICON_AND_TEXT);
        self.__commandToRun = _command;
        self.__configureSelf();


    def __configureSelf(self) -> None:
        """initialises the ui-component's properties and children"""
        return;


    def __onClickedOrEnterPressed(self, _event=None):
        """fired whenever any of the three mouse buttons, or [Enter] are used"""
        self.__commandToRun(_event);