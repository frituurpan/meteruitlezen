import time

__author__ = 'Frituurpan'

import sys
import serial
from classes.input_parser import InputParser

class SerialController:
    inputParser = InputParser
    serialConnection = serial.Serial

    debug = False

    def __init__(self, input_parser):
        self.inputParser = input_parser

    def open_connection(self):

        # Set COM port config
        self.serialConnection = serial.Serial()
        self.get_connection().baudrate = 9600
        self.get_connection().bytesize = serial.SEVENBITS
        self.get_connection().parity = serial.PARITY_EVEN
        self.get_connection().stopbits = serial.STOPBITS_ONE
        self.get_connection().xonxoff = 0
        self.get_connection().rtscts = 0
        self.get_connection().timeout = 20

        if self.is_debug():
            self.get_connection().port = "COM5"
        else:
            self.get_connection().port = "/dev/ttyUSB0"

        #Open COM port
        try:
            self.get_connection().open()
        except StandardError, e:
            print e
            sys.exit("Fout bij het openen van %s. Aaaaarch.")

    def read_input(self):
        # Initialize
        #p1_teller is mijn tellertje voor van 0 tot 20 te tellen
        counter = 0
        while 1:
            #Read 1 line van de seriele poort
            try:
                p1_raw = self.get_connection().readline()
                data_in_waiting = self.get_connection().inWaiting()

            except:
                sys.exit("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % self.get_connection().name)

            if counter == 20 and p1_raw.strip() != '!':
                print(str(counter) + '  ' + p1_raw)
                sys.exit('unreliable result')

            print str(counter) + ': ' + p1_raw

            if counter == 20 and p1_raw.strip() == '!':
                counter = -1
            counter += 1


            #self.inputParser.process_line(p1_raw, p1_teller)


    def get_connection(self):
        """
        :return: serial.Serial
        """
        return self.serialConnection

    def set_debug(self, do_debug):
        do_debug = bool(do_debug)
        self.debug = do_debug

    def is_debug(self):

        return self.debug

    def close_connection(self):
        #Close port and show status
        try:
            self.get_connection().close()
        except:
            sys.exit("Oops %s. Programma afgebroken. Kon de seriele poort niet sluiten." % self.get_connection().name)