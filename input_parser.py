import sys

__author__ = 'Administrator'


class InputParser:
    energyTotal = -1
    gasTotal = -1
    currentWatts = -1

    def __init__(self):
        pass

    def process_line(self, line, lineNumber):
        p1_str = str(line)
        p1_line = p1_str.strip()

        if lineNumber in [4, 5]:
            try:
                val = p1_line[p1_line.index('(') + 1:p1_line.index('*')];
                val = self.convert_value(val)
                self.energyTotal += val
            except ValueError:
                print("ValueError in Line  " + str(lineNumber) + ': ' + line)
                sys.exit('Fatal')

        if lineNumber == 9:
            try:
                val = p1_line[p1_line.index('(') + 1:p1_line.index('*')];
                val = self.convert_value(val)
                self.currentWatts = val
            except ValueError:
                print("ValueError in Line  " + str(lineNumber) + ': ' + line)
                sys.exit('Fatal')

        if lineNumber == 18:
            try:
                val = p1_line[p1_line.index('(') + 1:p1_line.index(')')];
                val = self.convert_value(val)
                self.gasTotal = val
            except ValueError:
                print("ValueError in Line  " + str(lineNumber) + ': ' + line)
                sys.exit('Fatal')

                # als je alles wil zien moet je de volgende line uncommenten
                # print (str(lineNumber) + str(': ') + str(p1_line))

    @staticmethod
    def convert_value(val):
        return int(float(val) * 1000)

    def get_energy_total(self):
        return self.energyTotal

    def get_gas_total(self):
        return self.gasTotal

    def get_current_watts(self):
        return self.currentWatts