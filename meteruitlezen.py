# DSMR P1 uitlezen
# (c) 10-2012 - GJ - gratis te kopieren en te plakken
from _socket import gaierror
from emoncontroller import EmonController
from input_parser import InputParser
from serialcontroller import SerialController

versie = "2.0"

apiKey = ''
inputUrl = ''
debug = True

# #############################################################################
#Main program
##############################################################################
print ("DSMR P1 uitlezen", versie)
print ("Control-C om te stoppen")

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
emonController.upload_results(energy_total,gas_total,current_watts)