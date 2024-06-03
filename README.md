# CESAR_epic_01
Co-Simulation code using , helics, gridlabd d , python and pypower. for CESAR project, EPIC,UNCC

- basic gridlabd module to reprsent source , switch and load.
- switch being run by a scheduler in GLD and also being CLOSED from python file every 300sec and OPEN 180sec after closing. (previous version)

-currently the switch status is fetched from cloud via https request and updated in python.
- the 2nd python file is updating the IOT switch status every 5 mins.

run command: helics run --path=switch_cosim_runner.json
