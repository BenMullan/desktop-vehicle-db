ASCII class-diagram (of everything)
===================================

.. code-block::

    +-----------------+
    |    enum.Enum    |
    |-----------------|
    |                 |
    +-----------------+
            .                                
        /_\                               
            |                 [ enum.Enum ]  
            |                       .        
            |                      /_\       
            |                       |        
            |                       |        
    +-----------------+       +-------------+
    | VehicleFuelType |       | VehicleType |
    |-----------------|       |-------------|
    | DIESEL          |       | CAR         |
    | ELECTRONS       |       | LORRY       |
    | PETROL          |       | PICKUPTRUCK |
    +-----------------+       | VAN         |
                            +-------------+
                            
                            
                            
                            
    +----------------------+
    |        object        |
    |----------------------|
    |                      |
    +----------------------+
            .                                                                                                                                                                                                                                                                                                                                      
            /_\                                                                                                                                                                                                                                                                                                                                     
            |                                                             [ object ]                                                                       [ object ]                                                                        [ object ]                                                   [ object ]                               
            |                                                                 .                                                                                .                                                                                 .                                                            .                                    
            |                                                                /_\                                                                              /_\                                                                               /_\                                                          /_\                                   
            |                                                                 |                                                                                |                                                                                 |                                                            |                                    
            |                                                                 |                                                                                |                                                                                 |                                                            |                                    
    +----------------------+                                   +-----------------------------------+                                            +------------------------------------+                                            +------------------------------------+                               +--------------------+                        
    |       Vehicle        |                                   |        VehicleFilterOptions       |                                            |         DatabaseInteractor         |                                            |        DatabaseFileManager         |                               |     UiRenderer     |                        
    |----------------------|                                   |-----------------------------------|                                            |------------------------------------|                                            |------------------------------------|                               |--------------------|                        
    | fuelType             |  ---->  [ UnknownType ]           | lastServicedDate_between          |  ---->  [ UnknownType ]                    | __DB_CONFIG_                       |  ---->  [ UnknownType ]                    | __DB_CONFIG_                       |  ---->  [ UnknownType ]       | __UI_CONFIG_       |  ---->  [ UnknownType ]
    | isCurrentlyTaxed     |  ---->  [ VehicleFuelType ]       | manufacturedDate_between          |  ---->  [ datetime.datetime ]              | __singletonInstance_               |  ---->  [ db_schemaClasses.Vehicle ]       |------------------------------------|                               | __ttkStyles        |  ---->  [ tkinter.Tk ] 
    | lastServicedDate     |  ---->  [ VehicleType ]           | must_be_currentlyTaxed            |  ---->  [ db_schemaClasses.Vehicle ]       | __targetDbFile_fullPath            |                                            | _dbContainsValidVehiclesTable_     |                               |--------------------|                        
    | makeAndModel         |  ---->  [ dict ]                  | numberOfNonNullFilterOptions      |  ---->  [ list ]                           | targetDatabase                     |                                            | createNewVehiclesDb_               |                               | __declareTtkStyles |                        
    | manufacturedDate     |                                   | only_makesAndModels_containing    |  ---->  [ tuple ]                          |------------------------------------|                                            | getFullDbPath_fromDbName_          |                               | runMainWindow      |                        
    | regPlate             |                                   | only_regPlates_containing         |                                            | __ensureDatabaseExists_andIsValid_ |                                            | listExistingDatabases_             |                               +--------------------+                        
    | taxExpiryDate        |                                   | only_these_fuelTypes              |                                            | __init__                           |                                            | vehiclesDatabaseExists_andIsValid_ |                                                                             
    | typeOfVehicle        |                                   | only_these_vehicleTypes           |                                            | __yieldCursor                      |                                            +------------------------------------+                                                                             
    |----------------------|                                   | taxExpiryDate_between             |                                            | addVehicle                         |                                                                                                                                                               
    | deserialiseDatetime_ |                                   |-----------------------------------|                                            | deleteVehicle_byRegPlate           |                                                                                                                                                               
    | fromSerialisedDict_  |                                   | __dateIsInRange_                  |                                            | getAllVehicles                     |                                                                                                                                                               
    | getEmptyVehicle_     |                                   | __makeDateRanges_inAscendingOrder |                                            | getInstance                        |                                                                                                                                                               
    | getFormattedDate_    |                                   | __post_init__                     |                                            | getVehicleTableColumns             |                                                                                                                                                               
    | getTableCreationSql_ |                                   | getEmpty_                         |                                            | getVehicle_byRegPlate              |                                                                                                                                                               
    | serialiseDatetime_   |                                   | isSatisfiedBy                     |                                            | updateVehicle_byRegPlate           |                                                                                                                                                               
    | serialiseToDict      |                                   | pluckMatchingVehicles             |                                            +------------------------------------+                                                                                                                                                               
    | toDisplayTuple       |                                   +-----------------------------------+                                                                                                                                                                                                                                                 
    +----------------------+                                                                                                                                                                                                                                                                                                                         
                                        
                                        
                                        
                                        
    +----------------------------------+
    |            tkinter.Tk            |
    |----------------------------------|
    |                                  |
    +----------------------------------+
                    .                                           
                /_\                                          
                    |                                           
                    |                                           
                    |                                           
                    |                                           
                    |                                           
    +----------------------------------+                        
    |            MainWindow            |                        
    |----------------------------------|                        
    | __DB_CONFIG_                     |  ---->  [ Exception ]  
    | __UI_CONFIG_                     |  ---->  [ UnknownType ]
    | __dbRecordView                   |  ---->  [ any ]        
    |----------------------------------|                        
    | __addChildWidgets                |  ---->  [ list ]       
    | __configureGrid                  |  ---->  [ type ]       
    | __configureSelf                  |                        
    | __ensureDefaultDatabaseExists    |                        
    | __executeTasks_withLoadingDialog |                        
    | __getGeometry                    |                        
    | __init__                         |                        
    | __task_addNewVehicle             |                        
    | __task_deleteVehicle             |                        
    | __task_editVehicle               |                        
    | __task_filterVehicles            |                        
    | __task_loadAllVehicleRecords     |                        
    | _addInputtedVehicle_toDatabase_  |                        
    | _backgroundTask                  |                        
    | _deleteVehicleFromDb             |                        
    | _editVehicleWithDialog           |                        
    | _execTaskThenNextOne             |                        
    | _fetchVehicleFromDb              |                        
    | _writeVehicleBackToDb            |                        
    | report_callback_exception        |                        
    +----------------------------------+                        
                                                                    
                                                                    
                                                                    
                                                                    
    +-------------+       +------+       +--------------------------+
    | UnknownType |       | dict |       | db_schemaClasses.Vehicle |
    |-------------|       |------|       |--------------------------|
    |             |       |      |       |                          |
    +-------------+       +------+       +--------------------------+
                                                        
                                                        
                                                        
                                                        
    +-------------------+       +------+       +-------+
    | datetime.datetime |       | list |       | tuple |
    |-------------------|       |------|       |-------|
    |                   |       |      |       |       |
    +-------------------+       +------+       +-------+
                                            
                                            
                                            
                                            
    +-----+       +-----------+       +------+
    | any |       | Exception |       | type |
    |-----|       |-----------|       |------|
    |     |       |           |       |      |
    +-----+       +-----------+       +------+
