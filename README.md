# CESAR_epic_01
# latest comments are found on top of the page
--------------------------------------------------------------------------------------
# cosimulation between 1transmission network in pypower and 2 distribution network in gridlabd
------------------------------------------------------------------------------------------------
Changes in the run time have been done to observe the difference in reponse. The procedure was done to understand in better the time synvhronization between models.

The output file attached to the jira ticket contains the 3 differnt load curves with respect to
1. both running for 24hrs
2. 2nd grid running from 0600 -2000hrs without offset in .json file
3. 2nd grid running from 0600 -2000hrs with offset updated for 21600sec (6hrs)

More observations to be done. The decision has to be made either to be working on getting the same run on HPC or understanding the simulation/model better towards an effort to make it more accurate.

--------------------------------------------------------------------
the base is taken from the helics 1a grilabd example1 in misc folder.
contains 118bus T-sytem connected to 123 node D-system.
the D-system is duplicated and attached to 117 bus line as load.

the complete system with 3 federates and helics is running. 
In detailed observation and experiments have to be done on it.

parallelly the same is tried to run on HPC to comapre the speedness and paralelle processing capabilities of helics as a cosimulator.

-----------------------------------------------------------------------------------------------
Co-Simulation code using , helics, gridlabd d , python and pypower. for CESAR project, EPIC,UNCC

- basic gridlabd module to reprsent source , switch and load.
- the switch status is fetched by the switch_controller.py file using https request. The status is published to helics file.
- gridlab-d subscribes to this switch status and updates the switch accordingly.
- the load current measured using the recorder confirms for the switch closing and opening.

- the 2nd python file st_control.py is used to update the IOT switch status every 5 mins. This folder is used so that the time sync happens between all the federates as expected.

run command: helics run --path=switch_cosim_runner.json