# file:     dbRecordView.py - CRUD row-by-row editor (table) ui component
# author:   Ben Mullan (2025)

import tkinter; from tkinter import ttk;

from . import (
    app_constants, app_filesysUtils,
    db_dbInteractor, db_schemaClasses, db_vehicleFilterOptions,
    ui_c_dataGrid, ui_c_floatingToolTip, ui_c_imageButton, ui_c_dataSourceLabel
);


class DbRecordView (ttk.Frame):
    """
    ui-component: CRUD row-by-row editor (principally a table)

    *which* database file this component reads from,
    is goverened by the `targetDatabase` property of
    the DatabaseInteractor singleton.
    """


    __dbInteractor :db_dbInteractor.DatabaseInteractor;
    """the DatabaseInteractor whence to read/write to the database"""

    __dataGrid :ui_c_dataGrid.DataGrid;
    """the tabular grid of data-cells showing database records"""

    __editVehicleCallback :"callable[str]";
    """a function taking in a regPlate, to UPDATE a vehicle"""

    __deleteVehicleCallback :"callable[str]";
    """a function taking in a regPlate, to DELETE a vehicle"""

    __filterVehiclesCallback :"callable";
    """a ui-wireup function to get and apply filter-options"""

    __currentFilterOptions :db_vehicleFilterOptions.VehicleFilterOptions;
    """the current filter options for displaying vehicle records"""

    __filterDescriptionLabel_text = tkinter.StringVar;
    """shows the current filter-options in blue"""

    __dataSourceLabel :ui_c_dataSourceLabel.DataSourceLabel;
    """[pointer-to] the label saying [showing * vehicles from {database-file}]"""

    __contextMenu :tkinter.Menu;
    """the right-click menu for rows"""

    __deleteIcon16 :tkinter.PhotoImage;
    """[x] delete icon for context-menu"""

    __editIcon16 :tkinter.PhotoImage;
    """[/] edit icon for context-menu"""


    @property
    def currentFilterOptions(self) -> db_vehicleFilterOptions.VehicleFilterOptions:
        """returns the current filter-options"""
        return self.__currentFilterOptions;

    @currentFilterOptions.setter
    def currentFilterOptions(self, _newFilterOptions :db_vehicleFilterOptions.VehicleFilterOptions) -> None:
        """sets the current filter options, updating the filter-description label"""

        if (_newFilterOptions is None): raise ValueError("currentFilterOptions shouldn't be None");

        self.__filterDescriptionLabel_text.set(f"{_newFilterOptions.numberOfNonNullFilterOptions} filter(s) applied");
        self.__currentFilterOptions = _newFilterOptions;


    def __init__(self, _parentComponent :tkinter.Widget, _dbInteractor :db_dbInteractor.DatabaseInteractor, **kwargs) -> None:
        """instanciates the ui-component"""

        super().__init__(master=_parentComponent, **kwargs);

        self.__editVehicleCallback = None;
        self.__deleteVehicleCallback = None;
        self.__filterVehiclesCallback = None;
        self.__dataSourceLabel = None;

        self.__filterDescriptionLabel_text = tkinter.StringVar(master=self, value="$$__uninitialised__$$");
        self.currentFilterOptions = db_vehicleFilterOptions.VehicleFilterOptions.getEmpty_();

        self.__dbInteractor = _dbInteractor;
        self.__configureSelf();


    def __configureSelf(self) -> None:
        """initialises the ui-component's properties and children"""

        self.configure(style="vdb.normal.TFrame");

        self.__addChildWidgets();
        self.__configureContextMenu();


    def __addChildWidgets(self) -> None:
        """adds the child-widgets to the Frame"""

        #   top three components in a sub-frame, like...
        #
        # ╔═══════════════════════════╦═══════════════╦═══════════════╗
        # ║ info-label                ║ filters-label ║ filter-button ║
        # ╠═══════════════════════════╩═══════════════╩═══════════════╣
        # ║                                                           ║
        # ║                                                           ║
        # ║                   (table of records...)                   ║
        # ║                                                           ║
        # ║                                                           ║
        # ║                                                           ║
        # ╚═══════════════════════════════════════════════════════════╝

        _frameAboveTable = ttk.Frame(master=self, style="vdb.normal.TFrame");

        _rightClickInfoLabel = ttk.Label(
            master=_frameAboveTable,
            style="vdb.subtle.TLabel",
            text="right-click, or press [Enter] on a row, to edit/delete..."
        );

        _rightClickInfoLabel.grid(column=0, row=0, sticky="nw", padx=(0, 10), pady=2);

        _filterDescriptionLabel = ttk.Label(
            master=_frameAboveTable,
            style="vdb.accented.TLabel",
            textvariable=self.__filterDescriptionLabel_text
        );

        _filterDescriptionLabel.grid(column=1, row=0, sticky="ne", padx=(2, 10), pady=2);

        _filterButton = ui_c_imageButton.ImageButton(
            _parentComponent=_frameAboveTable,
            _text="filter...",
            _iconFilepath=app_filesysUtils.resolvePath_relativeToMainPy(f"{app_constants.UI_ASSETS_FOLDER}/icon-filter-16.png"),
            _command=lambda _event : self.__filterShownVehicles()
        );

        _filterButton.grid(column=2, row=0, sticky="ne", padx=(5, 0), pady=2);

        ui_c_floatingToolTip.FloatingToolTip(
            _targetWidget=_filterButton,
            _toolTipText="narrow-down which vehicles are shown... (Alt + F)"
        );

        self.bind_all("<Alt-f>", lambda _event : self.__filterShownVehicles());

        _frameAboveTable.grid_columnconfigure(0, weight=1);
        _frameAboveTable.grid_columnconfigure(1, weight=0);
        _frameAboveTable.grid_columnconfigure(2, weight=0);

        _frameAboveTable.pack(fill="x", padx=0, pady=2);

        # package the DataGrid in a Frame too,
        # with a neighbouring vertical scrollbar

        _frameForDataGrid = ttk.Frame(master=self, style="vdb.normal.TFrame");

        self.__dataGrid = ui_c_dataGrid.DataGrid(_parentComponent=_frameForDataGrid);

        _scrollbar = ttk.Scrollbar(master=_frameForDataGrid, orient=tkinter.VERTICAL, command=self.__dataGrid.yview);
        _scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y, padx=0, pady=0);

        self.__dataGrid.pack(side=tkinter.LEFT, expand=True, fill="both", padx=0, pady=0);
        self.__dataGrid.configure(yscrollcommand=_scrollbar.set);

        _frameForDataGrid.pack(expand=True, fill="both", padx=0, pady=2);


    def __configureContextMenu(self) -> None:
        """binds the right-click/[Enter] menu to each row"""

        self.__contextMenu = tkinter.Menu(master=self.__dataGrid, tearoff=False);

        self.__editIcon16 = tkinter.PhotoImage(
            master=self.__dataGrid,
            file=app_filesysUtils.resolvePath_relativeToMainPy(f"{app_constants.UI_ASSETS_FOLDER}/icon-edit-16.png")
        );

        self.__deleteIcon16 = tkinter.PhotoImage(
            master=self.__dataGrid,
            file=app_filesysUtils.resolvePath_relativeToMainPy(f"{app_constants.UI_ASSETS_FOLDER}/icon-delete-16.png")
        );

        self.__contextMenu.add_command(
            label    = "edit...",
            compound = tkinter.LEFT,
            image    = self.__editIcon16,
            command  = self.__editSelectedVehicle
        );

        self.__contextMenu.add_command(
            label    = "delete!",
            compound = tkinter.LEFT,
            image    = self.__deleteIcon16,
            command  = self.__deteleSelectedVehicle
        );

        [
            self.__dataGrid.bind(_trigger, self.__showContextMenu) for _trigger in [
                "<Button-3>", "<Double-1>", "<Return>", "<Delete>", "<space>", "<App>"
            ]
        ];


    def __showContextMenu(self, _event=None) -> None:
        """shows the right-click menu, for the currently-selected row"""

        _selectedRow :str = None;

        if (_event is not None) and (_event.type == tkinter.EventType.ButtonPress):

            # the context-menu has been triggered by a mouse-click
            _selectedRow = self.__dataGrid.identify_row(y=_event.y);
            if (_selectedRow is None): return;
            self.__dataGrid.selection_set(_selectedRow);

        else:

            # the context-menu has been triggered by a key-press
            _selectedRows :tuple[str, ...] = self.__dataGrid.selection();
            if len(_selectedRows) == 0: return;
            _selectedRow = _selectedRows[0];

        _boundryBox = self.__dataGrid.bbox(item=_selectedRow);
        if len(_boundryBox) == 0: return;
        _x, _y, _width, _height = _boundryBox;
        self.__contextMenu.post(self.__dataGrid.winfo_rootx() + _x + 25, self.__dataGrid.winfo_rooty() + _y + _height - 10);


    def __getSelectedRow_regPlate(self) -> str:
        """returns the regPlate of the selected row"""

        _selectedRows :tuple[str, ...] = self.__dataGrid.selection();
        if len(_selectedRows) == 0: return;

        _regPlateColumnIndex :int = list(self.__dbInteractor.getVehicleTableColumns().keys()).index("regPlate");
        _regPlate :str = self.__dataGrid.item(_selectedRows[0], "values")[_regPlateColumnIndex];

        return _regPlate;


    #region ui-task-callbacks

    def __editSelectedVehicle(self) -> None:
        """invokes __editVehicleCallback() with the selected vehicle's regPlate"""
        if (self.__editVehicleCallback is None): raise ValueError("__editVehicleCallback is null");
        self.__editVehicleCallback(self.__getSelectedRow_regPlate());


    def __deteleSelectedVehicle(self) -> None:
        """invokes __deleteVehicleCallback() with the selected vehicle's regPlate"""
        if (self.__deleteVehicleCallback is None): raise ValueError("__deleteVehicleCallback is null");
        self.__deleteVehicleCallback(self.__getSelectedRow_regPlate());


    def __filterShownVehicles(self) -> None:
        """invokes the __filterVehiclesCallback"""
        if (self.__filterVehiclesCallback is None): raise ValueError("__filterVehiclesCallback is null");
        self.__filterVehiclesCallback();


    def setEditVehicleCallback(self, _callback :"callable[str]") -> None:
        """sets __editVehicleCallback to a function taking in a regPlate"""
        self.__editVehicleCallback = _callback;


    def setDeleteVehicleCallback(self, _callback :"callable[str]") -> None:
        """sets __deleteVehicleCallback to a function taking in a regPlate"""
        self.__deleteVehicleCallback = _callback;


    def setFilterVehiclesCallback(self, _callback :"callable") -> None:
        """sets __filterVehiclesCallback to a function taking no arguments"""
        self.__filterVehiclesCallback = _callback;

    #endregion


    def setDataSourceLabelPointer(self, _dataSourceLabel :ui_c_dataSourceLabel.DataSourceLabel) -> None:
        """sets the __dataSourceLabel pointer to the given DataSourceLabel"""
        self.__dataSourceLabel = _dataSourceLabel;


    def loadVehicleColumns_fromDatabase(self) -> None:
        """
        queries the database for the vehicle-table's columns, & creates
        a DataGrid column for each property in the getVehicleTableColumns() result
        """

        _columns_namesAndTypes :dict[str, str] = self.__dbInteractor.getVehicleTableColumns();
        self.__dataGrid.configure(columns=tuple(_columns_namesAndTypes.keys()));

        # make each column as wide as [the width of
        # the table, divided by the number of columns]

        _widthOfEachColumn :int = (
            (self.__dataGrid.winfo_width() // len(_columns_namesAndTypes))
            if (len(_columns_namesAndTypes) > 0)
            else 10
        );

        for _colName, _colType in _columns_namesAndTypes.items():

            self.__dataGrid.heading(
                column=_colName,
                anchor=tkinter.W,
                text=app_filesysUtils.drinkingCamelCase_toKebabCase(_colName)
            );

            self.__dataGrid.column(
                column=_colName,
                stretch=True,
                width=_widthOfEachColumn
            );

        # letztendlich, make the first column (regPlate) not-squished
        self.__dataGrid.column(
            column=self.__dataGrid.cget("columns")[0],
            width=int(_widthOfEachColumn * 1)
        );


    def loadVehicleRecords_matchingFilter(self) -> None:
        """
        populates the table with vehicle records satisfying
        the `currentFilterOptions`, and updates the __dataSourceLabel
        """

        self.__dataGrid.clearAllRecords();

        _allVehicles :list[db_schemaClasses.Vehicle] = self.__dbInteractor.getAllVehicles();
        _vehiclesMatchingFilter = self.currentFilterOptions.pluckMatchingVehicles(_allVehicles);

        for _vehicle in _vehiclesMatchingFilter:
            self.__dataGrid.insert(parent="", index="end", values=_vehicle.toDisplayTuple());

        if (self.__dataSourceLabel is None): raise ValueError("__dataSourceLabel hasn't been initialised");

        self.__dataSourceLabel.setText(
            _numVehiclesShown   = len(_vehiclesMatchingFilter),
            _dbName             = self.__dbInteractor.targetDatabase
        );