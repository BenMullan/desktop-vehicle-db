@echo off
setlocal enabledelayedexpansion

rem file:     make-all-rst-files-from-logic.cmd - creates the rst files via batch, because "sphinx" is seemingly far too incompetent to do this
rem exec:     cmd.exe /c make-all-rst-files-from-logic.cmd
rem author:   Ben Mullan (2025)


set "logic_dir=..\logic"
set "docs_dir=."

for %%f in (%logic_dir%\*.py) do (

    set "filename=%%~nf"
    set "rst_file=%docs_dir%\%%~nf.rst"
    
    echo .. automodule:: logic.!filename! > "!rst_file!"
    echo    :members: >> "!rst_file!"
    echo    :undoc-members: >> "!rst_file!"
    echo    :private-members: >> "!rst_file!"
    echo    :special-members: __init__ >> "!rst_file!"
    echo    :show-inheritance: >> "!rst_file!"

)

echo *.rst files created in %cd%
pause
