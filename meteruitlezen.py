# DSMR P1 uitlezen
# (c) 10-2012 - GJ - gratis te kopieren en te plakken
# (c) 09-2014 - Frituurpan

import ConfigParser
from classes.emoncontroller import EmonController
from classes.input_parser import InputParser
from classes.serialcontroller import SerialController

versie = "3.0"

# #############################################################################
# Main program
##############################################################################
print ("DSMR P1 uitlezen", versie)
print ("Control-C om te stoppen")

configParser = ConfigParser.RawConfigParser()
configFilePath = r'./config.txt'
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

#read & process input
serialController.read_input()

#close connection
serialController.close_connection()

#read values
energy_total = inputParser.get_energy_total()
gas_total = inputParser.get_gas_total()
current_watts = inputParser.get_current_watts()

#post values
emonController.upload_results(energy_total, gas_total, current_watts)