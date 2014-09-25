import Queue
import threading
import serial


class mySerial(threading.Thread):
    def __init__(self, queue):
        super(mySerial, self).__init__()
        self.queue = queue  # the received data is put in a queue
        self.buffer = ''
        # configure serial connection
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.SEVENBITS
        self.ser.parity = serial.PARITY_EVEN
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.xonxoff = 0
        self.ser.rtscts = 0
        self.ser.timeout = None
        self.ser.port = "/dev/ttyUSB0"
        #self.ser.port = "COM5"
        self.ser.open()

    def run(self):
        while True:
            self.buffer += self.ser.read(self.ser.inWaiting() or 1)  # read all char in buffer
            while '\n' in self.buffer:  # split data line by line and store it in var
                var, self.buffer = self.buffer.split('\n', 1)
                self.queue.put(var)  #put received line in the queue


class Base():
    def __init__(self):
        self.queue = Queue.Queue(0)  # create a new queue
        self.ser = mySerial(self.queue)

        self.ser.start()  # run thread


    def main(self):
        while (True):
            try:
                var = self.queue.get(False)  # try to fetch a value from queue
            except Queue.Empty:
                pass  # if it is empty, do nothing
            else:
                print(var)


if __name__ == '__main__':
    b = Base()
    b.main()