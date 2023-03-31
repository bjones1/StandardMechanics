# <h2>Python Imports</h2>
# <table style="border-collapse: collapse; width: 101.811%; height: 46px;"
#     border="1">
#     <colgroup>
#         <col style="width: 33.42%;">
#         <col style="width: 33.42%;">
#         <col style="width: 33.291%;">
#     </colgroup>
#     <tbody>
#         <tr>
#             <td>Import&nbsp;</td>
#             <td>Library</td>
#             <td>Purpose</td>
#         </tr>
#         <tr>
#             <td>serial</td>
#             <td><a href="https://pypi.org/project/pyserial/">PySerial</a></td>
#             <td>Standard Library for connecting to a computer's serial ports
#                 across multiple operating systems using uniform commands</td>
#         </tr>
#     </tbody>
# </table>
# <p>&nbsp;</p>
import serial  # pip install pyserial
from enum import Enum


class JAISerial:
    class CLClockMHz(Enum):
        """
        The CL Clock MHz Enum is an Enum that contains the possible values for the CL Clock MHz setting.
        """
        MHZ_85 = 0  # 85 (Default)
        MHZ_63_75 = 1  # 63.75
        MHZ_42_5 = 2  # 42.5
        MHZ_31_875 = 3  # 31.875

    class ExposureMode(Enum):
        """
        The Exposure Mode Enum is an Enum that contains the possible values for the Exposure Mode setting.
        """
        OFF = 0  # Off
        TIMED = 1  # Timed (Default)
        TRIGGER_WIDTH = 2  # TriggerWidth

    class AnalogBaseGainDB(Enum):
        """
        The Analog Base Gain DB Enum is an Enum that contains the possible values for the Analog Base Gain DB setting.
        """
        DB_0 = 0  # 0dB (Default)
        DB_6 = 1  # 6dB
        DB_9_54 = 2  # 9dB
        DB_12 = 3  # 12dB

    class DeviceTapGeometryEnum(Enum):
        """
        The Tap Geometry Enum is an Enum that contains the possible values for the Tap Geometry setting.
        """
        GEOMETRY_1X2_1Y = 0
        GEOMETRY_1X3_1Y = 1
        GEOMETRY_1X4_1Y = 2  # Default
        GEOMETRY_1X8_1Y = 3
        GEOMETRY_1X10_1Y = 4

