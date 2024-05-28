# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 10:08:26 2018

@author: monish.mukherjee
"""
import scipy.io as spio
from pypower.api import case118, ppoption, runpf, runopf
import math
import numpy
import time
import helics as h
import random
import logging
import argparse

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

################################
import requests
import json
import time
import threading

# URLs for getting device status and controlling the device
url_status = "https://api.smartthings.com/v1/devices/2f20efea-b413-4fd3-b8c1-45279fc412ce/status"
url_control = "https://api.smartthings.com/v1/devices/2f20efea-b413-4fd3-b8c1-45279fc412ce/commands"

status = ""
switch_status = ""

headers = {
    'Authorization': 'Bearer 0dc70a10-bda8-4d39-a1ee-67dc45e91595',
    'Content-Type': 'application/json'
}

def get_device_status():
    response = requests.get(url_status, headers=headers)
    data = response.json()
    # Adjust the following line based on the actual structure of the JSON response
    status = data['components']['main']['switch']['switch']['value']

    if status == "on":
        switch_status = "CLOSED"
    elif status == "off":
        switch_status = "OPEN"

    return switch_status

#################################


def destroy_federate(fed):
    grantedtime = h.helicsFederateRequestTime(fed, h.HELICS_TIME_MAXTIME)
    status = h.helicsFederateDisconnect(fed)
    h.helicsFederateDestroy(fed)
    logger.info("Federate finalized")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-c', '--case_num',
                        help='Case number, must be either "1b" or "1c"',
                        nargs=1)
    args = parser.parse_args()

    #################################  Registering  federate from json  ########################################
    #case_num = str(args.case_num[0])
    fed = h.helicsCreateValueFederateFromConfig(f"switch_controller.json")
    #h.helicsFederateRegisterInterfaces(fed, "1a_Transmission_config.json")
    federate_name = h.helicsFederateGetName(fed)
    logger.info("HELICS Version: {}".format(h.helicsGetVersion()))
    logger.info("{}: Federate {} has been registered".format(federate_name, federate_name))
    pubkeys_count = h.helicsFederateGetPublicationCount(fed)
    subkeys_count = h.helicsFederateGetInputCount(fed)
    ######################   Reference to Publications and Subscription form index  #############################
    pubid = {}
    subid = {}
    for i in range(0, pubkeys_count):
        pubid["m{}".format(i)] = h.helicsFederateGetPublicationByIndex(fed, i)
        logger.info("######: pubid ---> {}".format( pubid))
        
        pubtype = h.helicsPublicationGetType(pubid["m{}".format(i)])
        pubname = h.helicsPublicationGetName(pubid["m{}".format(i)])
        logger.info("{}: Registered Publication ---> {}".format(federate_name, pubname))
    for i in range(0, subkeys_count):
        subid["m{}".format(i)] = h.helicsFederateGetInputByIndex(fed, i)
        h.helicsInputSetDefaultComplex(subid["m{}".format(i)], 0, 0)
        sub_key = h.helicsSubscriptionGetTarget(subid["m{}".format(i)])
        logger.info("{}: Registered Subscription ---> {}".format(federate_name, sub_key))

    ######################   Entering Execution Mode  ##########################################################
    h.helicsFederateEnterInitializingMode(fed)
    status = h.helicsFederateEnterExecutingMode(fed)


    plotting = False ## Adjust this flag to visulaize the control actions aas the simulation progresses
    hours = 1
    total_inteval = int(60 * 60 * hours)
    grantedtime = -1
    update_interval = 30 #1 * 60 ## Adjust this to change EV update interval
    k = 0
    time_sim = []
    feeder_real_power = []
    switch_state = "CLOSED"

    #########################################   Starting Co-simulation  ####################################################

    for t in range(0, total_inteval, update_interval):

        ############################   Publishing Voltage to GridLAB-D #######################################################
        #if (((grantedtime% 300 ==0) or (grantedtime% 300 ==180))and (grantedtime >0)): #close switch every 5 min
        #    switch_state = "CLOSED"
        if (grantedtime% 30 ==0): #update status very 30sec
            switch_state = get_device_status()
            logger.info("{}: switch state val = {} ".format(federate_name, switch_state))
            for i in range(0, pubkeys_count):
            #for i in range(0, 1):
                pub = pubid["m{}".format(i)]
                if i == 0:
                    status = h.helicsPublicationPublishString(pub, switch_state)
                else:
                    status = h.helicsPublicationPublishString(pub, test_val)
                    logger.info("..........{}: test_val".format(test_val))
                    test_val= test_val+ 2.505
            # status = h.helicsEndpointSendEventRaw(epid, "fixed_price", 10, t)

            logger.info("switch state => {}".format(switch_state))

        logger.info("{} - {}".format(grantedtime, t))
        while grantedtime < t:
            grantedtime = h.helicsFederateRequestTime(fed, t)

        #############################   Subscribing to Feeder Load from to GridLAB-D ##############################################

        for i in range(0, subkeys_count):
            sub = subid["m{}".format(i)]
            demand = h.helicsInputGetComplex(sub)
            rload = demand.real *1000;
            iload = demand.imag * 1000;
        logger.info("{}: Federate Granted Time = {}".format(federate_name,grantedtime))
        logger.info("{}: Load current consumption = {} Amps".format(federate_name, complex(round(rload,2), round(iload,2)) / 1000))
        # print(voltage_plot,real_demand)

     
    ##############################   Terminating Federate   ########################################################
    t = 60 * 60 * 24
    while grantedtime < t:
        grantedtime = h.helicsFederateRequestTime(fed, t)
    logger.info("{}: Destroying federate".format(federate_name))
    destroy_federate(fed)
    logger.info("{}: Done!".format(federate_name))
