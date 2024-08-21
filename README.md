# CESAR_epic_01
--------------------------------------------------------------------------------------
# cosimulation between 1transmission network in pypower and 2 distribution network in gridlabd

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