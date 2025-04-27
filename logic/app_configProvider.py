# file:     configProvider.py - provices global configuration-values from `main.pyw/../config.ini`
# author:   Ben Mullan (2025)

import os, sys, configparser;
from . import (app_constants, app_filesysUtils, app_errorHandling);


def getGlobalConfig() -> dict[str, dict[str, str]|None]:
    """
    provides globally-scoped readonly configuration-values

    detects whether the method is running under pytest, and if so,
    returns a patched-out version of the configuration-values.
    """

    if ("pytest" in sys.modules):

        print(
            "\n\n** getGlobalConfig() is running under pytest"
            + "or sphinx; returning a patched-out dict ***\n\n"
        );

        return {
            "database" : {
                "defaultDatabase" : "vehicles",
                "vehiclesTableName" : "allVehicles"
            },
            "userInterface" : {
                "showDebuggingBorders" : "false",
                "mainWindowSize" : "950x420"
            }
        };

    _configParser = configparser.ConfigParser(strict=True);
    _configParser.optionxform = str; # preserve keys' case

    _configIni_fullPath :str = app_filesysUtils.resolvePath_relativeToMainPy(
        app_constants.CONFIG_INI_FILENAME
    );

    if not os.path.isfile(_configIni_fullPath):

        _errorMsg :str = (
            "The `config.ini` file doesn't seem to exist!"
            + "\n\n(It ought to be next to `main.pyw`;"
            + f""" the full expected path was "{_configIni_fullPath}")"""
            + "\n\n((If running under pytest, and this is a messagebox, then"
            + """ the `if "pytest" in sys.modules: ...` check hasn't worked.))"""
        );

        if app_constants.DEBUG_DONT_CATCH_EXCEPTIONS:
            raise FileNotFoundError(_errorMsg);

        app_errorHandling.showErrorMessage_andExit(
            _message=_errorMsg,
            _existingRootWindow=None
        );

    _configParser.read(_configIni_fullPath);

    return {
        _section: dict(_configParser.items(_section))
            for _section in _configParser.sections()
    };