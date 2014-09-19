# DSMR P1 uitlezen
# (c) 10-2012 - GJ - gratis te kopieren en te plakken
# (c) 09-2014 - Frituurpan

import signal
import ConfigParser
import os
import time
import sys
from classes.emoncontroller import EmonController
from classes.input_parser import InputParser
from classes.serialcontroller import SerialController

versie = "3.0"


def exit_gracefully(signum, frame):
    # http://stackoverflow.com/questions/18114560/python-catch-ctrl-c-command-prompt-really-want-to-quit-y-n-resume-executi
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)

def read_serial(serialController, inputParser, emonController):
    #read & process input
    serialController.read_input()

    #read values
    energy_total = inputParser.get_energy_total()
    gas_total = inputParser.get_gas_total()
    current_watts = inputParser.get_current_watts()

    inputParser.reset()

    #post values
    emonController.upload_results(energy_total, gas_total, current_watts)


# #############################################################################
# Main program
##############################################################################
print ("DSMR P1 uitlezen", versie)
print ("Control-C om te stoppen")


def run_program():

    configParser = ConfigParser.RawConfigParser()
    currentDir = os.path.dirname(os.path.abspath(__file__))
    configFilePath = currentDir + r'/config.txt'
    configParser.read(configFilePath)

    apiKey = configParser.get('config', 'api_key')
    inputUrl = configParser.get('config', 'input_url')
    debug = configParser.getboolean('config', 'debug')

    #Init classes
    inputParser = InputParser()
    serialController = SerialController(inputParser)
    emonController = EmonController(inputUrl, apiKey)

    serialController.set_debug(debug)
    emonController.set_debug(debug)

    #open connection to meter
    serialController.open_connection()

    interval = 9
    interval_counter = 8
    try:
        while True:
            interval_counter += 1
            print interval_counter
            if interval_counter == interval:
                interval_counter = 0
                print ('read')
                read_serial(serialController, inputParser, emonController)
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print('close connection #1')
        serialController.close_connection()
        raise
    finally:
        #close connection
        print('close connection #2')
        serialController.close_connection()


original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)
run_program()