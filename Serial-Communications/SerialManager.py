import serial

class JAISerial:
    def __init__(self, serialPort, baudRate=9600, dataLength=serial.EIGHTBITS, stopBit=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, XonXoff=0, timeout=None):
        self.serialPort = serialPort
        self.baudRate = baudRate
        self.dataLength = dataLength
        self.stopBit = stopBit
        self.parity = parity
        self.timeout = timeout
        self.serialHandle = None
        self.__Open()

    def __Open(self):
        self.serialHandle = serial.Serial(self.serialPort, self.baudRate, self.dataLength, self.parity, self.stopBit, self.timeout, 0)
    
    def __Close(self):
        self.serialHandle.close()

    def __ChangeBaudRate(self, baudRate):
        self.__Close()
        self.serialHandle.baudrate = baudRate
        self.__Open()

    def __Write(self, command):
        # Command should be a string such as "CBDRT=1" or "SBDRT?"
        # It needs to be converted to bytes and have a carriage return and line feed added
        self.serialHandle.write(command.encode() + b'\r\n')

    def __Read(self):
        # Read the response until \r\n
        response = self.serialHandle.readline()
        return response

    def GetSupportedBaudRates(self):
        # Send the command
        self.__Write("SBDRT?")

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'SBDRT=<hexBaud>\r\n'
        # Where HexBaud is a hex value of the supported baud rates:
        #     0x01 = 9600
        #     0x03 = 19200
        #     0x07 = 38400
        #     0x0F = 57600
        #     0x1F = 115200

        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'SBDRT=<hexBaud>\r\n' then the command was recognized and the response is the supported baud rates
        elif response[0:6] == b'SBDRT=':
            # Convert the response to a string
            response = response.decode()

            # I cannot confirm that the return includes leading zeros, so instead I will find \r\n and remove it (more reliable)
            # Alternatively I was going to do something similar to response = response[6:10] but I am not sure if the return will always be 4 characters
            response = response.replace("\r\n", "")

            # Remove the SBDRT= from the response
            response = response.replace("SBDRT=", "")

            # Convert the response to an integer (base 16, accounts for both 0x01 and 0x1, etc.)
            response = int(response, 16)

            availableBaudRates = []
            if response >= 1:
                availableBaudRates.append(9600)
            if response >= 3:
                availableBaudRates.append(19200)
            if response >= 7:
                availableBaudRates.append(38400)
            if response >= 15:
                availableBaudRates.append(57600)
            if response == 31:
                availableBaudRates.append(115200)

            return availableBaudRates

    def SetBaudRate(self, baudRate):
        # If baudRate is the same as the current baud rate, then return "COMPLETE"
        if baudRate == self.baudRate:
            return "COMPLETE"

        # Note: Need to confirm if baudRate needs to be decimal or hex
        # This only supports decimal values for now

        encodedBaudRate = 1 # 9600 by default
        
        if baudRate == 115200:
            encodedBaudRate = 16
        elif baudRate == 57600:
            encodedBaudRate = 8
        elif baudRate == 38400:
            encodedBaudRate = 4
        elif baudRate == 19200:
            encodedBaudRate = 2
        
        # Send the command
        self.__Write("CBDRT=" + str(encodedBaudRate))

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'COMPLETE\r\n'
        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'COMPLETE\r\n' then the command was recognized and the baud rate was changed
        elif response == b'COMPLETE\r\n':
            self.__ChangeBaudRate(baudRate)
            self.__Write("CBDRT=" + str(encodedBaudRate))
            response = self.__Read()
            if response == b'COMPLETE\r\n':
                # Update the baud rate
                self.baudRate = baudRate
                return "COMPLETE"
            else:
                self.__ChangeBaudRate(9600)
                return "FAILED"










    



