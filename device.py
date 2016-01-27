import os
import serial

ARDUINO_PORT = os.environ.get('ARDUINO_PORT', '/dev/tty.usbmodem1411')
ROW_SIZE = os.environ.get('ROW_SIZE', 16)


class Device:
    def __init__(self):
        self.arduino = serial.Serial(ARDUINO_PORT)

    def print_rows(self, first_row="", second_row=""):
        message = "{}|{}&".format(first_row.ljust(ROW_SIZE), second_row.ljust(ROW_SIZE))
        self.arduino.write(message.encode())

    def clear_screen(self):
        message = ' ' * ROW_SIZE + '|' + ' ' * ROW_SIZE + '&'
        self.arduino.write(message.encode())
