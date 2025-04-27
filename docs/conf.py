import os, sys;
sys.path.insert(0, os.path.abspath("../"));

project = "Vehicle-DB";
copyright = "2025, Ben Mullan";
author = "Ben Mullan";
release = "1.2";

extensions = [
    "sphinx.ext.autodoc",           # Automatically document docstrings
    "sphinx.ext.napoleon",          # Supports Google and NumPy style docstrings
    "sphinx.ext.autosummary",       # Generate summary tables
    "sphinx_autodoc_typehints",     # Include type hints in the docs
];

templates_path = ["_templates"];
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"];

html_theme = "sphinx_rtd_theme";
html_static_path = ["_static"];
autodoc_default_flags = ["members", "undoc-members", "show-inheritance"];