    ╔═══════════════════════════╗
    ║        Vehicle-DB!        ║
    ╚═══════════════════════════╝
→ a neat-and-tidy desktop CRUD application<br/>
(for creating, editing, deleting, and filtering vehicle records)

<img alt="the application running" src="https://raw.githubusercontent.com/BenMullan/desktop-vehicle-db/main/docs/_static/vehicledbDemo.png" />

Whilst `python`, `tkinter`, and `sqlite3` aren't exactly _conducive_ to well-structured, modular, type-safe code... this software attempts to demonstrate that if one _really_ tries, they can _just about_ be wrangled into some semblance of a competent codebase. Maybe.

    To run this software...
    =======================
    *assuming*:         Python 3.12+, Windows 10+
    1) change dir:      cd into\the\extracted\zip\
    2) run program:     python main.pyw
    *optional*
    3) pre-reqs:        python -m pip install -r requirements.txt
    4) style-check:     python -m flake8 .
    5) unit-tests:      python -m pytest .
    6) sphinx-docs:     docs/_build/html/index.html

<img alt="the application running" src="https://raw.githubusercontent.com/BenMullan/desktop-vehicle-db/main/docs/_static/classDiagramOf_everything.png" />

### `python` - ruinous because...
- no proper access modifiers!
- no namespaces or competent module-ing system
- no block-closing (`}` or `End Function`); poor readability in large files
- can't have consolidated data-member declaration at top of class! (they're just static!😣)
- no declaration-before-definition (leading to type and nonlocal/global keyword nonsense!)
- no compile- or interpret-time checking that symbols exist; you only discover when code-branch run!
- no type-safety! (can have completely the wrong type-annotation on a function, and nothing will warn you!)