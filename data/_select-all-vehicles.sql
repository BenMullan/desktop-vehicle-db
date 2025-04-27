/*
    file:     _select-all-vehicles.sql - formats the dates as human-readable, beside the unix-epoch timestamps in the DB
    exec:     sqlite3.exe ./vehicles.sqlite < ./_select-all-vehicles.sql
    author:   Ben Mullan (2025)
*/

SELECT 
    *,
    date("manufacturedDate",  'unixepoch') AS manufacturedDate_humanReadable,
    date("taxExpiryDate",     'unixepoch') AS taxExpiryDate_humanReadable,
    date("lastServicedDate",  'unixepoch') AS lastServicedDate_humanReadable
FROM
    "allVehicles"
;
