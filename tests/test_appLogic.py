# file:     test_appLogic.py - unit-tests for the app_* logic files
# author:   Ben Mullan (2025)

import pytest, tkinter;
from . import (_testUtils);

app_configProvider  = _testUtils.importLogicFile("app_configProvider");
app_constants       = _testUtils.importLogicFile("app_constants");
app_errorHandling   = _testUtils.importLogicFile("app_errorHandling");
app_filesysUtils    = _testUtils.importLogicFile("app_filesysUtils");


@pytest.mark.parametrize(
    "_input, _expected",
    [
        ("", ""),
        ("Test", "test"),
        ("testCase", "test-case"),
        ("CamelCase", "camel-case"),
        ("somethingLikeThis", "something-like-this"),
        ("already-kebab-case", "already-kebab-case"),
        ("anotherExampleHere", "another-example-here"),
    ]
)
def test_drinkingCamelCase_toKebabCase(_input :str, _expected :str):

    assert app_filesysUtils.drinkingCamelCase_toKebabCase(_input) == _expected;


def test_drinkingCamelCase_toKebabCase__invalidInput():

    with pytest.raises(TypeError):
        app_filesysUtils.drinkingCamelCase_toKebabCase();

    with pytest.raises(TypeError):
        app_filesysUtils.drinkingCamelCase_toKebabCase(None);


def test_handleException_withMessageBox(mocker):

    _mock_showErrorMessage_andExit = mocker.patch.object(app_errorHandling, "showErrorMessage_andExit");

    app_errorHandling.__handleFatalException_withMessageBox(ValueError, ValueError("test error"), None);
    _mock_showErrorMessage_andExit.assert_called_once();


def test_yieldTkinterRoot():

    with app_errorHandling.yieldTkinterRoot() as _root:
        assert isinstance(_root, tkinter.Tk);
        assert _root.winfo_exists();

    with app_errorHandling.yieldTkinterRoot(_existingRoot=None) as _root:
        assert isinstance(_root, tkinter.Tk);
        assert _root.winfo_exists();

    with app_errorHandling.yieldTkinterRoot(_existingRoot=tkinter.Tk()) as _root:
        assert isinstance(_root, tkinter.Tk);
        assert _root.winfo_exists();


def test_ensureDontCatchExceptions_isFalse():

    assert (app_constants.DEBUG_DONT_CATCH_EXCEPTIONS is False);