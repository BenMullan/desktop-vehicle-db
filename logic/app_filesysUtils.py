# file:     filesysUtils.py - filesystem and path utilities
# author:   Ben Mullan (2025)

import os, re, sys;

def resolvePath_relativeToMainPy(_relativePath :str) -> str:
    """returns an absolute fs path, from a relative-to-main.py (actually main.pyw) path"""
    _mainPy_dirPath = os.path.dirname(os.path.abspath(sys.argv[0]));
    return os.path.join(_mainPy_dirPath, _relativePath);


def drinkingCamelCase_toKebabCase(_inputString :str) -> str:
    """takes a string like somethingLikeThis and returns something-like-this"""
    return re.sub(r"(?<!^)(?=[A-Z])", "-", _inputString).lower();