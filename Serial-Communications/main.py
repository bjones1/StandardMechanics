# This file is not documented since it is mainly used for testing the class JAISerial which is the intended product delivery
from SerialManager import JAISerial

if __name__ == "__main__":
    # Change this to the correct serial port for the camera (likely COM1)
    JAICamera = JAISerial("/dev/pts/6")
    test = JAICamera.GetSupportedBaudRates()
    test2 = JAICamera.SetBaudRate(115200)
    print(test)
    print(test2)
