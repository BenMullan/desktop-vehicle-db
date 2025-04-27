# file:     mainWindow.py - main-window ui component
# author:   Ben Mullan (2025)

import time, random, tkinter, threading;
from tkinter import ttk, messagebox;

from . import (
    app_configProvider, app_constants, app_filesysUtils, app_errorHandling,
    db_dbInteractor, db_dbFileManager, db_schemaClasses, db_vehicleFilterOptions,
    ui_c_dataSourceLabel, ui_c_imageButton, ui_c_dbRecordView, ui_c_floatingToolTip,
    ui_c_loadingDialog, ui_c_filterVehiclesDialog, ui_c_editVehicleDialog
);


class MainWindow (tkinter.Tk):
    """ui-component: main window"""


    __dbRecordView :ui_c_dbRecordView.DbRecordView;
    """the data-grid and associated controls for CRUD-ing vehicles"""


    def __init__(self, **kwargs) -> None:
        """instanciates the ui-component"""

        super().__init__(**kwargs);
        self.__configureSelf();

        # schedule loading-the-vehicles to run,
        # once the mainloop() message-pump starts...
        self.after(0, self.__task_loadAllVehicleRecords);


    @staticmethod
    def __getDbConfig_() -> dict[str, str]:
        """[static] returns the [database] section of config.ini"""
        return app_configProvider.getGlobalConfig()["database"];

    @staticmethod
    def __getUiConfig_() -> dict[str, str]:
        """[static] returns the [userInterface] section of config.ini"""
        return app_configProvider.getGlobalConfig()["userInterface"];


    def __configureSelf(self) -> None:
        """initialises the ui-component's properties and children"""

        # catch the database-file missing here, before this would be caught
        # by the getInstance() construction of the DatabaseInteractor for
        # DbRecordView (which would show a rather more cryptic error-message).

        self.__ensureDefaultDatabaseExists();

        self.minsize(400, 300);
        self.resizable(True, True);
        self.geometry(self.__getGeometry());

        self.__configureGrid();

        self.configure(background=app_constants.UI_COLOUR_BACKGROUND_MAIN);
        self.title(app_constants.UI_MAIN_WINDOW_TITLE);

        _windowIcon :tkinter.PhotoImage = tkinter.PhotoImage(
            master=self,
            file=app_filesysUtils.resolvePath_relativeToMainPy(
                f"{app_constants.UI_ASSETS_FOLDER}/vehicle.png"
            )
        );

        self.iconphoto(True, _windowIcon);

        self.__addChildWidgets();


    def __configureGrid(self) -> None:
        """declares the #columns and #rows"""

        _columnWeights = {0:100};
        _rowWeights = {0:1, 1:98, 2:1};

        [self.grid_columnconfigure(index=_i, weight=_w) for _i, _w in _columnWeights.items()];
        [self.grid_rowconfigure(index=_i, weight=_w) for _i, _w in _rowWeights.items()];

        if (MainWindow.__getUiConfig_()["showDebuggingBorders"].lower() == "true"):

            # render grid cells with borders and
            # coordinates; helpful for debugging

            for _iRow in range(len(_rowWeights)):
                for _iColumn in range(len(_columnWeights)):

                    _gridCellLabel = ttk.Label(master=self, text=f"{_iColumn},{_iRow}", borderwidth=1, relief="solid");
                    _gridCellLabel.grid(row=_iRow, column=_iColumn, padx=3, pady=3, sticky="nsew");


    def __getGeometry(self) -> str:
        """returns a tkinter-geometry-string, centering the window"""

        # offset the window, to make tkinter warning
        # messageboxes not obscured by the mainWindow
        _WINDOW_OFFSET_X = -250; _WINDOW_OFFSET_Y = +100;

        _windowWidth, _windowHeight = MainWindow.__getUiConfig_()["mainWindowSize"].split("x");
        _topLeftX = (self.winfo_screenwidth() - int(_windowWidth)) // 2;
        _topLeftY = (self.winfo_screenheight() - int(_windowHeight)) // 2;

        return f"{_windowWidth}x{_windowHeight}+{_topLeftX + _WINDOW_OFFSET_X}+{_topLeftY + _WINDOW_OFFSET_Y}";


    def __addChildWidgets(self) -> None:
        """adds the child-widgets to the main window"""

        _dataSourceLabel = ui_c_dataSourceLabel.DataSourceLabel(_parentComponent=self);
        _dataSourceLabel.grid(column=0, row=0, sticky="nw", padx=20, pady=(20, 25));

        self.bind_all("<Alt-a>", lambda _event : self.__task_addNewVehicle());

        self.__dbRecordView = ui_c_dbRecordView.DbRecordView(
            _parentComponent = self,
            _dbInteractor    = db_dbInteractor.DatabaseInteractor.getInstance()
        );

        self.__dbRecordView.setDataSourceLabelPointer(_dataSourceLabel);
        self.__dbRecordView.setEditVehicleCallback(self.__task_editVehicle);
        self.__dbRecordView.setDeleteVehicleCallback(self.__task_deleteVehicle);
        self.__dbRecordView.setFilterVehiclesCallback(self.__task_filterVehicles);

        self.__dbRecordView.grid(column=0, row=1, sticky="nesw", padx=20, pady=(0, 5));

        _addVehicleButton = ui_c_imageButton.ImageButton(
            _parentComponent = self,
            _text            = "add",
            _iconFilepath    = app_filesysUtils.resolvePath_relativeToMainPy(f"{app_constants.UI_ASSETS_FOLDER}/icon-add-16.png"),
            _command         = lambda _event : self.__task_addNewVehicle()
        );

        _addVehicleButton.grid(
            column=0, row=2, sticky="nw", padx=20, pady=(5, 25)
        );

        ui_c_floatingToolTip.FloatingToolTip(
            _targetWidget=_addVehicleButton,
            _toolTipText="create a new vehicle... (Alt + A)"
        );


    def report_callback_exception(self, _excType :type, _excValue :Exception, _traceback :any) -> None:
        """overrides the default exception-hook, to show a messagebox"""

        _errorMsg :str = f"There's been a tkinter {_excType.__name__}.\n\n{_excValue}";

        if app_constants.DEBUG_DONT_CATCH_EXCEPTIONS: raise Exception(_errorMsg);
        app_errorHandling.showWarningMessage_butDontExit(_message=_errorMsg, _existingRootWindow=self);


    def __ensureDefaultDatabaseExists(self) -> None:
        """calls showErrorMessageBox_andExit() (to terminate the programme) if the defaultDatabase existeth not"""

        _defaultDatabase :str = MainWindow.__getDbConfig_()["defaultDatabase"];

        if not db_dbFileManager.DatabaseFileManager.vehiclesDatabaseExists_andIsValid_(_defaultDatabase):

            _errorMsg :str = (
                "The defaultDatabase, "
                + _defaultDatabase
                + " (as specified in config.ini) doesn't seem to exist!"
                + "\n\nThe full expected file-path was "
                + db_dbFileManager.DatabaseFileManager.getFullDbPath_fromDbName_(_defaultDatabase)
            );

            if app_constants.DEBUG_DONT_CATCH_EXCEPTIONS: raise FileNotFoundError(_errorMsg);
            app_errorHandling.showErrorMessage_andExit(_message=_errorMsg, _existingRootWindow=self);


    def __executeTasks_withLoadingDialog(self, _tasks :list[tuple[callable, str]]) -> None:
        """
        shows a LoadingDialog() with the task-description, executes the task function,
        then calls dismissDialog(), then moves to the next task.

        example call:
            __executeTasks_withLoadingDialog(
                [
                    (self.__dbRecordView.loadTableColumns_fromDatabase, "loading table columns"),
                    (self.__dbRecordView.loadAllVehicleRecords, "loading all vehicles")
                ]
            );
        """

        def _execUiTask_thenNextOne(_index: int) -> None:

            if _index >= len(_tasks): return;
            _task, _taskDescription = _tasks[_index];

            _loadingDialog = ui_c_loadingDialog.LoadingDialog(
                _parentWindow=self,
                _taskDescription=f"{_taskDescription}..."
            );

            _loadingDialog.showDialog();

            def _runBackgroundUiTask():
                try:
                    time.sleep(0.6 + random.uniform(-0.5, 0.5));
                    _task();
                except Exception as _e:
                    _errorMsg :str = f"Somat went wrong whilst {_taskDescription}.\n\n({str(_e)})";
                    if app_constants.DEBUG_DONT_CATCH_EXCEPTIONS: raise Exception(_errorMsg) from _e;
                    self.after(0, lambda : messagebox.showwarning("Oh dear...", _errorMsg, parent=self));
                finally:
                    if (_loadingDialog is not None): self.after(0, _loadingDialog.dismissDialog);
                    self.after(0, lambda: _execUiTask_thenNextOne(_index + 1));

            threading.Thread(target=_runBackgroundUiTask).start();

        _execUiTask_thenNextOne(0);


    #region ui-tasks

    def __task_loadAllVehicleRecords(self) -> None:
        """
        [ui-task] (post-initialisation action) loads all vehicle records from the db,
        by re-setting the filter-options. Ensures the defaultDatabase existeth in /data/.
        """

        self.__ensureDefaultDatabaseExists();
        self.__dbRecordView.currentFilterOptions = db_vehicleFilterOptions.VehicleFilterOptions.getEmpty_();

        self.__executeTasks_withLoadingDialog(
            [
                (self.__dbRecordView.loadVehicleColumns_fromDatabase, "configuring table columns"),
                (self.__dbRecordView.loadVehicleRecords_matchingFilter, "fetching all vehicles")
            ]
        );


    def __task_addNewVehicle(self) -> None:
        """[ui-task] inputs a new vehicle, and CREATEs it in the database"""

        _editVehicleDialog :ui_c_editVehicleDialog.EditVehicleDialog = ui_c_editVehicleDialog.EditVehicleDialog(self);
        _inputtedVehicle :db_schemaClasses.Vehicle = _editVehicleDialog.showAndEditVehicle(db_schemaClasses.Vehicle.getEmptyVehicle_());

        def _addInputtedVehicle_toDatabase_():
            db_dbInteractor.DatabaseInteractor.getInstance().addVehicle(_inputtedVehicle);

        self.__executeTasks_withLoadingDialog(
            [
                (_addInputtedVehicle_toDatabase_, "writing vehicle to database"),
                (self.__dbRecordView.loadVehicleRecords_matchingFilter, "refreshing vehicle records")
            ]
        );

        # for debugging; show the edited-vehicle...
        # messagebox.showinfo("_inputtedVehicle", _inputtedVehicle.serialiseToDict(), parent=self);


    def __task_editVehicle(self, _regPlate :str) -> None:
        """[ui-task] SELECTs, allows user editing of, then UPDATEs, a vehicle in the database"""

        _vehicle_readyToBeEdited  :db_schemaClasses.Vehicle = None;
        _vehicle_withEditsApplied :db_schemaClasses.Vehicle = None;

        def _fetchVehicleFromDb():
            nonlocal _vehicle_readyToBeEdited;
            _vehicle_readyToBeEdited = db_dbInteractor.DatabaseInteractor.getInstance().getVehicle_byRegPlate(_regPlate);

        def _editVehicleWithDialog():
            nonlocal _vehicle_withEditsApplied;
            _editVehicleDialog = ui_c_editVehicleDialog.EditVehicleDialog(self);
            _vehicle_withEditsApplied = _editVehicleDialog.showAndEditVehicle(_vehicle_readyToBeEdited, _preventEditingRegPlate=True);

        def _writeVehicleBackToDb():
            db_dbInteractor.DatabaseInteractor.getInstance().updateVehicle_byRegPlate(_regPlate, _vehicle_withEditsApplied);

        self.__executeTasks_withLoadingDialog(
            [
                (_fetchVehicleFromDb, "fetching vehicle record"),
                (_editVehicleWithDialog, "waiting for edited-vehicle"),
                (_writeVehicleBackToDb, "updating vehicle record"),
                (self.__dbRecordView.loadVehicleRecords_matchingFilter, "refreshing vehicle records")
            ]
        );


    def __task_deleteVehicle(self, _regPlate :str) -> None:
        """[ui-task] confirms, then DELETEs a vehicle from the database"""

        _deletionHasBeenConfirmed :bool = messagebox.askyesno(
            "Sure...?",
            f"Delete {_regPlate}... forever?",
            icon=messagebox.WARNING,
            parent=self
        );

        if not _deletionHasBeenConfirmed: return;

        def _deleteVehicleFromDb():
            db_dbInteractor.DatabaseInteractor.getInstance().deleteVehicle_byRegPlate(_regPlate);

        self.__executeTasks_withLoadingDialog(
            [
                (_deleteVehicleFromDb, "deleting vehicle from database"),
                (self.__dbRecordView.loadVehicleRecords_matchingFilter, "refreshing vehicle records")
            ]
        );


    def __task_filterVehicles(self) -> None:
        """
        [ui-task] re-fetches all vehicles from the db, then uses
        a FilterVehiclesDialog() to construct a VehicleFilterOptions(),
        which is used to determine which of the fetched vehicles should
        be shown in the __dbRecordView.
        """

        _filterVehiclesDialog = ui_c_filterVehiclesDialog.FilterVehiclesDialog(self);
        self.__dbRecordView.currentFilterOptions = _filterVehiclesDialog.showAndGetFilterOptions();

        self.__executeTasks_withLoadingDialog(
            [
                (self.__dbRecordView.loadVehicleRecords_matchingFilter, "loading matching vehicles")
            ]
        );

    #endregion