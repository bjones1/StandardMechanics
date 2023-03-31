# This file is not documented since it is mainly used for testing the class JAISerial which is the intended product delivery
from SerialManager import JAISerial

if __name__ == "__main__":
    JAICamera = JAISerial("/dev/pts/7") # Change this to the correct serial port for the camera (likely COM1)
    JAICamera.SetCLClock(0)
