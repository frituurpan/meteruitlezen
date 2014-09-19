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

        # Set COM port config
        self.ser = serial.Serial()
        self.get_connection().baudrate = 9600
        self.get_connection().bytesize = serial.SEVENBITS
        self.get_connection().parity = serial.PARITY_EVEN
        self.get_connection().stopbits = serial.STOPBITS_ONE
        self.get_connection().xonxoff = 0
        self.get_connection().rtscts = 0
        self.get_connection().timeout = 20
        self.get_connection().port = "/dev/ttyUSB0"

    def open_connection(self):
        #Open COM port
        try:
            self.get_connection().open()
        except:
            if self.is_debug():
                print("Skip exit")
            else:
                sys.exit("Fout bij het openen van %s. Aaaaarch." % self.get_connection().name)

    def read_input(self):
        if self.is_debug():
            counter = 0
            with open('debugdata.txt') as f:
                for line in f:
                    self.inputParser.process_line(line, counter)
                    counter += 1

            print("debugging")
        else:
            # Initialize
            #p1_teller is mijn tellertje voor van 0 tot 20 te tellen
            p1_teller = 0

            while p1_teller < 20:
                #Read 1 line van de seriele poort
                try:
                    p1_raw = self.get_connection().readline()
                except:
                    sys.exit("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % self.get_connection().name)

                self.inputParser.process_line(p1_raw, p1_teller)
                p1_teller += 1

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
        if(self.is_debug()):
            return

        #Close port and show status
        try:
            self.get_connection().close()
        except:
            sys.exit("Oops %s. Programma afgebroken. Kon de seriele poort niet sluiten." % self.get_connection().name)