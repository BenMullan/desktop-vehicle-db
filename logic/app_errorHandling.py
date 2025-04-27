# file:     errorHandling.py - provices global Exception-recovery and -shutdown methods
# author:   Ben Mullan (2025)

import sys, tkinter, typing, contextlib;
from tkinter import messagebox;
from . import (app_constants);


def overrideDefaultExceptionHandler() -> None:
    """overrides the default stderr hook, to show a messagebox on unhandled exceptions"""

    sys.excepthook = __handleFatalException_withMessageBox;


def __handleFatalException_withMessageBox(_excType :type, _excValue :BaseException, _traceback :any) -> None:
    """shows the exception in a messagebox, then causes the programme to terminate"""

    _errorMsg :str = f"There's been a global {_excType.__name__}.\n\n{_excValue}";

    if app_constants.DEBUG_DONT_CATCH_EXCEPTIONS:

        _exceptionToRaise = None;

        try: _exceptionToRaise = _excType(_excValue).with_traceback(_traceback);
        except Exception: _exceptionToRaise = Exception(_errorMsg);
        raise _exceptionToRaise;

    showErrorMessage_andExit(_message=_errorMsg, _existingRootWindow=None);


def showErrorMessage_andExit(_message :str, _existingRootWindow :tkinter.Tk|None = None) -> None:
    """stderr + shows error-messagebox, and terminates execution with exit-code 1"""

    print(f"""handling fatal exception (..."{_message[-20:]}") with messagebox, then exiting with error-code 1...\n""");

    with yieldTkinterRoot(_existingRootWindow) as _parentWindow:

        messagebox.showerror(
            parent=_parentWindow,
            title="Oh dear...",
            message=f"{_message}\n\n(vehicle-db will now close)"
        );

    sys.exit(1);


def showWarningMessage_butDontExit(_message :str, _existingRootWindow :tkinter.Tk|None = None) -> None:
    """stderr + shows warning-messagebox - with an independant, isolated Tk() parent window, if needed"""

    print(f"""handling non-fatal exception (..."{_message[-20:]}") with messagebox...""");

    with yieldTkinterRoot(_existingRootWindow) as _parentWindow:

        messagebox.showwarning(
            parent=_parentWindow,
            title="Ahh...",
            message=_message
        );


@contextlib.contextmanager
def yieldTkinterRoot(_existingRoot :tkinter.Tk|None = None) -> typing.Generator[tkinter.Tk, None, None]:
    """instanciates & yields eine neue tempoary Tk(), unless _existingRoot is valid"""

    try:

        _hiddenParentWindow :tkinter.Tk = None;

        if (_existingRoot is None) or (not _existingRoot.winfo_exists()):
            _hiddenParentWindow = tkinter.Tk();
            _hiddenParentWindow.withdraw();

        yield (_hiddenParentWindow or _existingRoot);

    finally:

        if (_hiddenParentWindow is not None):
            _hiddenParentWindow.destroy();