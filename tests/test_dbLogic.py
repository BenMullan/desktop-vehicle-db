# file:     test_dbLogic.py - unit-tests for the db_* logic files
# author:   Ben Mullan (2025)

import pytest, datetime;
from . import (_testUtils);

db_dbFileManager         = _testUtils.importLogicFile("db_dbFileManager");
db_dbInteractor          = _testUtils.importLogicFile("db_dbInteractor");
db_schemaClasses         = _testUtils.importLogicFile("db_schemaClasses");
db_vehicleFilterOptions  = _testUtils.importLogicFile("db_vehicleFilterOptions");


def test_dbInteractor__init__nullDbFilePath():

    with pytest.raises(Exception, match=r"^This file isn't a valid vehicles' database:.*"):
        db_dbInteractor.DatabaseInteractor(None);


def test_dbInteractor_getAllVehicles(mocker):

    _testVehicle1 = {
        "regPlate": "TEST123", "typeOfVehicle": "CAR", "fuelType": "PETROL", "makeAndModel": "Test Model",
        "isCurrentlyTaxed": True, "manufacturedDate": None, "taxExpiryDate": None, "lastServicedDate": None
    };

    _testVehicle2 = {
        "regPlate": "TEST456", "typeOfVehicle": "VAN", "fuelType": "DIESEL", "makeAndModel": "Test VAN",
        "isCurrentlyTaxed": False, "manufacturedDate": None, "taxExpiryDate": None, "lastServicedDate": None
    };

    mocker.patch.object(
        db_dbInteractor.DatabaseInteractor,
        "_DatabaseInteractor__ensureDatabaseExists_andIsValid_",
        return_value=None
    );

    _mock_dbCursor = mocker.Mock();
    _mock_dbCursor.fetchall.return_value = [_testVehicle1, _testVehicle2];

    mocker.patch.object(
        db_dbInteractor.DatabaseInteractor,
        "_DatabaseInteractor__yieldCursor",
        return_value=mocker.MagicMock(__enter__=lambda s: _mock_dbCursor, __exit__=lambda s, exc_type, exc_val, exc_tb: None)
    );

    db_interactor = db_dbInteractor.DatabaseInteractor("__nonexist__");
    db_interactor.getAllVehicles();
    _mock_dbCursor.fetchall.assert_called_once();


def test_vehicle_serialisation_and_deserialisation():

    _testVehicle = db_schemaClasses.Vehicle(
        regPlate="TEST123",
        typeOfVehicle=db_schemaClasses.Vehicle.VehicleType.CAR,
        fuelType=db_schemaClasses.Vehicle.VehicleFuelType.PETROL,
        makeAndModel="Test Model",
        isCurrentlyTaxed=True,
        manufacturedDate=datetime.datetime(2020, 1, 1),
        taxExpiryDate=datetime.datetime(2021, 1, 1),
        lastServicedDate=datetime.datetime(2022, 1, 1)
    );

    _serialised = _testVehicle.serialiseToDict();
    _deserialised = db_schemaClasses.Vehicle.fromSerialisedDict_(_serialised);

    assert (_testVehicle == _deserialised);
    assert (_testVehicle.toDisplayTuple() == _deserialised.toDisplayTuple());


def test_vehicle_getEmptyVehicle():

    _emptyVehicle = db_schemaClasses.Vehicle.getEmptyVehicle_();

    assert (_emptyVehicle.regPlate == "");
    assert (_emptyVehicle.typeOfVehicle == db_schemaClasses.Vehicle.VehicleType.CAR);
    assert (_emptyVehicle.fuelType == db_schemaClasses.Vehicle.VehicleFuelType.PETROL);
    assert (_emptyVehicle.makeAndModel == "");
    assert (_emptyVehicle.isCurrentlyTaxed is False);
    assert (_emptyVehicle.manufacturedDate is None);
    assert (_emptyVehicle.taxExpiryDate is None);
    assert (_emptyVehicle.lastServicedDate is None);


