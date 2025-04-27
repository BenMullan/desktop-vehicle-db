# file:     filterVehiclesDialog.py - dialog for constructing a VehicleFilterOptions
# author:   Ben Mullan (2025)

import enum, datetime, dataclasses, tkinter;
from tkinter import ttk, messagebox;

from . import (
    app_constants, app_filesysUtils,
    db_schemaClasses, db_vehicleFilterOptions,
    ui_c_textboxWithPlaceholder, ui_c_floatingToolTip
);


class FilterVehiclesDialog (tkinter.Toplevel):
    """ui-component: dialog window for building a VehicleFilterOptions"""


    @dataclasses.dataclass(frozen=True)
    class PropertyToWidgetMapping (object):
        """
        represents the input-widget for a filter property,
        + methods for getting, setting, & validating its value.
        """

        widget   :tkinter.Widget;
        getValue :"callable[[], any]";
        setValue :"callable[[any], None]";
        validate :"callable[[], bool]";


    class BooleanCriteriumValues (enum.Enum):
        """
        the enumeration for whether to show vehicles
        based on a boolean criterium, eg what their
        isCurrentlyTaxed status is.
        """
        NO = 0; YES = 1; DOESNT_MATTER = 2;


    __DATETIME_FORMAT_ :str = "%d-%m-%Y";
    """[static] the (de)serialization format for filter datetimes"""

    __DATETIME_FORMAT_DESCRIPTION_ :str = "dd-mm-yyyy";
    """[static] a human-readable description of the above"""

    __dialogIsClosed :tkinter.BooleanVar;
    """signals when the dialog is closed"""

    __filterOptionsOut :db_vehicleFilterOptions.VehicleFilterOptions;
    """the resultant filter-options object constructed the input"""

    __filterWidgetsFrame :ttk.Labelframe;
    """the inner bordered-box housing the filter widgets"""

    __filterWidgets :dict[str, PropertyToWidgetMapping];
    """the input-widgets for the filter options"""


    def __init__(self, _parentWindow :tkinter.Misc, **kwargs) -> None:
        """instanciates the ui-component"""

        super().__init__(master=_parentWindow, **kwargs);
        self.__dialogIsClosed = tkinter.BooleanVar(master=self, value=True);
        self.__configureSelf();


    def __configureSelf(self) -> None:
        """initialises the ui-component's properties and children"""

        self.__centerSelfToParentWindow();

        self.transient(master=self.master);  # stay on top of parent window
        self.attributes("-topmost", True);   # make dialog topmost
        self.grab_set();                     # intercept all window events

        self.geometry("540x460");
        self.resizable(False, False);
        self.bind("<Escape>", lambda _event: self.destroy());
        self.configure(background=app_constants.UI_COLOUR_BACKGROUND_DIALOG);

        self.__addChildWidgets();

        # hide dialog, until showAndGetFilter() called
        # (...at which point, deiconify() and lift())

        self.withdraw();


    def __centerSelfToParentWindow(self) -> None:
        """centers the dialog relative to the parent Toplevel() window"""

        if self.winfo_viewable(): self.update_idletasks(); # enter message-pump temporarily
        _x = self.master.winfo_rootx() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2);
        _y = self.master.winfo_rooty() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2);
        self.geometry(f"+{_x}+{_y}");


    def __addChildWidgets(self) -> None:
        """(dynamically) adds the child widgets to the dialog"""

        self.__filterWidgetsFrame = ttk.Labelframe(master=self, text="Show...", style="vdb.dialog.TLabelframe");
        self.__filterWidgetsFrame.pack(padx=15, pady=(20, 2), fill="both", expand=True);

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # the __filterWidgetsFrame uses an implicitly-defined grid;
        # its #rows and #columns arent defined before widget grid()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        self.__declareFilterWidgets(_widgetsContainer=self.__filterWidgetsFrame);

        # for each declared PropertyToWidgetMapping, render a label
        # displaying its name, and grid() its widget rightwards.

        for _rowIndex, (_propName, _propWidgetMapping) in enumerate(self.__filterWidgets.items()):

            ttk.Label(
                self.__filterWidgetsFrame,
                style="vdb.labelframed.TLabel",
                text=f"{FilterVehiclesDialog.__getUiLabelString_fromFilterOptionName_(_propName)}:"
            ).grid(column=0, row=_rowIndex, padx=(15, 5), pady=3, sticky="w");

            _propWidgetMapping.widget.grid(column=1, row=_rowIndex, padx=5, pady=3, sticky="w");

        _blankDateInfoLabel = ttk.Label(
            master=self,
            style="vdb.dialogsubtle.TLabel",
            text="leave a date blank, to mean \"infinity in the past/future\""
        );

        _blankDateInfoLabel.pack(padx=10, pady=(1, 5));

        # add the [Ok] button below the filter-options' frame
        # this can be clicked using the [Enter] key too

        _okButton = ttk.Button(self, text="Ok", default="active", command=self.__constructFilterOptions_andClose)
        _okButton.pack(padx=10, pady=(15, 10));
        self.bind("<Return>", self.__constructFilterOptions_andClose);
        ui_c_floatingToolTip.FloatingToolTip(_okButton, "leave all fields blank, to apply no filter");


    @staticmethod
    def __getUiLabelString_fromFilterOptionName_(_filterOptionName :str) -> str:
        """[static] eg `regPlate_substring` → `reg-plate substring`"""
        return app_filesysUtils.drinkingCamelCase_toKebabCase(_filterOptionName).replace("_", " ");


    def __declareFilterWidgets(self, _widgetsContainer :tkinter.Widget) -> None:
        """initialises the __filterWidgets member with widgets for the filter-options (textbox for the regPlate_substring, etc)"""


        def _createDateRangeWidget_(_container :tkinter.Widget) -> tuple[ttk.Frame, "callable[[], tuple[datetime.datetime, datetime.datetime]|None]"]:
            """returns a Frame() containg two textboxes (for the start and end of the date-range), and a function to get the date-range itself"""

            _widgetFrame = ttk.Frame(master=_container);
            _startDate_textbox = ui_c_textboxWithPlaceholder.TextboxWithPlaceholder(_widgetFrame, FilterVehiclesDialog.__DATETIME_FORMAT_DESCRIPTION_);
            _endDate_textbox = ui_c_textboxWithPlaceholder.TextboxWithPlaceholder(_widgetFrame, FilterVehiclesDialog.__DATETIME_FORMAT_DESCRIPTION_);

            _startDate_textbox.grid(column=0, row=0, padx=(0, 5));
            _endDate_textbox.grid(column=1, row=0);


            def _getEnteredDateRange() -> tuple[datetime.datetime, datetime.datetime]|None:
                """
                returns infinity-in-the-{past/future} if ONE OF the {start/end} is empty;
                returns None if BOTH OF the {start/end} are empty.
                """

                _startDate_text = _startDate_textbox.get();
                _endDate_text = _endDate_textbox.get();
                if (_startDate_text == "") and (_endDate_text == ""): return None;

                _startDate = (
                    datetime.datetime.min
                    if (_startDate_text == "")
                    else datetime.datetime.strptime(_startDate_text, FilterVehiclesDialog.__DATETIME_FORMAT_)
                );

                _endDate = (
                    datetime.datetime.max
                    if (_endDate_text == "")
                    else datetime.datetime.strptime(_endDate_text, FilterVehiclesDialog.__DATETIME_FORMAT_)
                );

                return (_startDate, _endDate);


            return (_widgetFrame, _getEnteredDateRange);


        def _createMultiSelectWidget_(_container :tkinter.Widget, _listOptions :list[str]) -> tuple[ttk.Frame, tkinter.Listbox]:
            """returns a Frame() and a child Listbox(), containing each option"""

            _frame = ttk.Frame(_container);
            _listbox = tkinter.Listbox(master=_frame, selectmode=tkinter.MULTIPLE, height=4, exportselection=False);

            for _listOption in _listOptions: _listbox.insert(tkinter.END, _listOption);
            _listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True);
            return (_frame, _listbox);


        self.__filterWidgets :dict[str, FilterVehiclesDialog.PropertyToWidgetMapping] = {};

        self.__filterWidgets["only_regPlates_containing"] = FilterVehiclesDialog.PropertyToWidgetMapping(
            widget   = ui_c_textboxWithPlaceholder.TextboxWithPlaceholder(_widgetsContainer, "eg YMZ"),
            getValue = lambda : self.__filterWidgets["only_regPlates_containing"].widget.get() or None,
            setValue = lambda _newValue : self.__filterWidgets["only_regPlates_containing"].widget.insert(0, _newValue),
            validate = lambda : True
        );

        (_vTypesFrame, _vTypesListbox) = _createMultiSelectWidget_(_widgetsContainer, [_e.name.lower() for _e in db_schemaClasses.Vehicle.VehicleType]);
        self.__filterWidgets["only_these_vehicleTypes"] = FilterVehiclesDialog.PropertyToWidgetMapping(
            widget   = _vTypesFrame,
            getValue = lambda : (
                {db_schemaClasses.Vehicle.VehicleType[_item.upper()] for _item in FilterVehiclesDialog.__getListboxsSelectedValues_(_vTypesListbox)}
                if (len(FilterVehiclesDialog.__getListboxsSelectedValues_(_vTypesListbox)) > 0)
                else None
            ),
            setValue = lambda _newValues : None,
            validate = lambda : True
        );

        (_fuelTypesFrame, _fuelTypesListbox) = _createMultiSelectWidget_(_widgetsContainer, [_e.name.lower() for _e in db_schemaClasses.Vehicle.VehicleFuelType]);
        self.__filterWidgets["only_these_fuelTypes"] = FilterVehiclesDialog.PropertyToWidgetMapping(
            widget   = _fuelTypesFrame,
            getValue = lambda : (
                {db_schemaClasses.Vehicle.VehicleFuelType[_item.upper()] for _item in FilterVehiclesDialog.__getListboxsSelectedValues_(_fuelTypesListbox)}
                if (len(FilterVehiclesDialog.__getListboxsSelectedValues_(_fuelTypesListbox)) > 0)
                else None
            ),
            setValue = lambda _newValues : None,
            validate = lambda : True
        );

        self.__filterWidgets["only_makesAndModels_containing"] = FilterVehiclesDialog.PropertyToWidgetMapping(
            widget   = ui_c_textboxWithPlaceholder.TextboxWithPlaceholder(_widgetsContainer, "eg FORD"),
            getValue = lambda : self.__filterWidgets["only_makesAndModels_containing"].widget.get() or None,
            setValue = lambda _newValue : self.__filterWidgets["only_makesAndModels_containing"].widget.insert(0, _newValue),
            validate = lambda : True
        );

        self.__filterWidgets["must_be_currentlyTaxed"] = FilterVehiclesDialog.PropertyToWidgetMapping(
            widget   = ttk.Combobox(_widgetsContainer, state="readonly", values=[_e.name.lower() for _e in FilterVehiclesDialog.BooleanCriteriumValues]),
            getValue = lambda : (
                None
                if (
                    FilterVehiclesDialog.BooleanCriteriumValues[self.__filterWidgets["must_be_currentlyTaxed"].widget.get().upper()]
                    ==
                    FilterVehiclesDialog.BooleanCriteriumValues.DOESNT_MATTER
                ) else (
                    FilterVehiclesDialog.BooleanCriteriumValues[self.__filterWidgets["must_be_currentlyTaxed"].widget.get().upper()]
                    ==
                    FilterVehiclesDialog.BooleanCriteriumValues.YES
                )
            ),
            setValue = lambda _newValue : self.__filterWidgets["must_be_currentlyTaxed"].widget.set(
                FilterVehiclesDialog.BooleanCriteriumValues.YES.name.lower()
                if _newValue
                else (
                    FilterVehiclesDialog.BooleanCriteriumValues.NO.name.lower()
                    if (not _newValue)
                    else FilterVehiclesDialog.BooleanCriteriumValues.DOESNT_MATTER.name.lower()
                )
            ),
            validate = lambda : (
                self.__filterWidgets["must_be_currentlyTaxed"].widget.get().lower()
                in [_e.name.lower() for _e in FilterVehiclesDialog.BooleanCriteriumValues]
            )
        );

        # pre-set the [must be currently-taxed] checkbox to the last-available value in the enum; doesnt_matter
        self.__filterWidgets["must_be_currentlyTaxed"].widget.current(newindex=len(FilterVehiclesDialog.BooleanCriteriumValues) - 1);

        (_manDatesWidget, _getManDatesRange) = _createDateRangeWidget_(_widgetsContainer);
        self.__filterWidgets["manufacturedDate_between"] = FilterVehiclesDialog.PropertyToWidgetMapping(
            widget   = _manDatesWidget,
            getValue = _getManDatesRange,
            setValue = lambda _newValue : None,
            validate = lambda : True if FilterVehiclesDialog.__bothDateRangeTextboxes_areEmpty_(_manDatesWidget) else (_getManDatesRange() is not None)
        );

        (_taxDatesWidget, _getTaxDatesRange) = _createDateRangeWidget_(_widgetsContainer);
        self.__filterWidgets["taxExpiryDate_between"] = FilterVehiclesDialog.PropertyToWidgetMapping(
            widget   = _taxDatesWidget,
            getValue = _getTaxDatesRange,
            setValue = lambda _newValue : None,
            validate = lambda : True if FilterVehiclesDialog.__bothDateRangeTextboxes_areEmpty_(_taxDatesWidget) else (_getTaxDatesRange() is not None)
        );

        (_svcDatesWidget, _getSvcDatesRange) = _createDateRangeWidget_(_widgetsContainer);
        self.__filterWidgets["lastServicedDate_between"] = FilterVehiclesDialog.PropertyToWidgetMapping(
            widget   = _svcDatesWidget,
            getValue = _getSvcDatesRange,
            setValue = lambda _newValue : None,
            validate = lambda : True if FilterVehiclesDialog.__bothDateRangeTextboxes_areEmpty_(_svcDatesWidget) else (_getSvcDatesRange() is not None)
        );


    @staticmethod
    def __getListboxsSelectedValues_(_listbox :tkinter.Listbox) -> list[str]:
        """retrieves the have-been-selected values, from the _listbox widget"""
        return [_listbox.get(_item) for _item in _listbox.curselection()];


    @staticmethod
    def __bothDateRangeTextboxes_areEmpty_(_dateRangeFrame :ttk.Frame) -> bool:
        """determines if both entries in the date-range widget are empty"""

        _childWidgets :list[tkinter.Widget] = _dateRangeFrame.winfo_children();
        if len(_childWidgets) < 2: raise Exception("the _dateRangeFrame didn't contain two child-widgets");
        return (_childWidgets[0].get() == "") and (_childWidgets[1].get() == "");


    def __showSelf(self, _dialogTitle :str) -> None:
        """disables the parent window, and shows this dialog"""

        self.title(_dialogTitle);

        # prevent interaction with the parent window
        # self.master.protocol("WM_DELETE_WINDOW", lambda : None);

        # show thyself
        self.deiconify(); self.lift(); self.focus_set();
        self.__centerSelfToParentWindow();
        if not self.winfo_viewable(): raise Exception("the edit-vehicle dialog failed to become visible");


    def showAndGetFilterOptions(self) -> db_vehicleFilterOptions.VehicleFilterOptions:
        """
        shows the filter dialog, allowing the user to input filter options,
        then returns the resultant VehicleFilterOptions on dialog closure;
        """

        self.__showSelf(_dialogTitle="Filter...");
        self.__dialogIsClosed.set(value=False);

        self.wait_variable(self.__dialogIsClosed);
        return self.__filterOptionsOut;


    def __constructFilterOptions_andClose(self, _event=None) -> None:
        """parses the input-fields to instanciate a VehicleFilterOptions(), then closes the dialog"""

        _valuesAreValid :bool; _whatsWrongMsg :str;
        (_valuesAreValid, _whatsWrongMsg) = self.__checkThatInputtedValues_areValid();

        if not _valuesAreValid:
            messagebox.showwarning("Sorry darling...", _whatsWrongMsg, parent=self);
            return;

        # some getValue() calls may return None; that filter-option simply won't have an effect
        self.__filterOptionsOut = db_vehicleFilterOptions.VehicleFilterOptions(
            ** { _propName : _propWidgetMapping.getValue() for _propName, _propWidgetMapping in self.__filterWidgets.items() }
        );

        self.__closeDialog();


    def __checkThatInputtedValues_areValid(self) -> tuple[bool, str]:
        """returns [whether the input-fields' values are valid] and [if not, why]"""

        for _fieldName, _fieldWidgetMapping in self.__filterWidgets.items():

            try:
                if not _fieldWidgetMapping.validate():
                    return (
                        False,
                        f"""That {
                            FilterVehiclesDialog.__getUiLabelString_fromFilterOptionName_(_fieldName)
                        } ({_fieldWidgetMapping.getValue() or "empty"}) isn't valid."""
                    );

            except Exception as _e:
                messagebox.showwarning(
                    title=f"{FilterVehiclesDialog.__getUiLabelString_fromFilterOptionName_(_fieldName)}'s a bit funny...",
                    message=f"\"{FilterVehiclesDialog.__getUiLabelString_fromFilterOptionName_(_fieldName)}\" seems invalid because {str(_e)}",
                    parent=self
                );

        return (True, "(all input was valid)");


    def __closeDialog(self) -> None:
        """closes the currently-open filter dialog"""

        if not self.winfo_viewable(): raise RuntimeError("cannot __closeDialog() because the dialog isn't currently shown");

        # re-enable the parent-window's [x] button, & close self
        # self.master.protocol("WM_DELETE_WINDOW", self.master.destroy);

        self.__dialogIsClosed.set(value=True);
        self.destroy();