# file:     _testUtils.py - unit-testing utility functions
# author:   Ben Mullan (2025)

import os, sys, types, importlib.util;


def importLogicFile(_fileWithoutExtension :str) -> types.ModuleType:
    """
    dynamically reaches up-and-out into the logic/ directory,
    to import a file by name.

    example:
        app_filesysUtils = importLogicFile("app_filesysUtils");
    """

    _fullModuleName = f"logic.{_fileWithoutExtension}";
    _fullModulePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logic", f"{_fileWithoutExtension}.py"));

    _moduleSpec = importlib.util.spec_from_file_location(_fullModuleName, _fullModulePath, submodule_search_locations=[os.path.dirname(_fullModulePath)]);
    _actualModule = importlib.util.module_from_spec(_moduleSpec);

    sys.modules[_fullModuleName] = _actualModule;
    _moduleSpec.loader.exec_module(_actualModule);

    return _actualModule;