# <div>The JAISerial Class within Serial Manager is a class that allows for easy
#     communication with the JAI SW-4000M-PMCL camera via serial communication.
# </div>
# <div>The main idea is to make a package which can be used throughout other
#     Python Codes to facilitate direct communication with the camera.</div>
# <div>Default Class Parameters were determined by the JAI SW-4000M-PMCL Command
#     List <a href="../datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=3"
#         target="_blank" rel="noopener">datasheet</a>.</div>
# <div>Currently a blocker in that CodeChat does not seem to want to parse past
#     this point, as such please pay attention to inline comments until it is
#     resolved.</div>
    def __init__(self, serialPort, baudRate=9600, dataLength=serial.EIGHTBITS, stopBit=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, XonXoff=False, timeout=None):
        """
        Initializes a JAI-4000M Serial Manager on the specified serial port.
        :param serialPort: The serial port to use (ex. "COM1")
        :param baudRate: The baud rate to use in decimal (9600, 19200, 38400, 57600, 115200).
        :param dataLength: The data length to use (serial.EIGHTBITS, serial.SEVENBITS, serial.SIXBITS, serial.FIVEBITS).
        :param stopBit: The stop bit to use (serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO)
        :param parity: The parity to use (serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK, serial.PARITY_SPACE)
        :param XonXoff: The Xon/Xoff to use (True, False). Xon/Xoff is a software flow control protocol that uses the XON and XOFF characters to pause and resume data transmission. The camera does not support this.
        :param timeout: The timeout to use in seconds (float). If None, the read operation will block until at least one byte is received. If 0, the read operation will return immediately in all cases, returning zero or more, up to the requested number of bytes. If timeout is set to a value greater than zero, it may return fewer characters as requested if the timeout expires before the requested number of bytes is received.
        :type serialPort: str
        :type baudRate: int
        :type dataLength: int
        :type stopBit: int
        :type parity: int
        :type XonXoff: bool
        :type timeout: float
        """

        self.serialPort = serialPort
        self.baudRate = baudRate
        self.dataLength = dataLength
        self.stopBit = stopBit
        self.parity = parity
        self.timeout = timeout

        # Non-parameter Camera Variables (with Default Values)
        self.lineRate = 500  # 500 lines per second (Camera Default)
        self.CCLK = self.CLClockMHz.MHZ_85  # 85 MHz (Camera Default)
        self.exposureMode = self.ExposureMode.TIMED  # Timed (Camera Default)
        self.gainLevel = 100  # 100 (Camera Default)
        # 0dB (Camera Default)
        self.analogBaseGain = self.AnalogBaseGainDB.DB_0
        # 1x4 (Camera Default)
        self.deviceTapGeometry = self.DeviceTapGeometryEnum.GEOMETRY_1X4_1Y

        # Non-parameter Camera Variables (without Default Values)

        # Open the serial port
        self.serialHandle = None
        self.__Open()

    def __Open(self):
        """
        Opens the serial port, this is called when the class is initialized and when the baud rate is changed, it is intended to be used internally and should not be called directly by the user.
        """

        self.serialHandle = serial.Serial(
            self.serialPort, self.baudRate, self.dataLength, self.parity, self.stopBit, self.timeout, 0)

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
        # Theoretically, serialHandle should not be None, but just in case it is, this will Raise an Exception
        if self.serialHandle is None:
            raise Exception("__Write(self) accessed before __Open(self)")

        # The command is encoded to a byte array and then a carriage return and line feed are added in accordance with the JAI Serial Protocol (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=3)
        self.serialHandle.write(command.encode() + b'\r\n')

    def __Read(self):
        """
        Reads a response from the serial port, it is intended to be used internally and should not be called directly by the user. This function will block until a response is received or the timeout (see class constructor) is reached.
        """

        # Theoretically, serialHandle should not be None, but just in case it is, this will Raise an Exception
        if self.serialHandle is None:
            raise Exception("__Read(self) accessed before __Open(self)")

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
        Sets the baud rate of the camera via (CBDRT) command.
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
        encodedBaudRate = 1  # 9600 by default

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

    def GetBaudRate(self):
        """
        Gets the baud rate of the camera via (CBDRT?) command.
        :return: The current baud rate of the camera in decimal form or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: int or str
        """

        # Send the command
        self.__Write("CBDRT?")

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'CBDRT=<encodedBaud>\r\n'
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=5)

        # <encodedBaud> is a decimal value of the supported baud rates:
        #     00001 - 1 = 9600
        #     00010 - 2 = 19200
        #     00100 - 4 = 38400
        #     01000 - 8 = 57600
        #     10000 - 16 = 115200

        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized (this should not happen, if it does it is indicative of bad serial communication)
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'CBDRT=<encodedBaud>\r\n' then the command was recognized and the response is the current baud rate
        elif response[0:6] == b'CBDRT=':
            # Convert the response to a string
            response = response.decode()

            # Remove the \r\n from the response
            response = response.replace("\r\n", "")

            # Remove the CBDRT= from the response
            response = response.replace("CBDRT=", "")

            # Convert the response to an integer
            response = int(response)

            # Convert the response to a decimal value
            if response == 16:
                return 115200
            elif response == 8:
                return 57600
            elif response == 4:
                return 38400
            elif response == 2:
                return 19200
            elif response == 1:
                return 9600

    def SetCLClock(self, clock):
        """
        Sets the clock of the camera via (CLC) command.
        :param clock: The MHz of the clock to change to 85 MHz (0), 63.75 MHz (1), 42.5 MHz(2), 31.875 (3)
        :type clock: Enum/int (See: CLClockEnum)
        :return: "COMPLETE" if the clock was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # We are being extra cautious here and checking the type of the clock parameter to make sure it is an int or a CLClockEnum
        # If it is not an int or a CLClockEnum then raise a ValueError exception and do not send the command
        if not isinstance(clock, self.CLClockMHz) and isinstance(clock, int):
            # See if the integer value is a valid CLClockMHz Enum
            # This will throw a ValueError if the value is not a valid CLClockMHz Enum (and is intended to do so)
            clock = self.CLClockMHz(clock)
        if not isinstance(clock, self.CLClockMHz) and not isinstance(clock, int):
            raise ValueError(
                "The clock parameter must be an int or a CLClockEnum")

        # If the clock is already set to the desired clock then return "COMPLETE" and do not send the command
        if self.clock == clock:
            return "COMPLETE"

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=6``)
        self.__Write("CLC=" + str(clock.value)) # type: ignore

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'COMPLETE\r\n'
        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'COMPLETE\r\n' then the command was recognized and the clock was changed
        elif response == b'COMPLETE\r\n':
            # Update internal clock
            self.clock = clock
            return "COMPLETE"

    def GetCLClock(self):
        """
        Gets the clock of the camera via (CLC?) command.
        :return: The current clock of the camera in enum form or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: Enum (See CLClockMHz) or str
        """

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=6)
        self.__Write("CLC?")

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'CLC=<clock>\r\n'
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=6)

        # <clock> is a decimal value of the supported clocks:
        #     0 - 85 MHz
        #     1 - 63.75 MHz
        #     2 - 42.5 MHz
        #     3 - 31.875 MHz

        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized (this should not happen, if it does it is indicative of bad serial communication)
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'CLC=<clock>\r\n' then the command was recognized and the response is the current clock
        elif response[0:4] == b'CLC=':
            # Convert the response to a string
            response = response.decode()

            # Remove the \r\n from the response
            response = response.replace("\r\n", "")

            # Remove the CLC= from the response
            response = response.replace("CLC=", "")

            # Convert the response to an integer
            response = int(response)

            # Convert the response to a CLClockMHz Enum
            return self.CLClockMHz(response)

    def SetExposureMode(self, mode):
        """
        Sets the exposure mode of the camera via (EM) command.
        :param mode: The exposure mode to change to 0 (Off), 1 (Timed), or 2 (TriggerWidth)
        :type mode: Enum/int (See: ExposureMode)
        :return: "COMPLETE" if the exposure mode was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # We are being extra cautious here and checking the type of the mode parameter to make sure it is an int or a ExposureMode
        # If it is not an int or a ExposureMode then raise an exception and do not send the command
        if not isinstance(mode, self.ExposureMode) and isinstance(mode, int):
            # See if the integer value is a valid ExposureMode Enum
            # This will throw a ValueError if the integer value is not a valid ExposureMode Enum (and is intended to do so)
            mode = self.ExposureMode(mode)
        if not isinstance(mode, self.ExposureMode) and not isinstance(mode, int):
            raise ValueError(
                "The mode parameter must be an integer or a ExposureMode Enum")

        # If the exposure mode is already set to the desired exposure mode then return "COMPLETE" and do not send the command
        if self.exposureMode == mode:
            return "COMPLETE"

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)
        self.__Write("EM=" + str(mode.value))  # type: ignore

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'COMPLETE\r\n'
        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'COMPLETE\r\n' then the command was recognized and the exposure mode was changed
        elif response == b'COMPLETE\r\n':
            # Update internal exposure mode
            self.exposureMode = mode
            return "COMPLETE"

    def GetExposureMode(self):
        """
        Gets the exposure mode of the camera via (EM?) command.
        :return: The current exposure mode of the camera in enum form or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: Enum (See ExposureMode) or str
        """

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)
        self.__Write("EM?")

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'EM=<mode>\r\n'
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)

        # <mode> is a decimal value of the supported exposure modes:
        #     0 - Off
        #     1 - Timed
        #     2 - TriggerWidth

        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized (this should not happen, if it does it is indicative of bad serial communication)
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'EM=<mode>\r\n' then the command was recognized and the response is the current exposure mode
        elif response[0:3] == b'EM=':
            # Convert the response to a string
            response = response.decode()

            # Remove the \r\n from the response
            response = response.replace("\r\n", "")

            # Remove the EM= from the response
            response = response.replace("EM=", "")

            # Convert the response to an integer
            response = int(response)

            # Convert the response to a ExposureMode Enum
            return self.ExposureMode(response)

    def SetLineRate(self, rate):
        """
        Sets the line rate of the camera via (LR) command.
        :param rate: The line rate to change to 500 to 1515152
        :type rate: int
        :return: "COMPLETE" if the Line Rate was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # If the line rate is already set to the desired line rate then return "COMPLETE" and do not send the command
        if self.lineRate == rate:
            return "COMPLETE"

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)
        self.__Write("LR=" + str(rate))

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'COMPLETE\r\n'
        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'COMPLETE\r\n' then the command was recognized and the line rate was changed
        elif response == b'COMPLETE\r\n':
            # Update internal line rate
            self.lineRate = rate
            return "COMPLETE"

    def GetLineRate(self):
        """
        Gets the line rate of the camera via (LR?) command.
        :return: The current line rate of the camera or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: int or str
        """

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)
        self.__Write("LR?")

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'LR=<rate>\r\n'
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)

        # <rate> is a decimal value of the supported line rates:
        #     500 to 1515152

        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized (this should not happen, if it does it is indicative of bad serial communication)
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'LR=<rate>\r\n' then the command was recognized and the response is the current line rate
        elif response[0:3] == b'LR=':
            # Convert the response to a string
            response = response.decode()

            # Remove the \r\n from the response
            response = response.replace("\r\n", "")

            # Remove the LR= from the response
            response = response.replace("LR=", "")

            # Convert the response to an integer
            return int(response)

    def SetGainLevel(self, gain):
        """
        Sets the gain level of the camera via (GA) command.
        :param gain: The gain level to change to 100 to 6400
        :type gain: int
        :return: "COMPLETE" if the Gain Level was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # If the gain level is already set to the desired gain level then return "COMPLETE" and do not send the command
        if self.gainLevel == gain:
            return "COMPLETE"

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)
        self.__Write("GA=" + str(gain))

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'COMPLETE\r\n'
        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'COMPLETE\r\n' then the command was recognized and the gain level was changed
        elif response == b'COMPLETE\r\n':
            # Update internal gain level
            self.gainLevel = gain
            return "COMPLETE"

    def GetGainLevel(self):
        """
        Gets the gain level of the camera via (GA?) command.
        :return: The current gain level of the camera or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: int or str
        """

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)
        self.__Write("GA?")

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'GA=<gain>\r\n'
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)

        # <gain> is a decimal value of the supported gain levels:
        #     100 to 6400

        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized (this should not happen, if it does it is indicative of bad serial communication)
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'GA=<gain>\r\n' then the command was recognized and the response is the current gain level
        elif response[0:3] == b'GA=':
            # Convert the response to a string
            response = response.decode()

            # Remove the \r\n from the response
            response = response.replace("\r\n", "")

            # Remove the GA= from the response
            response = response.replace("GA=", "")

            # Convert the response to an integer
            return int(response)

    def SetAnalogBaseGain(self, dB):
        """
        Sets the analog base gain of the camera via (ABG) command.
        :param dB: The analog base gain to change to 0 (0dB), 1 (+6dB), 2 (+9.54dB), or 3 (+12dB)
        :type dB: Enum/int (See: AnalogBaseGain)
        :return: "COMPLETE" if the Analog Base Gain was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # We are being extra cautious here and checking the type of the mode parameter to make sure it is an int or a AnalogBaseGain
        # If it is not an int or a AnalogBaseGain then raise a ValueError exception and do not send the command
        if not isinstance(dB, self.AnalogBaseGainDB) and isinstance(dB, int):
            # See if the integer value is a valid AnalogBaseGain Enum
            # This will throw a ValueError if the integer value is not a valid AnalogBaseGain Enum (and is intended to do so)
            dB = self.AnalogBaseGainDB(dB)
        if not isinstance(dB, self.AnalogBaseGainDB) and not isinstance(dB, int):
            raise ValueError(
                "The dB parameter must be an int or a AnalogBaseGainDB Enum")

        # If the AnalogBaseGain dB is already set to the desired gain mode then return "COMPLETE" and do not send the command
        if self.analogBaseGain == dB:
            return "COMPLETE"

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)
        self.__Write("ABG=" + str(dB.value))  # type: ignore

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'COMPLETE\r\n'
        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'COMPLETE\r\n' then the command was recognized and the analog base gain was changed
        elif response == b'COMPLETE\r\n':
            # Update internal analog base gain
            self.analogBaseGain = dB
            return "COMPLETE"

    def GetAnalogBaseGain(self):
        """
        Gets the analog base gain of the camera via (ABG?) command.
        :return: The current analog base gain of the camera or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: Enum/int (See: AnalogBaseGain) or str
        """

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)
        self.__Write("ABG?")

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'ABG=<dB>\r\n'
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)

        # <dB> is a decimal value of the supported analog base gains:
        #     0 (0dB), 1 (+6dB), 2 (+9.54dB), or 3 (+12dB)

        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized (this should not happen, if it does it is indicative of bad serial communication)
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'ABG=<dB>\r\n' then the command was recognized and the response is the current analog base gain
        elif response[0:4] == b'ABG=':
            # Convert the response to a string
            response = response.decode()

            # Remove the \r\n from the response
            response = response.replace("\r\n", "")

            # Remove the ABG= from the response
            response = response.replace("ABG=", "")

            # Convert the response to an integer
            return AnalogBaseGain(int(response))

    def SetDeviceTapGeometry(self, geometry):
        """
        Sets the device tap geometry of the camera via (TAGM) command.
        :param geometry: The device tap geometry to change to 0 (Geometry_1X2_1Y), 1 (Geometry_1X3_1Y), 2 (Geometry_1X4_1Y), 3 (Geometry_1X8_1Y), or 4 (Geometry_1X10_1Y)
        :type geometry: Enum/int (See: DeviceTapGeometryEnum)
        :return: "COMPLETE" if the Device Tap Geometry was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # We are being extra cautious here and checking the type of the mode parameter to make sure it is an int or a DeviceTapGeometryEnum
        # If it is not an int or a DeviceTapGeometry then raise a ValueError exception and do not send the command
        if not isinstance(geometry, self.DeviceTapGeometryEnum) and isinstance(geometry, int):
            # See if the integer value is a valid DeviceTapGeometry Enum
            # This will throw a ValueError if the integer value is not a valid DeviceTapGeometryEnum entry (and is intended to do so)
            geometry = self.DeviceTapGeometryEnum(geometry)
        if not isinstance(geometry, self.DeviceTapGeometryEnum) and not isinstance(geometry, int):
            raise ValueError(
                "The geometry parameter must be an int or a DeviceTapGeometryEnum Enum")

        # If the DeviceTapGeometry geometry is already set to the desired geometry then return "COMPLETE" and do not send the command
        if self.deviceTapGeometry == geometry:
            return "COMPLETE"

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)
        self.__Write("TAGM=" + str(geometry.value))  # type: ignore

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'COMPLETE\r\n'
        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'COMPLETE\r\n' then the command was recognized and the device tap geometry was changed
        elif response == b'COMPLETE\r\n':
            # Update internal device tap geometry
            self.deviceTapGeometry = geometry
            return "COMPLETE"

    def GetDeviceTapGeometry(self):
        """
        Gets the device tap geometry of the camera via (TAGM?) command.
        :return: The current device tap geometry of the camera or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: Enum/int (See: DeviceTapGeometry) or str
        """

        # Send the command
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)
        self.__Write("TAGM?")

        # Read the Response
        response = self.__Read()

        # Expected Response Structure: b'TAGM=<geometry>\r\n'
        # (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)

        # <geometry> is a decimal value of the supported device tap geometries:
        #     0 (Geometry_1X2_1Y), 1 (Geometry_1X3_1Y), 2 (Geometry_1X4_1Y), 3 (Geometry_1X8_1Y), or 4 (Geometry_1X10_1Y)

        # If the response is b'01 Unknown Command!!\r\n' then the command was not recognized
        if response == b'01 Unknown Command!!\r\n':
            return "01 Unknown Command!!"
        # If the response is b'02 Bad Parameters!!\r\n' then the parameters were not recognized (this should not happen, if it does it is indicative of bad serial communication)
        elif response == b'02 Bad Parameters!!\r\n':
            return "02 Bad Parameters!!"
        # If the response is b'TAGM=<geometry>\r\n' then the command was recognized and the response is the current device tap geometry
        elif response[0:5] == b'TAGM=':
            # Convert the response to a string
            response = response.decode()

            # Remove the \r\n from the response
            response = response.replace("\r\n", "")

            # Remove the TAGM= from the response
            response = response.replace("TAGM=", "")

            # Convert the response to an integer
            return self.DeviceTapGeometryEnum(int(response))
