# file:     test_uiLogic.py - unit-tests for the ui_* logic files
# author:   Ben Mullan (2025)

import pytest, tkinter;
from . import (_testUtils);

ui_c_dataGrid               = _testUtils.importLogicFile("ui_c_dataGrid");
ui_c_dataSourceLabel        = _testUtils.importLogicFile("ui_c_dataSourceLabel");
ui_c_dbRecordView           = _testUtils.importLogicFile("ui_c_dbRecordView");
ui_c_editVehicleDialog      = _testUtils.importLogicFile("ui_c_editVehicleDialog");
ui_c_filterVehiclesDialog   = _testUtils.importLogicFile("ui_c_filterVehiclesDialog");
ui_c_floatingToolTip        = _testUtils.importLogicFile("ui_c_floatingToolTip");
ui_c_imageButton            = _testUtils.importLogicFile("ui_c_imageButton");
ui_c_loadingDialog          = _testUtils.importLogicFile("ui_c_loadingDialog");
ui_c_mainWindow             = _testUtils.importLogicFile("ui_c_mainWindow");
ui_c_textboxWithPlaceholder = _testUtils.importLogicFile("ui_c_textboxWithPlaceholder");
ui_uiRenderer               = _testUtils.importLogicFile("ui_uiRenderer");


@pytest.fixture
def dataGridFixture():

    _window = tkinter.Tk()
    _dataGrid = ui_c_dataGrid.DataGrid(_window);
    yield _dataGrid; _window.destroy();


def test_dataGrid_clearAllRecords(dataGridFixture, mocker):

    _mock_recordsData = ["row1", "row2", "row3"];
    mocker.patch.object(dataGridFixture, 'get_children', return_value=_mock_recordsData);
    _mock_delete = mocker.patch.object(dataGridFixture, 'delete');

    dataGridFixture.clearAllRecords();

    # assert that delete was called for each row
    for _row in _mock_recordsData: _mock_delete.assert_any_call(_row);

    # assert that get_children was called exactly once
    dataGridFixture.get_children.assert_called_once();


def test_dbRecordView_currentFilterOptions__nullFilterOptions(mocker):

    _originalPhotoImage = tkinter.PhotoImage;

    def _mock_PhotoImage(*args, **kwargs):

        _1x1PixelData = "R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
        kwargs.pop("file", None);
        kwargs["data"] = _1x1PixelData;

        return _originalPhotoImage(*args, **kwargs);

    _window = tkinter.Tk();
    _dbInteractor = mocker.Mock();
    mocker.patch("tkinter.PhotoImage", _mock_PhotoImage);
    _dbRecordView = ui_c_dbRecordView.DbRecordView(_window, _dbInteractor);

    with pytest.raises(ValueError, match="currentFilterOptions shouldn't be None"):
        _dbRecordView.currentFilterOptions = None;

    _window.destroy();


@pytest.fixture
def editVehicleDialogFixture(mocker):

    _window = tkinter.Tk();
    _editVehicleDialog = ui_c_editVehicleDialog.EditVehicleDialog(_window);
    yield _editVehicleDialog; _window.destroy();


def test_editVehicleDialog_checkThatInputtedValues_areValid(editVehicleDialogFixture, mocker):

    mocker.patch.object(
        editVehicleDialogFixture,
        "_EditVehicleDialog__vehicleWidgets",
        {
            "regPlate"          : mocker.Mock(validate=lambda: True),
            "typeOfVehicle"     : mocker.Mock(validate=lambda: True),
            "fuelType"          : mocker.Mock(validate=lambda: True),
            "makeAndModel"      : mocker.Mock(validate=lambda: True),
            "isCurrentlyTaxed"  : mocker.Mock(validate=lambda: True),
            "manufacturedDate"  : mocker.Mock(validate=lambda: True),
            "taxExpiryDate"     : mocker.Mock(validate=lambda: True),
            "lastServicedDate"  : mocker.Mock(validate=lambda: True)
        }
    );

    (_areValid, _message) = editVehicleDialogFixture._EditVehicleDialog__checkThatInputtedValues_areValid();

    assert (_areValid is True);
    assert (_message == "(all input was valid)");