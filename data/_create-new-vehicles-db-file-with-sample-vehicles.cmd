@echo off
setlocal EnableDelayedExpansion


rem file:     _create-new-vehicles-db-file-with-sample-vehicles.cmd - creates a new *.sqlite file, and executes the create & insert sql-scripts
rem exec:     cmd.exe /c _create-new-vehicles-db-file-with-sample-vehicles.cmd
rem author:   Ben Mullan (2025)


rem if sqlite3.exe isn't avaliable in %PATH% or %CD%, prompt for it
where sqlite3.exe >nul 2>&1
if errorlevel 1 (
    echo sqlite3.exe wan't found in PATH or the working directory
    set /p "SQLITE_PATH=enter the full path to sqlite3.exe: "
    if not exist "%SQLITE_PATH%" (
        echo the file "%SQLITE_PATH%" does not exist; exiting
        pause
        exit /b 1
    )
    set "SQLITE_EXE=%SQLITE_PATH%"
) else (
    set "SQLITE_EXE=sqlite3.exe"
)


rem prompt for the name of the new database (without extension)
set /p "DB_NAME=enter the name for the new *.sqlite database file (without extension): "
set "DB_FILE=%~dp0%DB_NAME%.sqlite"


rem use `VACUUM` to force sqlite to create the (empty) file
echo creating database file "%DB_FILE%"...
"%SQLITE_EXE%" "%DB_FILE%" "VACUUM;"
if errorlevel 1 (
    echo failed to create the database file
    pause
    exit /b 1
)


rem `%~dp0` expands to the directory of this batch script
echo executing `_create-vehicles-table.sql` on "%DB_FILE%"...
"%SQLITE_EXE%" "%DB_FILE%" < "%~dp0\_create-vehicles-table.sql"
if errorlevel 1 (
    echo failed to execute `_create-vehicles-table.sql`
    pause
    exit /b 1
)


rem `%~dp0` expands to the directory of this batch script
echo executing `_insert-sample-vehicles.sql` on "%DB_FILE%"...
"%SQLITE_EXE%" "%DB_FILE%" < "%~dp0\_insert-sample-vehicles.sql"
if errorlevel 1 (
    echo failed to execute `_insert-sample-vehicles`
    pause
    exit /b 1
)


echo successfully created "%DB_FILE%" with sample-vehicles
echo.
pause
