# This file is not documented since it is mainly used for testing the class JAISerial which is the intended product delivery
from SerialManager import JAISerial

if __name__ == "__main__":
    JAICamera = JAISerial("COM1") # Change this to the correct serial port for the camera (likely COM1)
    JAICamera.GetSupportedBaudRates() # Gets the Supported Baud Rates as an array
    JAICamera.SetBaudRate(115200) # (We don't really care about Supported Baud Rates, we know the max is 115200)
    JAICamera.GetSupportedBaudRates() # Verify it changed succesfully by getting the supported baud rates again
