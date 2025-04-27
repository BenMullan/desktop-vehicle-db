# file:     constants.py - global hard-coded constants
# author:   Ben Mullan (2025)

CONFIG_INI_FILENAME             = "config.ini";

DB_DATABASES_FOLDER             = "data";
DB_DATABASE_FILE_EXTENSION      = "sqlite";

UI_ASSETS_FOLDER                = "logic/ui-assets";
UI_MAIN_WINDOW_TITLE            = "Vehicle-DB!";
UI_TYPEFACE                     = "Segoe UI";
UI_FONTSIZE_MEDIUM              = 10;

UI_COLOUR_BACKGROUND_MAIN       = "#ffffff";
UI_COLOUR_BACKGROUND_DIALOG     = "#fffff2";
UI_COLOUR_BACKGROUND_LBLFRAME   = "#f7f7f7";
UI_COLOUR_BACKGROUND_TOOLTIP    = "#ffffdd";
UI_COLOUR_OFFBLACK              = "#303030";
UI_COLOUR_OFFWHITE              = "#c0c0c0";
UI_COLOUR_GREY                  = "#909090";
UI_COLOUR_BUTTONBORDER          = "#008ad4";
UI_COLOUR_ACCENTBLUE            = "#2f4f9c";
UI_COLOUR_LINK                  = "#3366cc";

DEBUG_DONT_CATCH_EXCEPTIONS     = False;
"""
if `True`, causes tkinter- and global-exceptions
to be raised, instead of messagebox-ed out,
in order that they can be caught in a debugger.
"""