# file:     schemaClasses.py - classes to represent CRUD-able database objects
# author:   Ben Mullan (2025)

import enum, datetime, dataclasses;
from . import (app_configProvider);


@dataclasses.dataclass(frozen=True)
class Vehicle (object):
    """
    represents a vehicle, as stored in the database.
    This is the only file in the codebase to define the
    avaliable vehicle-attributes (regPlate, fuelType, etc.),
    EXCEPT FOR `editVehicleDialog`, `vehicleFilterCriteria`,
    and `filterVehiclesDialog`.
    """


    class VehicleType (enum.Enum):
        """the enumeration of possible vehicle-types"""
        CAR = 1; PICKUPTRUCK = 2; VAN = 3; LORRY = 4;


    class VehicleFuelType (enum.Enum):
        """the enumeration of possible vehicle-fuel-types"""
        PETROL = 1; DIESEL = 2; ELECTRONS = 3;


    regPlate            :str;
    typeOfVehicle       :VehicleType;
    fuelType            :VehicleFuelType;
    makeAndModel        :str;
    isCurrentlyTaxed    :bool;
    manufacturedDate    :datetime.datetime;
    taxExpiryDate       :datetime.datetime|None;
    lastServicedDate    :datetime.datetime|None;


    @staticmethod
    def getTableCreationSql_() -> str:
        """
        returns the SQL neesed to create a table for storing vehicle records.
        **IMPORTANT** → dates are stored using the SQL `INTEGER` type, as unix-epoch timestamps.
        """

        return f"""
            CREATE TABLE "{ app_configProvider.getGlobalConfig()["database"]["vehiclesTableName"] }" (
                "regPlate"          TEXT    NOT NULL COLLATE NOCASE CHECK ((length("regPlate") > 2) AND (length("regPlate") < 10)),
                "typeOfVehicle"     TEXT    NOT NULL COLLATE NOCASE CHECK ("typeOfVehicle" IN ('car', 'pickupTruck', 'van', 'lorry')),
                "fuelType"          TEXT    NOT NULL COLLATE NOCASE CHECK ("fuelType" IN ('petrol', 'diesel', 'electrons')),
                "makeAndModel"      TEXT    NOT NULL COLLATE NOCASE,
                "isCurrentlyTaxed"  INTEGER NOT NULL CHECK ("isCurrentlyTaxed" IN (0, 1)),
                "manufacturedDate"  INTEGER NOT NULL,
                "taxExpiryDate"     INTEGER,
                "lastServicedDate"  INTEGER,
                PRIMARY KEY ("regPlate")
            );
        """;


    @staticmethod
    def getEmptyVehicle_() -> "Vehicle":
        """returns an empty vehicle (for showing nothing in an editVehicleDialog)"""

        return Vehicle(
            regPlate="",
            typeOfVehicle=Vehicle.VehicleType.CAR,
            fuelType=Vehicle.VehicleFuelType.PETROL,
            makeAndModel="",
            isCurrentlyTaxed=False,
            manufacturedDate=None,
            taxExpiryDate=None,
            lastServicedDate=None
        );


    def serialiseToDict(self) -> dict[str, any]:
        """serialises each property appropriately (for db-storage)"""

        return {
            "regPlate"          : self.regPlate,
            "typeOfVehicle"     : self.typeOfVehicle.name.lower(),
            "fuelType"          : self.fuelType.name.lower(),
            "makeAndModel"      : self.makeAndModel,
            "isCurrentlyTaxed"  : self.isCurrentlyTaxed,
            "manufacturedDate"  : Vehicle.serialiseDatetime_(self.manufacturedDate),
            "taxExpiryDate"     : Vehicle.serialiseDatetime_(self.taxExpiryDate),
            "lastServicedDate"  : Vehicle.serialiseDatetime_(self.lastServicedDate)
        };


    def toDisplayTuple(self) -> tuple[str]:
        """returns an in-order tuple of all vehicle properties, suitable for DataGrid insertion"""

        return (
            self.regPlate,
            self.typeOfVehicle.name.lower(),
            self.fuelType.name.lower(),
            self.makeAndModel,
            "yes" if self.isCurrentlyTaxed else "no",
            Vehicle.getFormattedDate_(self.manufacturedDate),
            Vehicle.getFormattedDate_(self.taxExpiryDate),
            Vehicle.getFormattedDate_(self.lastServicedDate)
        );


    @staticmethod
    def fromSerialisedDict_(_dict :dict[str, any]) -> "Vehicle":
        """side-loading constructor: instanciates a Vehicle() from the db-derived dict"""

        return Vehicle(
            regPlate            = _dict["regPlate"],
            typeOfVehicle       = Vehicle.VehicleType[_dict["typeOfVehicle"].upper()],
            fuelType            = Vehicle.VehicleFuelType[_dict["fuelType"].upper()],
            makeAndModel        = _dict["makeAndModel"],
            isCurrentlyTaxed    = bool(_dict["isCurrentlyTaxed"]),
            manufacturedDate    = Vehicle.deserialiseDatetime_(_dict["manufacturedDate"]),
            taxExpiryDate       = Vehicle.deserialiseDatetime_(_dict["taxExpiryDate"]),
            lastServicedDate    = Vehicle.deserialiseDatetime_(_dict["lastServicedDate"])
        );


    @staticmethod
    def serialiseDatetime_(_datetime :datetime.datetime|None) -> int|None:
        """returns either the timestamp() int, or None"""
        return int(_datetime.timestamp()) if (_datetime is not None) else (None);


    @staticmethod
    def deserialiseDatetime_(_timestamp :int|None) -> datetime.datetime|None:
        """returns either the timestamp-derived datetime, or None"""
        return datetime.datetime.fromtimestamp(_timestamp) if (_timestamp is not None) else (None);


    @staticmethod
    def getFormattedDate_(_datetime :datetime.datetime|None) -> str:
        """returns in the format 30-02-2011"""
        return _datetime.strftime("%d-%m-%Y") if (_datetime is not None) else "(never)";