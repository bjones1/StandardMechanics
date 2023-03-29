import serial

# Define Default Values
SerialPort = '/dev/pts/5'
BaudRate = 9600
DataLength = serial.EIGHTBITS
StopBit = serial.STOPBITS_ONE
Parity = serial.PARITY_NONE
XonXoff = serial.XOFF



# Command Functions
def GetSupportedBaudRates(serialHandle):
    # Get the Supported Baud Rates (Send: SBDRT?\r\n)
    serialHandle.write(b'SBDRT?\r\n')

    # Read the response until \r\n
    response = serialHandle.readline()

    # Get the Supported Baud Rates (Send: SBDRT?\r\n)
    # 11111
    # 11111 - 31 - 115200bps
    # 01111 - 15 - 57600bps
    # 00111 - 7 - 38400bps
    # 00011 - 3 - 19200bps
    # 00001 - 1 - 9600bps

    # Convert the response to an int
    print(response)
    response = int(response)

    # Parse the response
    if response>=1:
        print("9600bps Supported")
    if response>=3:
        print("19200bps Supported")
    if response>=7:
        print("38400bps Supported")
    if response>=15:
        print("57600bps Supported")
    if response==31:
        print("115200bps Supported")



def SetBaudRate(serialHandle, baudRate):
    # If baudRate is the same as the current baud rate, then do nothing
    if baudRate == BaudRate:
        return

    # Set the Baud Rate (Send: CBDRT=<baudRate>\r\n)
    # 10000 - 115200bps - 16
    # 01000 - 57600bps - 8
    # 00100 - 38400bps - 4
    # 00010 - 19200bps - 2
    # 00001 - 9600bps - 1

    baudRateParam = 1
    # Convert the baud rate to the correct value
    if baudRate == 115200:
        baudRateParam = 16
    elif baudRate == 57600:
        baudRateParam = 8
    elif baudRate == 38400:
        baudRateParam = 4
    elif baudRate == 19200:
        baudRateParam = 2
    elif baudRate == 9600:
        baudRateParam = 1

    # Send the command
    serialHandle.write(b'CBDRT=' + str(baudRateParam).encode() + b'\r\n')

    # Read the response until \r\n
    response = serialHandle.readline()

    # If the response is b'COMPLETE\r\n' then the baud rate was set and the serial port needs to be changed to the new baud rate
    if response == b'COMPLETE\r\n':
        # Serial Handle should now open at the new baud rate
        serialHandle.close()
        serialHandle.baudrate = baudRate
        serialHandle.open()

        # Send the command again for confirmation
        serialHandle.write(b'CBDRT=' + str(baudRateParam).encode() + b'\r\n')

        # Read the response until \r\n
        response = serialHandle.readline()

        if response == b'COMPLETE\r\n':
            print("Baud Rate Set")
        else:
            serialHandle.close()
            serialHandle.baudrate = BaudRate
            serialHandle.open()
            print("Baud Rate Not Set")

    elif response == b'01 Unknown Command!!\r\n':
        # The command was not recognized
        print("The command was not recognized")
    elif response == b'02 Bad Parameters!!\r\n':
        # The parameters were not recognized
        print("The parameters were not recognized")







if __name__ == "__main__":
    # Calling this automatically opens the serial port
    #                              Port        Baud      Bits      Parity  StopBits Timeout  XonXoff
    serialHandle = serial.Serial(SerialPort, BaudRate, DataLength, Parity, StopBit, None, XonXoff)

    GetSupportedBaudRates(serialHandle)
    SetBaudRate(serialHandle, 115200)
    GetSupportedBaudRates(serialHandle)

    # Close the serial port
    serialHandle.close()
