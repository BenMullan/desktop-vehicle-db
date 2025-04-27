# file:     editVehicleDialog.py - form with vehicle fields (non-simpledialog.Dialog-derived) ui component
# author:   Ben Mullan (2025)

import re, tkinter, datetime, dataclasses; from tkinter import ttk, messagebox;
from . import (db_schemaClasses, app_constants, app_filesysUtils, ui_c_textboxWithPlaceholder);


class EditVehicleDialog (tkinter.Toplevel):
    """ui-component: vehicle-editing form window"""


    @dataclasses.dataclass(frozen=True)
    class PropertyToWidgetMapping (object):
        """
        represents the input-widget for a vehicle property
        (eg a textbox for regPlate, etc)
        """

        widget   :tkinter.Widget;
        getValue :"callable[[], any]";
        setValue :"callable[[any], None]";
        validate :"callable[[], bool]";


    __DATETIME_FORMAT_ :str = "%d-%m-%Y";
    """[static] the (de)serialisation format for vehicle datetimes"""

    __DATETIME_FORMAT_DESCRIPTION_ :str = "dd-mm-yyyy";
    """[static] a human-readable description of the above"""

    __dialogIsClosed :tkinter.BooleanVar;
    """signals when the dialog is closed"""

    __vehicleOut :db_schemaClasses.Vehicle;
    """the resultant output vehicle object"""

    __vehicleWidgetsFrame :ttk.Labelframe;
    """the inner bordered-box housing the vehicle widgets"""

    __vehicleWidgets :dict[str, PropertyToWidgetMapping];
    """the input-widgets for the vehcile properties (regPlate, etc)"""


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
        self.grab_set();                     # intercept all window-events

        self.geometry("370x330");
        self.resizable(False, False);
        self.bind("<Escape>", lambda _event: self.destroy());
        self.configure(background=app_constants.UI_COLOUR_BACKGROUND_DIALOG);

        self.__addChildWidgets();

        # hide dialog, until showAndEditVehicle() called
        # (...at which point, deiconify() and lift())

        self.withdraw();


    def __centerSelfToParentWindow(self) -> None:
        """centers the dialog relative to the parent Toplevel() window"""

        if self.winfo_viewable(): self.update_idletasks(); # enter message-pump temporarily
        _x = self.master.winfo_rootx() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2);
        _y = self.master.winfo_rooty() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2);
        self.geometry(f"+{_x}+{_y}");


    def __addChildWidgets(self) -> None:
        """adds the child-widgets to the dialog"""

        self.__vehicleWidgetsFrame = ttk.Labelframe(master=self, text="Vehicle", style="vdb.dialog.TLabelframe");
        self.__vehicleWidgetsFrame.pack(padx=15, pady=(20, 2), fill="both", expand=True);

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # the __vehicleWidgetsFrame uses an implicitly-defined grid;
        # its #rows and #columns aren't defined before widget grid()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        self.__declareVehicleWidgets(_widgetsContainer=self.__vehicleWidgetsFrame);

        # for each declared PropertyToWidgetMapping, render a label
        # displaying its name, and grid() its widget rightwards.

        for _rowIndex, (_propName, _propWidgetMapping) in enumerate(self.__vehicleWidgets.items()):

            ttk.Label(
                self.__vehicleWidgetsFrame,
                style="vdb.labelframed.TLabel",
                text=f"{app_filesysUtils.drinkingCamelCase_toKebabCase(_propName)}:"
            ).grid(column=0, row=_rowIndex, padx=(15, 25), pady=3, sticky="w");

            _propWidgetMapping.widget.grid(column=1, row=_rowIndex, padx=5, pady=3, sticky="w");

        # add the [Ok] button below the vehicle-properties' frame
        # this can be clicked using the [Enter] key too

        ttk.Button(self, text="Ok", default="active", command=self.__reconstructVehicle_andClose).pack(padx=10, pady=(20, 10));
        self.bind("<Return>", self.__reconstructVehicle_andClose);


    def __declareVehicleWidgets(self, _widgetsContainer :tkinter.Widget) -> None:
        """initialises the __vehicleWidgets member with widgets for vehcile properties (a textbox for regPlate, etc)"""

        def _getDatetime_fromTextboxValue_(_textboxValue :str) -> datetime.datetime|None:
            return (
                datetime.datetime.strptime(_textboxValue, EditVehicleDialog.__DATETIME_FORMAT_)
                if (_textboxValue != "")
                else None
            );

        def _getTextboxValue_fromDatetime_(_datetime :datetime.datetime|None) -> str:
            return (
                _datetime.strftime(EditVehicleDialog.__DATETIME_FORMAT_)
                if (_datetime is not None)
                else ""
            );

        # getValue() and setValue() return/take-in objects of {↓these↓} types...
        #   regPlate            :str;
        #   typeOfVehicle       :VehicleType;
        #   fuelType            :VehicleFuelType;
        #   makeAndModel        :str;
        #   isCurrentlyTaxed    :bool;
        #   manufacturedDate    :datetime.datetime;
        #   taxExpiryDate       :datetime.datetime|None;
        #   lastServicedDate    :datetime.datetime|None;

        self.__vehicleWidgets :dict[str, EditVehicleDialog.PropertyToWidgetMapping] = {};

        _isCurrentlyTaxed_booleanVar = tkinter.BooleanVar(master=self, value=False);

        self.__vehicleWidgets = {
            "regPlate" : EditVehicleDialog.PropertyToWidgetMapping(
                widget   =  ui_c_textboxWithPlaceholder.TextboxWithPlaceholder(_widgetsContainer, "eg AB12 CDE"),
                getValue =  lambda : self.__vehicleWidgets["regPlate"].widget.get().upper(),
                setValue =  lambda _newValue : self.__vehicleWidgets["regPlate"].widget.insert(0, _newValue.upper()),
                validate =  lambda : bool(re.match(r"^[A-Z0-9 ]{3,10}$", self.__vehicleWidgets["regPlate"].getValue()))
            ),
            "typeOfVehicle" : EditVehicleDialog.PropertyToWidgetMapping(
                widget   =  ttk.Combobox(_widgetsContainer, state="readonly", values=[_e.name.lower() for _e in db_schemaClasses.Vehicle.VehicleType]),
                getValue =  lambda : db_schemaClasses.Vehicle.VehicleType[self.__vehicleWidgets["typeOfVehicle"].widget.get().upper()],
                setValue =  lambda _newValue : self.__vehicleWidgets["typeOfVehicle"].widget.set(_newValue.name.lower()),
                validate =  lambda : self.__vehicleWidgets["typeOfVehicle"].widget.get().upper() in db_schemaClasses.Vehicle.VehicleType.__members__.keys()
            ),
            "fuelType" : EditVehicleDialog.PropertyToWidgetMapping(
                widget   =  ttk.Combobox(_widgetsContainer, state="readonly", values=[_e.name.lower() for _e in db_schemaClasses.Vehicle.VehicleFuelType]),
                getValue =  lambda : db_schemaClasses.Vehicle.VehicleFuelType[self.__vehicleWidgets["fuelType"].widget.get().upper()],
                setValue =  lambda _newValue : self.__vehicleWidgets["fuelType"].widget.set(_newValue.name.lower()),
                validate =  lambda : self.__vehicleWidgets["fuelType"].widget.get().upper() in db_schemaClasses.Vehicle.VehicleFuelType.__members__.keys()
            ),
            "makeAndModel" : EditVehicleDialog.PropertyToWidgetMapping(
                widget   =  ttk.Entry(_widgetsContainer),
                getValue =  lambda : self.__vehicleWidgets["makeAndModel"].widget.get(),
                setValue =  lambda _newValue : self.__vehicleWidgets["makeAndModel"].widget.insert(0, _newValue),
                validate =  lambda : True
            ),
            "isCurrentlyTaxed" : EditVehicleDialog.PropertyToWidgetMapping(
                widget   =  ttk.Checkbutton(_widgetsContainer, variable=_isCurrentlyTaxed_booleanVar),
                getValue =  _isCurrentlyTaxed_booleanVar.get,
                setValue =  _isCurrentlyTaxed_booleanVar.set,
                validate =  lambda : True
            ),
            "manufacturedDate" : EditVehicleDialog.PropertyToWidgetMapping(
                widget   =  ui_c_textboxWithPlaceholder.TextboxWithPlaceholder(_widgetsContainer, EditVehicleDialog.__DATETIME_FORMAT_DESCRIPTION_),
                getValue =  lambda : _getDatetime_fromTextboxValue_(self.__vehicleWidgets["manufacturedDate"].widget.get()),
                setValue =  lambda _newValue : self.__vehicleWidgets["manufacturedDate"].widget.insert(0, _getTextboxValue_fromDatetime_(_newValue)),
                validate =  lambda : (
                    (lambda _val : bool(_val and re.match(r"^\d{2}\-\d{2}\-\d{4}$", _val)))
                    (self.__vehicleWidgets["manufacturedDate"].widget.get())
                )
            ),
            "taxExpiryDate" : EditVehicleDialog.PropertyToWidgetMapping(
                widget   =  ui_c_textboxWithPlaceholder.TextboxWithPlaceholder(_widgetsContainer, EditVehicleDialog.__DATETIME_FORMAT_DESCRIPTION_),
                getValue =  lambda : _getDatetime_fromTextboxValue_(self.__vehicleWidgets["taxExpiryDate"].widget.get()),
                setValue =  lambda _newValue : self.__vehicleWidgets["taxExpiryDate"].widget.insert(0, _getTextboxValue_fromDatetime_(_newValue)),
                validate =  lambda : (
                    (lambda _val : (_val == "") or bool(_val and re.match(r"^(\d{2}\-\d{2}\-\d{4})?$", _val)))
                    (self.__vehicleWidgets["taxExpiryDate"].widget.get())
                )
            ),
            "lastServicedDate" : EditVehicleDialog.PropertyToWidgetMapping(
                widget   =  ui_c_textboxWithPlaceholder.TextboxWithPlaceholder(_widgetsContainer, EditVehicleDialog.__DATETIME_FORMAT_DESCRIPTION_),
                getValue =  lambda : _getDatetime_fromTextboxValue_(self.__vehicleWidgets["lastServicedDate"].widget.get()),
                setValue =  lambda _newValue : self.__vehicleWidgets["lastServicedDate"].widget.insert(0, _getTextboxValue_fromDatetime_(_newValue)),
                validate =  lambda : (
                    (lambda _val : (_val == "") or bool(_val and re.match(r"^(\d{2}\-\d{2}\-\d{4})?$", _val)))
                    (self.__vehicleWidgets["lastServicedDate"].widget.get())
                )
            )
        };


    def __showSelf(self, _dialogTitle :str) -> None:
        """disables the parent window, and shows this dialog"""

        self.title(_dialogTitle);

        # prevent interaction with the parent window
        # self.master.protocol("WM_DELETE_WINDOW", lambda : None);

        # show thyself
        self.deiconify(); self.lift(); self.focus_set();
        self.__centerSelfToParentWindow();
        if not self.winfo_viewable(): raise Exception("the edit-vehicle dialog failed to become visible");


    def showAndEditVehicle(self, _vehicleIn :db_schemaClasses.Vehicle, _preventEditingRegPlate :bool = False) -> db_schemaClasses.Vehicle:
        """
        shows a vehicle-editing dialog with the input-fields set to the
        values of the _vehicleIn, permits editing these values, then returns
        the resultant Vehicle state on dialog closure.

        example usage:
            _editVehicleDialog = EditVehicleDialog(self);
            _editedVehcile :Vehicle = _editVehicleDialog.showAndEditVehicle(_existingVehicle);
        """

        self.__showSelf(_dialogTitle=f"Editing {_vehicleIn.regPlate}..." if (_vehicleIn.regPlate != "") else "New vehicle...");
        self.__dialogIsClosed.set(value=False);

        # populate the input-fields (for regPlate, etc.), then when
        # the [ok] button is clicked, instanciate an updated vehicle
        # form the input-fields, and make this method return it.

        for _propName, _propWidgetMapping in self.__vehicleWidgets.items():
            _propWidgetMapping.setValue(getattr(_vehicleIn, _propName));

            if (_propName == "regPlate") and _preventEditingRegPlate:
                _propWidgetMapping.widget.config(state="disabled");

        self.wait_variable(self.__dialogIsClosed);
        return self.__vehicleOut;


    def __reconstructVehicle_andClose(self, _event=None) -> None:
        """parses the input-fields to instanciate a Vehicle(), then closes the dialog"""

        _valuesAreValid :bool; _whatsWrongMsg :str;
        (_valuesAreValid, _whatsWrongMsg) = self.__checkThatInputtedValues_areValid();

        if not _valuesAreValid:
            messagebox.showwarning("Sorry darling...", _whatsWrongMsg, parent=self);
            return;

        self.__vehicleOut = db_schemaClasses.Vehicle(
            ** { _propName : _propWidgetMapping.getValue() for _propName, _propWidgetMapping in self.__vehicleWidgets.items() }
        );

        self.__closeDialog();


    def __checkThatInputtedValues_areValid(self) -> tuple[bool, str]:
        """returns [whether the input-fields' values are valid] and [if not, why]"""

        for _fieldName, _fieldWidgetMapping in self.__vehicleWidgets.items():

            try:
                if not _fieldWidgetMapping.validate():
                    return (False, f"""That {app_filesysUtils.drinkingCamelCase_toKebabCase(_fieldName)} ({_fieldWidgetMapping.getValue() or "empty"}) isn't valid.""");

            except Exception as _e:
                messagebox.showwarning(
                    title=f"{app_filesysUtils.drinkingCamelCase_toKebabCase(_fieldName)}'s a bit funny...",
                    message=f"The \"{app_filesysUtils.drinkingCamelCase_toKebabCase(_fieldName)}\" seems invalid because {str(_e)}",
                    parent=self
                );

        return (True, "(all input was valid)");


    def __closeDialog(self) -> None:
        """closes the currently-open loading dialog"""

        if not self.winfo_viewable(): raise RuntimeError("cannot __closeDialog() because the dialog isn't currently shown");

        # re-enable the parent-window's [x] button, & close self
        # self.master.protocol("WM_DELETE_WINDOW", self.master.destroy);

        self.__dialogIsClosed.set(value=True);
        self.destroy();