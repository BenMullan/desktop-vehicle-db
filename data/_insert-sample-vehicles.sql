/*
    file:     _insert-sample-vehicles.sql - inserts 30 example vehicles into an already-existent allVehicles table in a *.sqlite file
    exec:     sqlite3.exe ./vehicles.sqlite < ./_insert-sample-vehicles.sql
    author:   Ben Mullan (2025)
*/

INSERT INTO "allVehicles"
    ("regPlate", "typeOfVehicle", "fuelType", "makeAndModel", "isCurrentlyTaxed", "manufacturedDate", "taxExpiryDate", "lastServicedDate")
VALUES
    ('GW14 YMZ',  'car',          'petrol',     'Ford Fiesta',           1,  strftime('%s', '2007-06-15'),  strftime('%s', '2023-03-10'),  strftime('%s', '2028-11-20') ),
    ('AB01 CDE',  'car',          'diesel',     'Vauxhall Corsa',        1,  strftime('%s', '2010-04-25'),  strftime('%s', '2022-07-14'),  strftime('%s', '2025-09-30') ),
    ('CD23 EFG',  'van',          'electrons',  'Ford Transit',          1,  strftime('%s', '2015-08-19'),  NULL,                          strftime('%s', '2023-05-22') ),
    ('EF45 GHI',  'lorry',        'electrons',  'Mercedes Actros',       1,  strftime('%s', '2018-01-10'),  strftime('%s', '2024-12-05'),  NULL                         ),
    ('GH67 IJK',  'pickupTruck',  'diesel',     'Toyota Hilux',          0,  strftime('%s', '2012-09-17'),  strftime('%s', '2022-04-18'),  strftime('%s', '2022-06-25') ),
    ('IJ89 LMN',  'car',          'petrol',     'Volkswagen Golf',       1,  strftime('%s', '2011-11-23'),  NULL,                          NULL                         ),
    ('KL10 OPQ',  'car',          'petrol',     'BMW 1 Series',          1,  strftime('%s', '2019-02-14'),  strftime('%s', '2024-08-09'),  strftime('%s', '2023-10-12') ),
    ('MN11 RST',  'van',          'diesel',     'Volkswagen Golf',       1,  strftime('%s', '2013-05-30'),  strftime('%s', '2023-01-20'),  strftime('%s', '2021-03-15') ),
    ('MP12 UVW',  'lorry',        'diesel',     'Scania R-Series',       1,  strftime('%s', '2016-07-11'),  strftime('%s', '2023-09-27'),  strftime('%s', '2023-12-01') ),
    ('QR13 XYZ',  'car',          'petrol',     'Audi A3',               1,  strftime('%s', '2010-10-05'),  NULL,                          strftime('%s', '2022-02-28') ),
    ('ST14 ABC',  'car',          'diesel',     'Peugeot 208',           0,  strftime('%s', '2008-03-18'),  strftime('%s', '2020-06-12'),  strftime('%s', '2019-08-23') ),
    ('UV15 DEF',  'lorry',        'electrons',  'MAN TGX',               1,  strftime('%s', '2020-12-07'),  strftime('%s', '2025-04-16'),  strftime('%s', '2023-11-19') ),
    ('WX16 GHI',  'pickupTruck',  'electrons',  'Isuzu D-Max',           1,  strftime('%s', '2014-01-22'),  strftime('%s', '2022-05-13'),  strftime('%s', '2022-07-30') ),
    ('YZ17 JKL',  'car',          'petrol',     'Mini Cooper',           1,  strftime('%s', '2017-04-09'),  strftime('%s', '2023-08-21'),  NULL                         ),
    ('ZA18 MNO',  'van',          'diesel',     'Renault Trafic',        1,  strftime('%s', '2011-06-03'),  strftime('%s', '2021-10-17'),  NULL                         ),
    ('AB19 PQR',  'car',          'petrol',     'Honda Civic',           1,  strftime('%s', '2005-09-12'),  NULL,                          NULL                         ),
    ('CD20 STU',  'lorry',        'diesel',     'Volvo FH',              1,  strftime('%s', '2013-11-29'),  strftime('%s', '2022-02-14'),  strftime('%s', '2021-05-06') ),
    ('EF21 VWX',  'pickupTruck',  'diesel',     'Ford Ranger',           1,  strftime('%s', '2018-08-04'),  strftime('%s', '2024-03-25'),  strftime('%s', '2023-07-18') ),
    ('GH22 YZA',  'car',          'petrol',     'Skoda Octavia',         1,  strftime('%s', '2015-02-27'),  strftime('%s', '2023-06-30'),  strftime('%s', '2022-09-11') ),
    ('IJ23 BCD',  'van',          'diesel',     'Mercedes Vito',         1,  strftime('%s', '2009-05-08'),  strftime('%s', '2021-12-22'),  NULL                         ),
    ('KL24 EFG',  'car',          'electrons',  'Nissan Leaf',           0,  strftime('%s', '2021-03-14'),  strftime('%s', '2025-11-03'),  strftime('%s', '2023-04-27') ),
    ('MN25 HIJ',  'car',          'petrol',     'Skoda Fabia',           1,  strftime('%s', '2003-07-19'),  strftime('%s', '2020-01-05'),  strftime('%s', '2019-02-16') ),
    ('OP26 KLM',  'lorry',        'diesel',     'DAF XF',                1,  strftime('%s', '2016-10-23'),  strftime('%s', '2023-05-09'),  strftime('%s', '2023-08-14') ),
    ('QR27 NOP',  'pickupTruck',  'diesel',     'Mitsubishi Triton',     1,  strftime('%s', '2012-11-01'),  strftime('%s', '2022-03-07'),  strftime('%s', '2021-06-20') ),
    ('ST28 QRS',  'van',          'diesel',     'Iveco Daily',           1,  strftime('%s', '2000-02-11'),  strftime('%s', '2018-09-15'),  strftime('%s', '2017-12-29') ),
    ('UV29 TUV',  'car',          'petrol',     'Toyota Yaris',          1,  strftime('%s', '2019-06-26'),  strftime('%s', '2024-10-08'),  strftime('%s', '2023-01-31') ),
    ('WX20 VWX',  'car',          'petrol',     'Vauxhall Astra',        1,  strftime('%s', '2006-12-18'),  strftime('%s', '2021-07-23'),  NULL                         ),
    ('YZ21 XYZ',  'lorry',        'diesel',     'Mercedes-Benz Actros',  1,  strftime('%s', '2022-04-02'),  NULL,                          strftime('%s', '2023-11-07') ),
    ('ZA22 BCD',  'pickupTruck',  'diesel',     'Nissan Navara',         1,  strftime('%s', '2014-08-28'),  strftime('%s', '2022-02-19'),  strftime('%s', '2021-10-04') ),
    ('BC23 EFG',  'car',          'electrons',  'Hyundai i30',           0,  strftime('%s', '2004-01-13'),  strftime('%s', '2021-05-27'),  strftime('%s', '2029-09-09') )
;
