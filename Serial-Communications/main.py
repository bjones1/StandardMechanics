from SerialManager import JAISerial

if __name__ == "__main__":
    JAICamera = JAISerial("COM1") # Change this to the correct serial port for the camera (likely COM1)
    JAICamera.GetSupportedBaudRates()
    JAICamera.SetBaudRate(115200)
    JAICamera.GetSupportedBaudRates()
