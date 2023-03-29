from SerialManager import JAISerial

if __name__ == "__main__":
    JAICamera = JAISerial("/dev/pts/4") # Change this to the correct serial port for the camera
    JAICamera.GetSupportedBaudRates()
    JAICamera.SetBaudRate(115200)
    JAICamera.GetSupportedBaudRates()