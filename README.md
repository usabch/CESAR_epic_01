# CESAR_epic_01
Co-Simulation code using , helics, gridlabd d , python and pypower. for CESAR project, EPIC,UNCC

- basic gridlabd module to reprsent source , switch and load.
- the switch status is fetched by the switch_controller.py file using https request. The status is published to helics file.
- gridlab-d subscribes to this switch status and updates the switch accordingly.
- the load current measured using the recorder confirms for the switch closing and opening.

- the 2nd python file st_control.py is used to update the IOT switch status every 5 mins. This folder is used so that the time sync happens between all the federates as expected.

run command: helics run --path=switch_cosim_runner.json
