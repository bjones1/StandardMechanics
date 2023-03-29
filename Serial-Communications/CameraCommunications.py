import serial

# <p>Define Default Values</p>
SerialPort = '/dev/pts/5'
BaudRate = 9600
DataLength = serial.EIGHTBITS
StopBit = serial.STOPBITS_ONE
Parity = serial.PARITY_NONE
XonXoff = serial.XOFF



# <p>Command Functions</p>
def GetSupportedBaudRates(serialHandle):
    # <p>Get the Supported Baud Rates (Send: SBDRT?\r\n)</p>
    serialHandle.write(b'SBDRT?\r\n')

    # <p>Read the response until \r\n</p>
    response = serialHandle.readline()

    # <p>11111 11111 - 31 - 115200bps&nbsp;</p>
    # <p>01111 - 15 - 57600bps</p>
    # <p>00111 - 7 - 38400bps</p>
    # <p>00011 - 3 - 19200bps</p>
    # <p>00001 - 1 - 9600bps</p>

    # <p>Convert the response to an int</p>
    print(response)
    response = int(response)

    # <p>Parse the response</p>
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
    # <p>If baudRate is the same as the current baud rate, then do nothing</p>
    if baudRate == BaudRate:
        return

    # <p>Set the Baud Rate (Send: CBDRT=\r\n)</p>
    # <p>10000 - 115200bps - 16</p>
    # <p>01000 - 57600bps - 8</p>
    # <p>00100 - 38400bps - 4</p>
    # <p>00010 - 19200bps - 2</p>
    # <p>00001 - 9600bps - 1</p>

    baudRateParam = 1
    # <p>Convert the baud rate to the correct value</p>
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

    # <p>Send the command</p>
    serialHandle.write(b'CBDRT=' + str(baudRateParam).encode() + b'\r\n')

    # <p>Read the response until \r\n</p>
    response = serialHandle.readline()

    # <p>If the response is b'COMPLETE\r\n' then the baud rate was set and the
    #     serial port needs to be changed to the new baud rate</p>
    if response == b'COMPLETE\r\n':
        # <p>Serial Handle should now open at the new baud rate</p>
        serialHandle.close()
        serialHandle.baudrate = baudRate
        serialHandle.open()

        # <p>Send the command again for confirmation</p>
        serialHandle.write(b'CBDRT=' + str(baudRateParam).encode() + b'\r\n')

        # <p>Read the response until \r\n</p>
        response = serialHandle.readline()

        if response == b'COMPLETE\r\n':
            print("Baud Rate Set")
        else:
            serialHandle.close()
            serialHandle.baudrate = BaudRate
            serialHandle.open()
            print("Baud Rate Not Set")

    elif response == b'01 Unknown Command!!\r\n':
        # <p>The command was not recognized</p>
        print("The command was not recognized")
    elif response == b'02 Bad Parameters!!\r\n':
        # <p>The parameters were not recognized</p>
        print("The parameters were not recognized")







if __name__ == "__main__":
    # <p>Calling this automatically opens the serial port</p>
    serialHandle = serial.Serial(SerialPort, BaudRate, DataLength, Parity, StopBit, None, XonXoff)

    GetSupportedBaudRates(serialHandle)
    SetBaudRate(serialHandle, 115200)
    GetSupportedBaudRates(serialHandle)

    # <p>Close the serial port</p>
    serialHandle.close()
