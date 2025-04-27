# file:     dbFileManager.py - logic for creating NEW *.sqlite files (in /data)
# author:   Ben Mullan (2025)

import os, pathlib, sqlite3
from . import (app_filesysUtils, app_constants, app_configProvider, db_schemaClasses);


class DatabaseFileManager (object):
    """static methods for managing and creating NEW *.sqlite files (in /data)"""


    @staticmethod
    def __getDbConfig_() -> dict[str, str]:
        """[static] returns the [database] section of config.ini"""
        return app_configProvider.getGlobalConfig()["database"];


    @staticmethod
    def getFullDbPath_fromDbName_(_dbName :str) -> str:
        """resolves the full file-path, i.e. {_dbName}.sqlite in the /data folder"""
        return app_filesysUtils.resolvePath_relativeToMainPy(f"{app_constants.DB_DATABASES_FOLDER}/{_dbName}.{app_constants.DB_DATABASE_FILE_EXTENSION}");


    @staticmethod
    def listExistingDatabases_() -> list[str]:
        """
        returns JUST THE NAMES of currently-existent databases in the /data directory,
        without their file-extensions.
        """

        _dataDir = app_filesysUtils.resolvePath_relativeToMainPy(f"{app_constants.DB_DATABASES_FOLDER}/");

        return [
            pathlib.Path(_file).stem
            for _file in os.listdir(_dataDir)
            if _file.endswith(app_constants.DB_DATABASE_FILE_EXTENSION)
        ];


    @staticmethod
    def createNewVehiclesDb_(_dbName :str) -> None:
        """
        creates a new *.sqlite file in the /data folder, initialising it with
        a valid empty `allVehicles` table.

        Parameters:
        _dbName (str): JUST THE (file-extension-less) NAME for the database file;
            the resultant path will be `/data/{_dbName}.sqlite`.
        """

        _dbFile_fullPath :str = DatabaseFileManager.getFullDbPath_fromDbName_(_dbName);

        with sqlite3.connect(_dbFile_fullPath) as _dbConnection:
            _dbConnection.cursor().execute(
                db_schemaClasses.Vehicle.getTableCreationSql_()
            );


    @staticmethod
    def vehiclesDatabaseExists_andIsValid_(_dbName :str) -> bool:
        """
        determines whether the pointed-to file is...
            - existent & accessible
            - a file (as distinct from a directory)
            - a valid sqlite3 database
            - containing a `allVehicles` table

        Parameters:
        _dbName (str): JUST THE NAME of an *.sqlite file in the /data directory,
            without a file-extension; eg `vehicles`.

        Returns:
        bool: True if the database file is valid, False otherwise
        """

        _dbFile_fullPath :str = DatabaseFileManager.getFullDbPath_fromDbName_(_dbName);

        def _dbContainsValidVehiclesTable_(_dbFile_fullPath :str) -> bool:
            with sqlite3.connect(_dbFile_fullPath) as _dbConnection:

                _dbCursor = _dbConnection.cursor();

                _dbCursor.execute(
                    f"""
                        SELECT "name" FROM "sqlite_master"
                        WHERE type='table' AND name='{ DatabaseFileManager.__getDbConfig_()["vehiclesTableName"] }';
                    """
                );

                return (_dbCursor.fetchone() is not None);

        return (
            os.path.exists(_dbFile_fullPath)
            and os.path.isfile(_dbFile_fullPath)
            and _dbContainsValidVehiclesTable_(_dbFile_fullPath)
        );