def test_vehicle_serialise_and_deserialise_datetime():

    _datetime = datetime.datetime(2023, 10, 5, 15, 30, 45);
    _timestamp = db_schemaClasses.Vehicle.serialiseDatetime_(_datetime);
    _deserialisedDatetime = db_schemaClasses.Vehicle.deserialiseDatetime_(_timestamp);

    assert (_timestamp == int(_datetime.timestamp()));
    assert (_deserialisedDatetime == _datetime);

    _none_timestamp = db_schemaClasses.Vehicle.serialiseDatetime_(None);
    _deserialised_none = db_schemaClasses.Vehicle.deserialiseDatetime_(_none_timestamp);

    assert (_none_timestamp is None);
    assert (_deserialised_none is None);


def test_vehicleFilterOptions_isSatisfiedBy():

    _testVehicle = db_schemaClasses.Vehicle(
        regPlate="TEST123",
        typeOfVehicle=db_schemaClasses.Vehicle.VehicleType.CAR,
        fuelType=db_schemaClasses.Vehicle.VehicleFuelType.PETROL,
        makeAndModel="Test Model",
        isCurrentlyTaxed=True,
        manufacturedDate=datetime.datetime(2020, 1, 1),
        taxExpiryDate=datetime.datetime(2021, 1, 1),
        lastServicedDate=datetime.datetime(2022, 1, 1)
    );

    _filterOptions = db_vehicleFilterOptions.VehicleFilterOptions(
        only_regPlates_containing="TEST",
        only_these_vehicleTypes={db_schemaClasses.Vehicle.VehicleType.CAR},
        only_these_fuelTypes={db_schemaClasses.Vehicle.VehicleFuelType.PETROL},
        only_makesAndModels_containing="Test",
        must_be_currentlyTaxed=True,
        manufacturedDate_between=(datetime.datetime(2019, 1, 1), datetime.datetime(2021, 1, 1)),
        taxExpiryDate_between=(datetime.datetime(2020, 1, 1), datetime.datetime(2022, 1, 1)),
        lastServicedDate_between=(datetime.datetime(2021, 1, 1), datetime.datetime(2023, 1, 1))
    );

    assert (_filterOptions.isSatisfiedBy(_testVehicle) is True);

    _filterOptions.must_be_currentlyTaxed = False;
    assert (_filterOptions.isSatisfiedBy(_testVehicle) is False);


def test_vehicleFilterOptions_pluckMatchingVehicles():

    _testVehicle1 = db_schemaClasses.Vehicle(
        regPlate="TEST123",
        typeOfVehicle=db_schemaClasses.Vehicle.VehicleType.CAR,
        fuelType=db_schemaClasses.Vehicle.VehicleFuelType.PETROL,
        makeAndModel="Test Model",
        isCurrentlyTaxed=True,
        manufacturedDate=datetime.datetime(2020, 1, 1),
        taxExpiryDate=datetime.datetime(2021, 1, 1),
        lastServicedDate=datetime.datetime(2022, 1, 1)
    );

    _testVehicle2 = db_schemaClasses.Vehicle(
        regPlate="TEST456",
        typeOfVehicle=db_schemaClasses.Vehicle.VehicleType.VAN,
        fuelType=db_schemaClasses.Vehicle.VehicleFuelType.DIESEL,
        makeAndModel="Test Van",
        isCurrentlyTaxed=False,
        manufacturedDate=datetime.datetime(2019, 1, 1),
        taxExpiryDate=datetime.datetime(2020, 1, 1),
        lastServicedDate=datetime.datetime(2021, 1, 1)
    );

    _filterOptions = db_vehicleFilterOptions.VehicleFilterOptions(
        only_regPlates_containing="TEST",
        only_these_vehicleTypes={db_schemaClasses.Vehicle.VehicleType.CAR},
        only_these_fuelTypes={db_schemaClasses.Vehicle.VehicleFuelType.PETROL},
        only_makesAndModels_containing="Test",
        must_be_currentlyTaxed=True,
        manufacturedDate_between=(datetime.datetime(2019, 1, 1), datetime.datetime(2021, 1, 1)),
        taxExpiryDate_between=(datetime.datetime(2020, 1, 1), datetime.datetime(2022, 1, 1)),
        lastServicedDate_between=(datetime.datetime(2021, 1, 1), datetime.datetime(2023, 1, 1))
    );

    _matchingVehicles = _filterOptions.pluckMatchingVehicles(
        [_testVehicle1, _testVehicle2]
    );

    assert (len(_matchingVehicles) == 1);
    assert (_matchingVehicles[0] == _testVehicle1);