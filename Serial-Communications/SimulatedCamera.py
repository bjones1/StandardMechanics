import serial

# Define Default Values
SerialPort = '/dev/pts/6'
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

    # Print the response
    print(response)




lastCommand = b''
if __name__ == "__main__":
    # Calling this automatically opens the serial port
    #                              Port        Baud      Bits      Parity  StopBits Timeout  XonXoff
    serialHandle = serial.Serial(SerialPort, BaudRate, DataLength, Parity, StopBit, None, XonXoff)

    # Loop and read the serial port
    while True:
        # Read the serial port
        response = serialHandle.readline()
        # If the response is b'SBDRT?\r\n' then send the supported baud rates
        if response == b'SBDRT?\r\n':
            lastCommand = b'SBDRT?\r\n'
            # Get the Supported Baud Rates (Send: SBDRT?\r\n)
            # 11111
            # 11111 - 115200bps
            # 01111 - 57600bps
            # 00111 - 38400bps
            # 00011 - 19200bps
            # 00001 - 9600bps

            # Send the supported baud rates (Binary converted to Int)
            # 11111 - 31
            # 01111 - 15
            # 00111 - 7
            # 00011 - 3
            # 00001 - 1
            serialHandle.write(b'1\r\n')
        
        # If the response is CBDRT=<baudRate>\r\n then set the baud rate
        # where <baudRate> is an integer value between 1 and 16
        elif response[0:6] == b'CBDRT=':
            # Get the baud rate
            baudRate = int(response[6:])

            # 10000 - 115200bps - 16
            # 01000 - 57600bps - 8
            # 00100 - 38400bps - 4
            # 00010 - 19200bps - 2
            # 00001 - 9600bps - 1

            baudRateParam = 9600
            # Convert the baud rate to the correct value
            if baudRate == 16:
                baudRateParam = 115200
            elif baudRate == 8:
                baudRateParam = 57600
            elif baudRate == 4:
                baudRateParam = 38400
            elif baudRate == 2:
                baudRateParam = 19200
            elif baudRate == 1:
                baudRateParam = 9600
            else:
                print("Invalid Baud Rate: " + str(baudRate) + "bps")
                serialHandle.write(b'02 Bad Parameters!!\r\n')
                continue

            # COMPLETE COMMAND
            serialHandle.write(b'COMPLETE\r\n')

            serialHandle.close()
            serialHandle.baudrate = baudRateParam
            serialHandle.Timeout = 0.25
            serialHandle.open()

            response = serialHandle.readline()
            print(response)
            if response[0:6] == b'CBDRT=':
                # Get the baud rate
                baudRate = int(response[6:])

                # 10000 - 115200bps - 16
                # 01000 - 57600bps - 8
                # 00100 - 38400bps - 4
                # 00010 - 19200bps - 2
                # 00001 - 9600bps - 1

                baudRateParam2 = 9600
                # Convert the baud rate to the correct value
                if baudRate == 16:
                    baudRateParam2 = 115200
                elif baudRate == 8:
                    baudRateParam2 = 57600
                elif baudRate == 4:
                    baudRateParam2 = 38400
                elif baudRate == 2:
                    baudRateParam2 = 19200
                elif baudRate == 1:
                    baudRateParam2 = 9600
                else:
                    print("Invalid Baud Rate: " + str(baudRate) + "bps")
                    serialHandle.write(b'02 Bad Parameters!!\r\n')
                    continue
                
                if baudRateParam == baudRateParam2:
                    print("Baud Rate Confirmed")
                    serialHandle.close()
                    serialHandle.Timeout = None
                    serialHandle.open()
                    serialHandle.write(b'COMPLETE\r\n')
            else:
                print("Baud Rate not confirmed")
                serialHandle.close()
                serialHandle.baudrate = BaudRate
                serialHandle.Timeout = None
                serialHandle.open()
                continue



        print(response)


    # Close the serial port
    serialHandle.close()