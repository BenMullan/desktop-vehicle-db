# file:     vehicleFilterOptions.py - a class defining criteria for filtering Vehicle()s
# author:   Ben Mullan (2025)

import dataclasses, datetime;
from . import (db_schemaClasses);


@dataclasses.dataclass
class VehicleFilterOptions (object):
    """
    represents a set of criteria for determining if a given
    Vehicle() instance should be included in a filtered search
    """


    # all filter-options can be (and are by default) `None`
    # if a filter-option is `None`, it's ignored when filtering.
    # -
    # the naming-convention for these options deviates slightly from
    # that of the elsewhere in the codebase, in order that they work with
    # FilterVehiclesDialog.__getUiLabelString_fromFilterOptionName_()

    only_regPlates_containing       :str                                            | None = None;
    only_these_vehicleTypes         :set[db_schemaClasses.Vehicle.VehicleType]      | None = None;
    only_these_fuelTypes            :set[db_schemaClasses.Vehicle.VehicleFuelType]  | None = None;
    only_makesAndModels_containing  :str                                            | None = None;
    must_be_currentlyTaxed          :bool                                           | None = None;
    manufacturedDate_between        :tuple[datetime.datetime, datetime.datetime]    | None = None;
    taxExpiryDate_between           :tuple[datetime.datetime, datetime.datetime]    | None = None;
    lastServicedDate_between        :tuple[datetime.datetime, datetime.datetime]    | None = None;


    def __post_init__(self) -> None:
        """runs directly after object instantiation"""
        self.__makeDateRanges_inAscendingOrder();


    def __makeDateRanges_inAscendingOrder(self) -> None:
        """sets all date-ranges to be in ascending order"""

        if (self.manufacturedDate_between is not None):
            self.manufacturedDate_between = tuple(sorted(self.manufacturedDate_between));

        if (self.taxExpiryDate_between is not None):
            self.taxExpiryDate_between = tuple(sorted(self.taxExpiryDate_between));

        if (self.lastServicedDate_between is not None):
            self.lastServicedDate_between = tuple(sorted(self.lastServicedDate_between));


    @staticmethod
    def __dateIsInRange_(_date :datetime.datetime, _range :tuple[datetime.datetime|None, datetime.datetime|None]) -> bool:
        """returns True if the given date is within the given range"""

        # if a vehicle doesn't have eg a taxExpiryDate, then that date ISN'T in the range...
        if (_date is None): return None;

        return (
            (_range[0] or datetime.datetime.min)
            <= _date
            <= (_range[1] or datetime.datetime.max)
        );


    @staticmethod
    def getEmpty_() -> "VehicleFilterOptions":
        """
        returns a VehicleFilterOptions() with all filter-options set to `None`
        (ie. all vehicles will pass through it; none will be filtered-out)
        """
        return VehicleFilterOptions();


    @property
    def numberOfNonNullFilterOptions(self) -> int:
        """returns the number of defined (not-None) filter-options"""
        return sum(1 for _member in dataclasses.asdict(self).values() if (_member is not None));


    def isSatisfiedBy(self, _examinee :db_schemaClasses.Vehicle) -> bool:
        """returns True if the given Vehicle satisfies all set filter-options"""

        if (self.only_regPlates_containing is not None):
            if not (self.only_regPlates_containing.lower() in _examinee.regPlate.lower()):
                return False;

        if (self.only_these_vehicleTypes is not None):
            if not (_examinee.typeOfVehicle in self.only_these_vehicleTypes):
                return False;

        if (self.only_these_fuelTypes is not None):
            if not (_examinee.fuelType in self.only_these_fuelTypes):
                return False;

        if (self.only_makesAndModels_containing is not None):
            if not (self.only_makesAndModels_containing.lower() in _examinee.makeAndModel.lower()):
                return False;

        if (self.must_be_currentlyTaxed is not None):
            if not (_examinee.isCurrentlyTaxed == self.must_be_currentlyTaxed):
                return False;

        if (self.manufacturedDate_between is not None):
            if not VehicleFilterOptions.__dateIsInRange_(_examinee.manufacturedDate, self.manufacturedDate_between):
                return False;

        if (self.taxExpiryDate_between is not None):
            if not VehicleFilterOptions.__dateIsInRange_(_examinee.taxExpiryDate, self.taxExpiryDate_between):
                return False;

        if (self.lastServicedDate_between is not None):
            if not VehicleFilterOptions.__dateIsInRange_(_examinee.lastServicedDate, self.lastServicedDate_between):
                return False;

        # if we're here, none of the filter-options have been contravened;
        # the examinee Vehicle satisfies all the non-None filters.

        return True;


    def pluckMatchingVehicles(self, _examinees :list[db_schemaClasses.Vehicle]) -> list[db_schemaClasses.Vehicle]:
        """returns the Vehicles which satisfy all conditions of the current VehicleFilterOptions"""
        return [_vehicle for _vehicle in _examinees if self.isSatisfiedBy(_vehicle)];