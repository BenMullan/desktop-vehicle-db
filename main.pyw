"""
    file:   main.pyw - entrypoint for vehicle-db programme
    author: Ben Mullan (2025)
    exec:   {python or pythonw} ./main.py
"""

import sys;
from logic import ui_uiRenderer;


def main() -> int:
    """vehicle-db entrypoint"""

    _uiRenderer = ui_uiRenderer.UiRenderer();
    _uiRenderer.runMainWindow();

    return 0;


if __name__ == "__main__": sys.exit(main());