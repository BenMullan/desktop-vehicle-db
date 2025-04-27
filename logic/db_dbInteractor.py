# file:     dbInteractor.py - provices an interface for vehicles' CRUD operations, on EXISTING *.sqlite files
# author:   Ben Mullan (2025)

import pathlib, sqlite3, contextlib, typing;
from . import (app_configProvider, db_dbFileManager, db_schemaClasses);


class DatabaseInteractor (object):
    """
    provices an interface for vehicles' CRUD operations, on EXISTING ``*.sqlite`` files

    This type is a singleton; a class instanciatable only ONCE per
    running instance of this programme. It prevents re-instantiation
    by throwing a wobbly-fit if a cached instance already exists.
    """


    __singletonInstance_ :"DatabaseInteractor" = None;
    """[static] the one-per-application instance of the DatabaseInteractor"""

    __targetDbFile_fullPath :str = None;
    """the full path to the target sqlite3 database file"""


    def __init__(self, _targetDatabase :str) -> None:
        """
        [private]
        initialises the DatabaseInteractor, ensuring the singleton instance doesn't yet exist

        Parameters:
        _targetDatabase (str): JUST THE (file-extension-less) NAME of an already-existent
        ``*.sqlite file`` in the /data directory; eg `vehicles`.
        """

        # This type is a singleton; a class instanciatable only ONCE per
        # running instance of this programme. Prevent re-instantiation
        # by throwing a wobbly-fit if the cached instance already exists.

        if (DatabaseInteractor.__singletonInstance_ is not None):
            raise Exception("DatabaseInteractor is a singleton; use DatabaseInteractor.getInstance() instead of re-instantiating");

        self.targetDatabase = _targetDatabase;


    @property
    def targetDatabase(self) -> str:
        """returns JUST THE (file-extension-less) NAME of the target sqlite3 database file; eg `vehicles`"""
        return pathlib.Path(self.__targetDbFile_fullPath).stem;


    @targetDatabase.setter
    def targetDatabase(self, _databaseName :str) -> None:
        """
        sets the DatabaseInteractor to point to a different sqlite3 database file

        Parameters:
        _databaseName (str): JUST THE (file-extension-less) NAME of an already-existent
            ``*.sqlite`` file in the /data directory; eg `vehicles`.
        """

        self.__targetDbFile_fullPath = db_dbFileManager.DatabaseFileManager.getFullDbPath_fromDbName_(_databaseName);
        DatabaseInteractor.__ensureDatabaseExists_andIsValid_(_databaseName);


    @staticmethod
    def __getDbConfig_() -> dict[str, str]:
        """[static] returns the [database] section of config.ini"""
        return app_configProvider.getGlobalConfig()["database"];


    @staticmethod
    def getInstance() -> "DatabaseInteractor":
        """returns the one-per-application instance of the DatabaseInteractor"""

        if (DatabaseInteractor.__singletonInstance_ is None):
            DatabaseInteractor.__singletonInstance_ = DatabaseInteractor(
                _targetDatabase=DatabaseInteractor.__getDbConfig_()["defaultDatabase"]
            );

        return DatabaseInteractor.__singletonInstance_;


    @staticmethod
    def __ensureDatabaseExists_andIsValid_(_databaseName) -> None:
        """
        raises an Exception is the db-file isn't existent && valid

        Parameters:
        _databaseName (str): JUST THE (file-extension-less) NAME of an already-existent
        ``*.sqlite`` file in the /data directory; eg `vehicles`.
        """

        if not db_dbFileManager.DatabaseFileManager.vehiclesDatabaseExists_andIsValid_(_databaseName):
            raise Exception(
                f"This file isn't a valid vehicles' database: \"{db_dbFileManager.DatabaseFileManager.getFullDbPath_fromDbName_(_databaseName)}\".\n\n"
                + "This could be because eg the file doesn't exist, or doesn't contain a table named [the value in config.ini's vehiclesTableName]."
            );


    @contextlib.contextmanager
    def __yieldCursor(self) -> typing.Generator[sqlite3.Cursor, None, None]:
        """yields a database cursor, commiting the transaction if successful"""

        DatabaseInteractor.__ensureDatabaseExists_andIsValid_(self.targetDatabase);
        _dbConntection = sqlite3.connect(self.__targetDbFile_fullPath);
        _dbConntection.row_factory = sqlite3.Row;

        try: yield _dbConntection.cursor(); _dbConntection.commit();
        except Exception as _error: _dbConntection.rollback(); raise _error;
        finally: _dbConntection.close();


    #region CRUD-operations


    def addVehicle(self, _newVehicle :db_schemaClasses.Vehicle) -> None:
        """adds the already-instanciated vehicle to the database file"""

        _vehicleAsDict :dict[str, any] = _newVehicle.serialiseToDict();
        _columnsStr :str = ", ".join([f"\"{_prop}\"" for _prop in _vehicleAsDict.keys()]);
        _placeholdersStr :str = ", ".join([f":{_prop}" for _prop in _vehicleAsDict.keys()]);

        with self.__yieldCursor() as _dbCursor: _dbCursor.execute(
            f"""
                INSERT INTO "{ DatabaseInteractor.__getDbConfig_()["vehiclesTableName"] }"
                ({_columnsStr}) VALUES ({_placeholdersStr});
            """,
            _vehicleAsDict
        );


    def updateVehicle_byRegPlate(self, _vehicleRegPlate: str, _updatedVehicle: db_schemaClasses.Vehicle) -> None:
        """updates all properties of the vehicle whose regPlate == _vehicleRegPlate"""

        _vehicleAsDict :dict[str, any] = _updatedVehicle.serialiseToDict();
        _columnsStr = ", ".join([f"\"{_prop}\" = :{_prop}" for _prop in _vehicleAsDict.keys()]);

        with self.__yieldCursor() as _dbCursor: _dbCursor.execute(
            f"""
                UPDATE "{ DatabaseInteractor.__getDbConfig_()["vehiclesTableName"] }"
                SET {_columnsStr} WHERE "regPlate" = :regPlate;
            """,
            {**_vehicleAsDict, "regPlate" : _vehicleRegPlate}
        );


    def deleteVehicle_byRegPlate(self, _vehicleRegPlate: str) -> None:
        """removes the vehicle record whose regPlate == _vehicleRegPlate"""

        with self.__yieldCursor() as _dbCursor: _dbCursor.execute(
            f"""
                DELETE FROM "{ DatabaseInteractor.__getDbConfig_()["vehiclesTableName"] }"
                WHERE "regPlate" = :regPlate;
            """,
            {"regPlate" : _vehicleRegPlate}
        );


    def getVehicle_byRegPlate(self, _vehicleRegPlate: str) -> db_schemaClasses.Vehicle:
        """returns the vehicle record whose regPlate == _vehicleRegPlate, or None"""

        with self.__yieldCursor() as _dbCursor:

            _dbCursor.execute(
                f"""
                    SELECT * FROM "{ DatabaseInteractor.__getDbConfig_()["vehiclesTableName"] }"
                    WHERE "regPlate" = :regPlate;
                """,
                {"regPlate" : _vehicleRegPlate}
            );

            _record = _dbCursor.fetchone();

            return (
                db_schemaClasses.Vehicle.fromSerialisedDict_(dict(_record))
                if (_record is not None)
                else (None)
            );


    def getAllVehicles(self) -> list[db_schemaClasses.Vehicle]:
        """returns all vehicle records in the table; possibly none"""

        with self.__yieldCursor() as _dbCursor:
            _dbCursor.execute(f"""SELECT * FROM "{ DatabaseInteractor.__getDbConfig_()["vehiclesTableName"] }";""");
            _records = _dbCursor.fetchall();
            return [db_schemaClasses.Vehicle.fromSerialisedDict_(dict(_record)) for _record in _records];


    def getVehicleTableColumns(self) -> dict[str, str]:
        """returns a dict of the column-name to its -type"""

        with self.__yieldCursor() as _dbCursor:
            _dbCursor.execute(f"""SELECT "name", "type" FROM pragma_table_info('{ DatabaseInteractor.__getDbConfig_()["vehiclesTableName"] }');""");
            _records = _dbCursor.fetchall();
            return { _record["name"]: _record["type"] for _record in _records };


    #endregion