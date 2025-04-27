/*
    file:     _create-vehicles-table.sql - creates the allVehicles table, in an already-existent *.sqlite file
    exec:     sqlite3.exe ./vehicles.sqlite < ./_create-vehicles-table.sql
    author:   Ben Mullan (2025)
*/

CREATE TABLE "allVehicles" (
    "regPlate"                 TEXT      NOT NULL   COLLATE NOCASE   CHECK ((length("regPlate") > 2) AND (length("regPlate") < 10))     ,
    "typeOfVehicle"            TEXT      NOT NULL   COLLATE NOCASE   CHECK ("typeOfVehicle" IN ('car', 'pickupTruck', 'van', 'lorry'))  ,
    "fuelType"                 TEXT      NOT NULL   COLLATE NOCASE   CHECK ("fuelType" IN ('petrol', 'diesel', 'electrons'))            ,
    "makeAndModel"             TEXT      NOT NULL   COLLATE NOCASE   CHECK (length("makeAndModel") <= 150)                              ,
    "isCurrentlyTaxed"         INTEGER   NOT NULL                    CHECK ("isCurrentlyTaxed" IN (0, 1))                               ,
    "manufacturedDate"         INTEGER   NOT NULL                    CHECK ("manufacturedDate" >= 0)                                    ,
    "taxExpiryDate"            INTEGER                               CHECK ("taxExpiryDate" >= 0)                                       ,
    "lastServicedDate"         INTEGER                               CHECK ("lastServicedDate" >= 0)                                    ,
    PRIMARY KEY ("regPlate")
);
