import serial # pip install pyserial (https://pypi.org/project/pyserial/)

class JAISerial:
# <div>The JAI-4000M Serial Manager is a class that allows for easy
#     communication with the JAI SW-4000M-PMCL camera via serial
#     communication.</div>
# <div>Default Class Parameters were determined by the JAI SW-4000M-PMCL
#     Command List <a
#         href="../datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=3"
#         target="_blank" rel="noopener">datasheet</a>.</div>
    def __init__(self, serialPort, baudRWate=9600, dataLength=serial.EIGHTBITS, stopBit=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, XonXoff=0, timeout=None):
        """
        Initializes a JAI-4000M Serial Manager on the specified serial port.
        :param serialPort: The serial port to use (ex. "COM1")
        :param baudRate: The baud rate to use in decimal (9600, 19200, 38400, 57600, 115200)
        :param dataLength: The data length to use (serial.EIGHTBITS, serial.SEVENBITS, serial.SIXBITS, serial.FIVEBITS)
        :param stopBit: The stop bit to use (serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO)
        :param parity: The parity to use (serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK, serial.PARITY_SPACE)
        :param XonXoff: The Xon/Xoff to use (0, 1)
        :param timeout: The timeout to use in seconds (None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        :type serialPort: str
        :type baudRate: int
        :type dataLength: int
        :type stopBit: int
        :type parity: int
        :type XonXoff: int
        :type timeout: int
        """

        self.serialPort = serialPort
        self.baudRate = baudRate
        self.dataLength = dataLength
        self.stopBit = stopBit
        self.parity = parity
        self.timeout = timeout
        self.serialHandle = None
        self.__Open()

    def __Open(self):
        """
        Opens the serial port, this is called when the class is initialized and when the baud rate is changed, it is intended to be used internally and should not be called directly by the user.
        """

        self.serialHandle = serial.Serial(self.serialPort, self.baudRate, self.dataLength, self.parity, self.stopBit, self.timeout, 0)
    
    def __Close(self):
        """
        Closes the serial port, this is called when the baud rate is changed and when the class is destroyed, it is intended to be used internally and should not be called directly by the user.
        """

        self.serialHandle.close()

    def __ChangeBaudRate(self, baudRate):
        """
        Changes the baud rate of the serial port, this is called when the baud rate is changed by SetBaudRate, it is intended to be used internally and should not be called directly by the user.

        :param baudRate: The baud rate to change to in decimal (9600, 19200, 38400, 57600, 115200)
        :type baudRate: int
        """

        self.__Close()
        self.serialHandle.baudrate = baudRate
        self.__Open()

    def __Write(self, command):
        """ 
        Writes a command to the serial port, it is intended to be used internally and should not be called directly by the user.

        :param command: The command to send to the serial port (ex. "CBDRT=1")
        :type command: str
        """

        # The command is encoded to a byte array and then a carriage return and line feed are added in accordance with the JAI Serial Protocol (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=3)
        self.serialHandle.write(command.encode() + b'\r\n')

    def __Read(self):
        """
        Reads a response from the serial port, it is intended to be used internally and should not be called directly by the user. This function will block until a response is received or the timeout (see class constructor) is reached.
        """

        response = self.serialHandle.readline()
        return response

    def GetSupportedBaudRates(self):
        """
        Gets the supported baud rates from the camera.
        :return: A list of supported baud rates (9600, 19200, 38400, 57600, 115200) or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: list or str
        """

        # Send the command (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=5)
        self.__Write("SBDRT?")

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'SBDRT=<hexBaud>\r\n'
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=5)
        # Where HexBaud is a hex value of the supported baud rates:
        #     00001 - 0x01 = 9600
        #     00011 - 0x03 = 19200
        #     00111 - 0x07 = 38400
        #     01111 - 0x0F = 57600
        #     11111 - 0x1F = 115200

        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized (this should not happen, if it does it is indicative of bad serial communication)
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
        """
        Sets the baud rate of the serial port via (CBDRT) command.
        :param baudRate: The baud rate to change to in decimal (9600, 19200, 38400, 57600, 115200)
        :type baudRate: int
        :return: "COMPLETE" if the baud rate was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!, FAILED)
        :rtype: str
        """

        # If the baud rate is already set to the desired baud rate then return "COMPLETE", do not send the command again
        # self.baudRate is maintained by the class and is updated when the baud rate is changed
        if baudRate == self.baudRate:
            return "COMPLETE"

        # Note: Need to confirm if baudRate needs to be decimal or hex
        # This only supports decimal values for now (seemed to work in testing session with Trey Leonard)
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=5)
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
            # We must execute a confirmation command once the baud rate is changed to verify we are still communicating with the camera
            # This protocol is described in the datasheet (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=4)
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










    



