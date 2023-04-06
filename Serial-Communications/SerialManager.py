# <h1>JAISerial Class</h1>
# <p>The purpose of this module (which currently only exports the JAISerial
#     class) is to fully facilitate communication with a <a
#         href="../datasheets/http:/localhost:8080/fs/home/kkonaog/Projects/School/StandardMechanics/datasheets/Datasheet_SW-4000M-PMCL_SW-8000M-PMCL.pdf">JAI
#         SW-4000M-PCL</a> camera via it's serial port protocol.<br>This program
#     operates under the assumption that direct access to the Camera's serial
#     port (COM port) is provided through the Sapera Configuration Tool. All
#     Commands implemented can be found in the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf">Command
#         List</a> datasheet.</p>
# <h2>Important Enumerations</h2>
# <p>It is the goal of the JAISerial class to provide streamlined access and
#     conversion of user commands and device responses, as such, a handful of
#     commands which take in a set number of parameters were provided quick
#     conversion enumerations.<br>Primarily, the goal is to provide any
#     overlaying programs a way to quickly understand the nature and "type" of a
#     return.</p>
# <h3 id="h_402237036916081680746737333">CommandResponse</h3>
# <p>Encodes the various standard responses from the camera (not including
#     unique command responses, such as those returned when getting a current
#     parameter's values.</p>
# <table style="border-collapse: collapse; width: 42.7817%; height: 84px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50%;">
#         <col style="width: 50%;">
#     </colgroup>
#     <tbody>
#         <tr>
#             <td>Enum</td>
#             <td>Value</td>
#         </tr>
#         <tr>
#             <td>CommandResponse.SUCCESS</td>
#             <td>b'COMPLETE\r\n'</td>
#         </tr>
#         <tr>
#             <td>CommandResponse.UNKNOWN_COMMAND</td>
#             <td>b'01 Unknown Command!!\r\n'</td>
#         </tr>
#         <tr>
#             <td>CommandResponse.BAD_PARAMETERS</td>
#             <td>b'02 Bad Parameters!!\r\n'</td>
#         </tr>
#     </tbody>
# </table>
# <h3 id="h_878246600650561680745303345">CLClockMHz</h3>
# <p>Encodes the valid parameters/returns (MHz) for the CL Clock</p>
# <table style="border-collapse: collapse; width: 42.7176%; height: 107px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50%;">
#         <col style="width: 50%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Enum</td>
#             <td style="height: 21px;">Value</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">CLClockMHz.MHZ_85</td>
#             <td style="height: 21px;">0 (85 MHz)</td>
#         </tr>
#         <tr style="height: 23px;">
#             <td style="height: 23px;">CLClockMHz.MHZ_63_75</td>
#             <td style="height: 23px;">1 (63.75 MHz)</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">CLClockMHz.MHZ_42_5</td>
#             <td style="height: 21px;">2 (42.5 MHz)</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">CLClockMHz.MHZ_31_875</td>
#             <td style="height: 21px;">3 (31.875 MHz)</td>
#         </tr>
#     </tbody>
# </table>
# <h3 id="h_378606409645151680745284696">ExposureMode</h3>
# <p>Encodes the valid parameters (mode) for the Exposure Mode</p>
# <table style="border-collapse: collapse; width: 42.5251%; height: 5px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50%;">
#         <col style="width: 50%;">
#     </colgroup>
#     <tbody>
#         <tr>
#             <td>Enum</td>
#             <td>Value</td>
#         </tr>
#         <tr>
#             <td>ExposureMode.OFF</td>
#             <td>0</td>
#         </tr>
#         <tr>
#             <td>ExposureMode.TIMED</td>
#             <td>1</td>
#         </tr>
#         <tr>
#             <td>ExposureMode.TRIGGER_WIDTH</td>
#             <td>2</td>
#         </tr>
#     </tbody>
# </table>
# <h3 id="h_217419339654671680745311753">AnalogBaseGainDB</h3>
# <p>Encodes the valid parameters/returns (dB) for Analog Base Gain</p>
# <table style="border-collapse: collapse; width: 42.461%; height: 105px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50%;">
#         <col style="width: 50%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Enum</td>
#             <td style="height: 21px;">Value</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">AnalogBaseGainDB.DB_0</td>
#             <td style="height: 21px;">0 (0 dB)</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">AnalogBaseGainDB.DB_6</td>
#             <td style="height: 21px;">1 (6 dB)</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">AnalogBaseGainDB.DB_9_54</td>
#             <td style="height: 21px;">2 (9 dB)</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">AnalogBaseGainDB.DB_12</td>
#             <td style="height: 21px;">3 (12 dB)</td>
#         </tr>
#     </tbody>
# </table>
# <h3 id="h_536232016660211680745320718">DeviceTapGeometryEnum</h3>
# <p>Encodes the valid parameters/returns (dB) for Device Tap Geometry</p>
# <table style="border-collapse: collapse; width: 42.6534%; height: 126px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0012%;">
#         <col style="width: 50.0012%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Enum</td>
#             <td style="height: 21px;">Value</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">DeviceTapGeometryEnum.GEOMETRY_1X2_1Y
#             </td>
#             <td style="height: 21px;">0</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">DeviceTapGeometryEnum.GEOMETRY_1X3_1Y
#             </td>
#             <td style="height: 21px;">1</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">DeviceTapGeometryEnum.GEOMETRY_1X4_1Y
#             </td>
#             <td style="height: 21px;">2</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">DeviceTapGeometryEnum.GEOMETRY_1X8_1Y
#             </td>
#             <td style="height: 21px;">3</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">DeviceTapGeometryEnum.GEOMETRY_1X10_1Y
#             </td>
#             <td style="height: 21px;">4</td>
#         </tr>
#     </tbody>
# </table>
# <h2>Implementation</h2>
# <p>The following is a breakdown of every function and its purpose in the
#     class. An important note in nomenclature is that functions prefixed with
#     "__" are not intended to be called by the user and may result in
#     unintended functionality. The only exception to this case may be the
#     __Close() function.</p>
# <h3 id="h_535242650676701680745558111">Constructor (__init__) - Parameters:
#     serialPort, baudRate, dataLength, stopBit, parity, XonXoff, and timeout
# </h3>
# <p>Initializes a JAI-4000M Serial Manager using the parameters provided and
#     initializes variables related to camera values.</p>
# <table style="border-collapse: collapse; width: 79.389%; height: 384px;"
#     border="1">
#     <colgroup>
#         <col style="width: 25.0409%;">
#         <col style="width: 25.0409%;">
#         <col style="width: 25.0409%;">
#         <col style="width: 24.9182%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#             <td style="height: 21px;">Purpose</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">serialPort</td>
#             <td style="height: 21px;">N/A</td>
#             <td style="height: 21px;">String (i.e "COM1")</td>
#             <td style="height: 21px;">Specifies to the serial port the camera
#                 is using.</td>
#         </tr>
#         <tr style="height: 39px;">
#             <td style="height: 39px;">baudRate</td>
#             <td style="height: 39px;">9600</td>
#             <td style="height: 39px;">Numerical (i.e 9600)</td>
#             <td style="height: 39px;">Specifies the baud rate to use, it
#                 should be the default baudrate or configured baudrate of the
#                 JAI camera.</td>
#         </tr>
#         <tr style="height: 57px;">
#             <td style="height: 57px;">dataLength</td>
#             <td style="height: 57px;">serial.EIGHTBITS</td>
#             <td style="height: 57px;"><a
#                     href="https://pyserial.readthedocs.io/en/latest/pyserial_api.html#constants"
#                     target="_blank" rel="noopener">PySerial Byte Size
#                     Constant</a></td>
#             <td style="height: 57px;">Specifies the number of bits used in
#                 communication, the camera documentation should specify this
#                 value. In the case of the JAI-4000M it is 8 bits. It is
#                 unlikely to change for a specific camera.</td>
#         </tr>
#         <tr style="height: 57px;">
#             <td style="height: 57px;">stopBit</td>
#             <td style="height: 57px;">serial.STOPBITS_ONE</td>
#             <td style="height: 57px;"><a
#                     href="https://pyserial.readthedocs.io/en/latest/pyserial_api.html#constants">PySerial
#                     Stop Bits Constant</a></td>
#             <td style="height: 57px;">Specifies the number of stop bits used
#                 in communication, the camera documentation should specify this
#                 value. In the case of the JAI-4000M it is 1 bit. It is
#                 unlikely to change for a specific camera.</td>
#         </tr>
#         <tr style="height: 57px;">
#             <td style="height: 57px;">parity</td>
#             <td style="height: 57px;">serial.PARITY_NONE</td>
#             <td style="height: 57px;"><a
#                     href="https://pyserial.readthedocs.io/en/latest/pyserial_api.html#constants">PySerial
#                     Parity Constant</a></td>
#             <td style="height: 57px;">Specifies the type of parity used in
#                 communication, the camera documentation should specify the
#                 type needed. In the case of the JAI-4000M there is no parity
#                 checking. It is unlikely to change for a specific camera.</td>
#         </tr>
#         <tr style="height: 57px;">
#             <td style="height: 57px;">XonXoff</td>
#             <td style="height: 57px;">False</td>
#             <td style="height: 57px;">True/False</td>
#             <td style="height: 57px;">Specifies where software flow control
#                 should be used. The camera should specify if it supports flow
#                 control, if it does not, it is safer to assume that XonXoff
#                 should be false. It is unlikely to change for a specific
#                 camera.</td>
#         </tr>
#         <tr style="height: 75px;">
#             <td style="height: 75px;">Timeout</td>
#             <td style="height: 75px;">None</td>
#             <td style="height: 75px;">Numerical (i.e 10) - Supports Decimal
#                 Values</td>
#             <td style="height: 75px;">Specifies how long in seconds that the
#                 serial port should wait for data to be read in when executing
#                 a read command. The special values of None means wait forever
#                 and 0 means return immediately (do not block). None is
#                 typically a safe value to use as it blocks execution until the
#                 desired response is received.</td>
#         </tr>
#     </tbody>
# </table>
# <p>The JAISerial class also maintains records of the following camera values:
# </p>
# <table style="border-collapse: collapse; width: 79.3709%; height: 147px;"
#     border="1">
#     <colgroup>
#         <col style="width: 49.993%;">
#         <col style="width: 49.993%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Camera Value</td>
#             <td style="height: 21px;">Initialization Value (Camera Default
#                 Values)</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Line Rate</td>
#             <td style="height: 21px;">500</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">CL Clock</td>
#             <td style="height: 21px;"><a
#                     href="#h_878246600650561680745303345">CLClockMHz</a>.MHZ_85
#             </td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Exposure Mode</td>
#             <td style="height: 21px;"><a
#                     href="#h_378606409645151680745284696">ExposureMode</a>.TIMED
#             </td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Gain Level</td>
#             <td style="height: 21px;">100</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Analog Base Gain</td>
#             <td style="height: 21px;"><a
#                     href="#h_217419339654671680745311753">AnalogBaseGainDB</a>.DB_0
#             </td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Device Tap Geometry</td>
#             <td style="height: 21px;"><a
#                     href="#h_536232016660211680745320718">DeviceTapGeometryEnum</a>.GEOMETRY_1X4_1Y
#             </td>
#         </tr>
#     </tbody>
# </table>
# <p>The variables themselves are not intended to be modified by user and
#     instead&nbsp;are used as a means of preventing sending duplicate commands
#     to the camera. I.e, if Gain Level is 100, and a command to set the Gain
#     Level to 100 is sent then it is pre-empted and returns with
#     CommandResponse.SUCCESS immediately.&nbsp;The values are automatically
#     updated by their respective set commands when they return a success
#     response.</p>
# <p>The constructor automatically calls the PySerial Open Function for the
#     provided Serial Port and saves its handle to serialHandle via the <a
#         href="#h_665820432673031680745512639">__Open()</a> class function.</p>
# <p>&nbsp;</p>
# <h3 id="h_665820432673031680745512639">__Open - Parameters: None</h3>
# <p>This function is intended to be called internally by the class and uses the
#     serial port information provided in the <a
#         href="#h_535242650676701680745558111">Constructor </a>to open a valid
#     handle to the serial port. There is currently no error handling on this
#     call, the PySerial Exception for the port already being open should be
#     expected in the event it is already open.</p>
# <p>&nbsp;</p>
# <h3 id="h_372104307764331680745945889">__Close - Parameters: None</h3>
# <p>This function is intended to be called internally by the class and takes
#     the serial handle created in&nbsp;<a
#         href="#h_665820432673031680745512639">__Open</a> and closes it. If
#     __Close is called before the serial handle is defined in <a
#         href="#h_665820432673031680745512639">__Open</a> then it has a value
#     of (None) and raises the exception: Exception("__Close(self) accessed
#     before __Open(self)")</p>
# <h3>&nbsp;</h3>
# <h3 id="h_7570723211110561680747826655">__ChangeBaudRate - Parameters:
#     BaudRate</h3>
# <table style="border-collapse: collapse; width: 47.3468%; height: 18px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0003%;">
#         <col style="width: 25.0001%;">
#         <col style="width: 25.0001%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#         </tr>
#         <tr>
#             <td>BaudRate</td>
#             <td>N/A</td>
#             <td>A valid baudrate for the camera. (See&nbsp; the <a
#                     href="#h_878216019820031680746292219">GetSupportedBaudRate
#                 </a>function)</td>
#         </tr>
#     </tbody>
# </table>
# <p>This function is intended to be called internally by the class when the <a
#         href="#h_450954177824291680746297297">SetBaudRate </a>function gets a
#     success response from the camera. In the event __ChangeBaudRate is called
#     before the serial handle is opened by <a
#         href="#h_665820432673031680745512639">__Open</a> it raises the
#     exception: Exception("__ChangeBaudRate(self, baudRate) accessed before
#     __Open(self)")<br>If the serial handle is valid, then the function closes
#     the serial handle (<a href="#h_372104307764331680745945889">__Close</a>),
#     modifies the current baudrate, and re-opens (<a
#         href="#h_665820432673031680745512639">__Open</a>) the serial handle at
#     the specified baud rate.&nbsp;&nbsp;</p>
# <p>&nbsp;</p>
# <h3 id="h_115052218953281680747095090">__Write - Parameters: command</h3>
# <table style="border-collapse: collapse; width: 47.3468%; height: 60px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0003%;">
#         <col style="width: 25.0001%;">
#         <col style="width: 25.0001%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#         </tr>
#         <tr style="height: 39px;">
#             <td style="height: 39px;">Command</td>
#             <td style="height: 39px;">N/A</td>
#             <td style="height: 39px;">A string command to send to the camera.
#                 Valid Commands are listed in the <a
#                     href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf"
#                     target="_blank" rel="noopener">Command List</a> datasheet.
#             </td>
#         </tr>
#     </tbody>
# </table>
# <p>This function is intended to be called internally by the class and takes in
#     a simplified string version of a valid commands. (I.e CBDRT=2). It
#     automatically converts the string into a byte array and appends the needed
#     line terminators: "\r\n". If __Write is called before the serial handle is
#     opened by <a href="#h_665820432673031680745512639">__Open</a> it raises
#     the exception: Exception("__Write(self) accessed before __Open(self)").
#     There is no "valid command" checking at this level<br>the camera is
#     responsible for responding with a <a
#         href="#h_402237036916081680746737333">CommandResponse</a>.UNKNOWN_COMMAND
#     or <a
#         href="#h_402237036916081680746737333">CommandResponse</a>.BAD_PARAMETERS
#     response.</p>
# <p>&nbsp;</p>
# <h3>__Read - Parameters: None</h3>
# <p>This function is intended to be called internally by the class and returns
#     the response provided. If will wait for the amount of time specified by
#     the timeout provided in the <a
#         href="#h_535242650676701680745558111">Constructor.</a> If the Timeout
#     is None, then the __Read function can block forever until a full line of
#     data (\n) is received across the serial port. If __Read is called before
#     the serial handle is opened by <a
#         href="#h_665820432673031680745512639">__Open</a> it raises the
#     exception:&nbsp;Exception("__Read(self) accessed before __Open(self)")</p>
# <p>&nbsp;</p>
# <h3 id="h_878216019820031680746292219">GetSupportedBaudRates - Parameters:
#     None</h3>
# <p>Queries the camera for its supported baudrates and returns an array
#     containing the valid baudrates in ascending order. In the event the
#     response is not understood, it will return its matching <a
#         href="#h_402237036916081680746737333">CommandResponse</a>, otherwise
#     it will raise an exception: Exception("Unexpected response from camera: "
#     + response.decode())<br>Internally, this works by using <a
#         href="#h_115052218953281680747095090">__Write </a>to send "SBRDT?" as
#     specified by the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=5">Command
#         List</a> datasheet. The response of this command is a hex value
#     representing the binary value of supported baudrates. In our instance, the
#     exact binary response is not important so it is converted to decimal
#     values.</p>
# <table style="border-collapse: collapse; width: 77.6964%; height: 126px;"
#     border="1">
#     <colgroup>
#         <col style="width: 25.0086%;">
#         <col style="width: 25.0086%;">
#         <col style="width: 49.9829%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Hex Value</td>
#             <td style="height: 21px;">Decimal</td>
#             <td style="height: 21px;">Baud Rates</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">0x01</td>
#             <td style="height: 21px;">1</td>
#             <td style="height: 21px;">9600</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">0x03</td>
#             <td style="height: 21px;">3</td>
#             <td style="height: 21px;">9600, 19200</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">0x07</td>
#             <td style="height: 21px;">7</td>
#             <td style="height: 21px;">9600, 19200, 38400</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">0x0F</td>
#             <td style="height: 21px;">15</td>
#             <td style="height: 21px;">9600, 19200, 38400, 57600</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">0x1F</td>
#             <td style="height: 21px;">31</td>
#             <td style="height: 21px;">9600, 19200, 38400, 57600, 115200</td>
#         </tr>
#     </tbody>
# </table>
# <p>It is currently unknown if the Hex Value returned by the camera will
#     include the leadings 0s on smaller values. I.e 0x01 or 0x1. The code works
#     around this by removing the known portions of the command and sending the
#     rest into the <a
#         href="https://docs.python.org/3/library/functions.html#int">int</a>
#     data type with the base set to 16. This conversion method should handle
#     both cases of 0x01 or 0x1 with a valid return.</p>
# <p>&nbsp;</p>
# <h3 id="h_450954177824291680746297297">SetBaudRate - Parameters: BaudRate</h3>
# <table style="border-collapse: collapse; width: 77.5938%; height: 12px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0441%;">
#         <col style="width: 25%;">
#         <col style="width: 24.9559%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">BaudRate</td>
#             <td style="height: 21px;">N/A</td>
#             <td style="height: 21px;">A valid baud rate returned by <a
#                     href="#h_878216019820031680746292219">GetSupportedBaudRates</a>
#             </td>
#         </tr>
#     </tbody>
# </table>
# <p>Attempts to set the camera baud rate following
#     the&nbsp;<em><strong>special</strong></em><strong>&nbsp;</strong>process
#     laid out on page 4 of the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=4">Command
#         List</a>. This results in a call to <a
#         href="#h_7570723211110561680747826655">__ChangeBaudRate </a>if
#     successful. If the baudRate sent into the function is equal to the current
#     baudRate then <a
#         href="#h_402237036916081680746737333">CommandResponse</a>.SUCCESS is
#     immediately returned. The encoding used by SetBaudRate seems to be a
#     little weird as it could be hex or decimal. In our testing, sending in
#     decimal values seemed to work.<br>The encoding is 1 hot binary of the
#     supported baudrates in decimal.</p>
# <table style="border-collapse: collapse; width: 70.5833%; height: 148px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0171%;">
#         <col style="width: 25.0086%;">
#         <col style="width: 24.9743%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Baud Rate</td>
#             <td style="height: 21px;">Decimal Value</td>
#             <td style="height: 21px;">Binary</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">9600</td>
#             <td style="height: 21px;">1</td>
#             <td style="height: 21px;">00001</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">19200</td>
#             <td style="height: 21px;">2</td>
#             <td style="height: 21px;">00010</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">38400</td>
#             <td style="height: 21px;">4</td>
#             <td style="height: 21px;">00100</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">57600</td>
#             <td style="height: 21px;">8</td>
#             <td style="height: 21px;">01000</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">115200</td>
#             <td style="height: 21px;">16</td>
#             <td style="height: 21px;">10000</td>
#         </tr>
#     </tbody>
# </table>
# <p>After completing this conversion SetBaudRate uses&nbsp;<a
#         href="#h_115052218953281680747095090">__Write</a> to send
#     "CBDRT=&lt;encodedBaudRate&gt;" as specified in the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=5">Command
#         List</a>. The return is one of the <a
#         href="#h_402237036916081680746737333">CommandResponse</a> responses
#     or, if none match the response, then it raises the
#     exception:&nbsp;Exception("Unexpected response from camera: " +
#     response.decode())</p>
# <p>&nbsp;</p>
# <h3>GetBaudRate - Parameters: None</h3>
# <p>Queries the camera for its current baudrate and returns it as an integer
#     value (9600, 19200, etc.). &nbsp;In the event the response is not
#     understood, it will return its matching <a
#         href="#h_402237036916081680746737333">CommandResponse</a>, otherwise
#     it will raise an exception: Exception("Unexpected response from camera: "
#     + response.decode())<br>Internally, this works by using <a
#         href="#h_115052218953281680747095090">__Write </a>to send "CBDRT?" as
#     specified by the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=5">Command
#         List</a> datasheet. The response of this command is a decimal value
#     representing the binary value of supported baudrates.</p>
# <table style="border-collapse: collapse; width: 70.5833%; height: 148px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0171%;">
#         <col style="width: 25.0086%;">
#         <col style="width: 24.9743%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Baud Rate</td>
#             <td style="height: 21px;">Decimal Value</td>
#             <td style="height: 21px;">Binary</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">9600</td>
#             <td style="height: 21px;">1</td>
#             <td style="height: 21px;">00001</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">19200</td>
#             <td style="height: 21px;">2</td>
#             <td style="height: 21px;">00010</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">38400</td>
#             <td style="height: 21px;">4</td>
#             <td style="height: 21px;">00100</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">57600</td>
#             <td style="height: 21px;">8</td>
#             <td style="height: 21px;">01000</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">115200</td>
#             <td style="height: 21px;">16</td>
#             <td style="height: 21px;">10000</td>
#         </tr>
#     </tbody>
# </table>
# <h3>&nbsp;</h3>
# <h3>SetCLClock - Parameters: clock</h3>
# <table style="border-collapse: collapse; width: 77.5938%; height: 42px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0441%;">
#         <col style="width: 25%;">
#         <col style="width: 24.9559%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">clock</td>
#             <td style="height: 21px;">N/A</td>
#             <td style="height: 21px;">A valid clock specified in&nbsp;<a
#                     href="#h_878246600650561680745303345">CLClockMHz</a></td>
#         </tr>
#     </tbody>
# </table>
# <p>The parameter is verified to be an instance of (a value in) <a
#         href="#h_878246600650561680745303345">CLClockMHz</a>&nbsp;or an
#     integer value that can be converted to an instance of <a
#         href="#h_878246600650561680745303345">CLClockMHz</a>. If the
#     conversion is not possible a ValueError exception is raised:
#     ValueError("The geometry parameter must be an int or a AnalogBaseGainDB
#     Enum") After completing this conversion SetCLClock uses&nbsp;<a
#         href="#h_115052218953281680747095090">__Write</a> to send
#     "CLC=&lt;clock&gt;" as specified in the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=6">Command
#         List</a>. The return is one of the&nbsp;<a
#         href="#h_402237036916081680746737333">CommandResponse</a> responses
#     or, if none match the response, then it raises the exception:
#     Exception("Unexpected response from camera: " + response.decode()).</p>
# <p>&nbsp;</p>
# <h3>GetCLClock - Parameters: None</h3>
# <p>Queries the camera for its CL Clock and returns it as an instance of <a
#         href="#h_878246600650561680745303345">CLClockMHz</a>. In the event the
#     response is not understood, it will return its matching <a
#         href="#h_402237036916081680746737333">CommandResponse</a>, otherwise
#     it will raise an exception: Exception("Unexpected response from camera: "
#     + response.decode())<br>Internally, this works by using <a
#         href="#h_115052218953281680747095090">__Write</a> to send "CLC?" as
#     specified by the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=6">Command
#         List</a> datasheet. The response of this command is an integer value
#     that can be converted to a <a
#         href="#h_878246600650561680745303345">CLClockMHz</a>.</p>
# <p>&nbsp;</p>
# <h3>SetExposureMode - Parameters: mode</h3>
# <table style="border-collapse: collapse; width: 77.5938%; height: 42px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0441%;">
#         <col style="width: 25%;">
#         <col style="width: 24.9559%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">mode</td>
#             <td style="height: 21px;">N/A</td>
#             <td style="height: 21px;">A valid mode specified in&nbsp;<a
#                     href="#h_378606409645151680745284696">ExposureMode</a>
#             </td>
#         </tr>
#     </tbody>
# </table>
# <p>The parameter is verified to be an instance of (a value in) <a
#         href="#h_378606409645151680745284696">ExposureMode</a>&nbsp;or an
#     integer value that can be converted to an instance of <a
#         href="#h_378606409645151680745284696">ExposureMode</a>. If the
#     conversion is not possible a ValueError exception is raised:
#     ValueError("The geometry parameter must be an int or a AnalogBaseGainDB
#     Enum") After completing this conversion SetExposureMode uses&nbsp;<a
#         href="#h_115052218953281680747095090">__Write</a> to send
#     "EM=&lt;mode&gt;" as specified in the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=7">Command
#         List</a>. The return is one of the&nbsp;<a
#         href="#h_402237036916081680746737333">CommandResponse</a> responses
#     or, if none match the response, then it raises the exception:
#     Exception("Unexpected response from camera: " + response.decode()).</p>
# <p>&nbsp;</p>
# <h3>GetExposureMode - Parameters: mode</h3>
# <p>Queries the camera for its Exposure Mode and returns it as an instance of
#     <a href="#h_378606409645151680745284696">ExposureMode</a>. In the event
#     the response is not understood, it will return its matching <a
#         href="#h_402237036916081680746737333">CommandResponse</a>, otherwise
#     it will raise an exception: Exception("Unexpected response from camera: "
#     + response.decode())<br>Internally, this works by using <a
#         href="#h_115052218953281680747095090">__Write</a> to send "EM?" as
#     specified by the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=7">Command
#         List</a> datasheet. The response of this command is an integer value
#     that can be converted to a <a
#         href="#h_378606409645151680745284696">ExposureMode</a>.</p>
# <p>&nbsp;</p>
# <h3>SetLineRate - Parameters: rate</h3>
# <table style="border-collapse: collapse; width: 77.5938%; height: 60px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0441%;">
#         <col style="width: 25%;">
#         <col style="width: 24.9559%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#         </tr>
#         <tr style="height: 39px;">
#             <td style="height: 39px;">rate</td>
#             <td style="height: 39px;">N/A</td>
#             <td style="height: 39px;">An integer value between 500 to 1515152
#             </td>
#         </tr>
#     </tbody>
# </table>
# <p>The parameter in this instance is not verified to be within the range 500
#     to 1515152. SetLineRate uses&nbsp;<a
#         href="#h_115052218953281680747095090">__Write</a> to send
#     "LR=&lt;rate&gt;" as specified in the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=7">Command
#         List</a>. The return is one of the&nbsp;<a
#         href="#h_402237036916081680746737333">CommandResponse</a> responses
#     or, if none match the response, then it raises the exception:
#     Exception("Unexpected response from camera: " + response.decode()).</p>
# <p>&nbsp;</p>
# <h3>GetLineRate - Parameters: None</h3>
# <p>Queries the camera for its Line Rate and returns it as an integer. In the
#     event the response is not understood, it will return its matching&nbsp;<a
#         href="#h_402237036916081680746737333">CommandResponse</a>, otherwise
#     it will raise an exception: Exception("Unexpected response from camera: "
#     + response.decode())<br>Internally, this works by using <a
#         href="#h_115052218953281680747095090">__Write</a> to send "LR?" as
#     specified by the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=7">Command
#         List</a> datasheet. The response of this command is an integer value.
# </p>
# <p>&nbsp;</p>
# <h3>SetGainLevel - Parameters: Level</h3>
# <table style="border-collapse: collapse; width: 77.5938%; height: 42px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0441%;">
#         <col style="width: 25%;">
#         <col style="width: 24.9559%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">level</td>
#             <td style="height: 21px;">N/A</td>
#             <td style="height: 21px;">An integer value between 100 to 6400
#             </td>
#         </tr>
#     </tbody>
# </table>
# <p>&nbsp;The parameter in this instance is not verified to be within the range
#     100 to 6400. SetGainLevel uses <a
#         href="#h_115052218953281680747095090">__Write</a> to send
#     "GA=&lt;level&gt;" as specified in the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=9">Command
#         List</a>. The return is one of the&nbsp;<a
#         href="#h_402237036916081680746737333">CommandResponse</a> responses
#     or, if none match the response, then it raises the exception:
#     Exception("Unexpected response from camera: " + response.decode()).</p>
# <p>&nbsp;</p>
# <h3>GetGainLevel - Parameters: None</h3>
# <p>Queries the camera for its Gain and returns it as an integer. In the event
#     the response is not understood, it will return its matching <a
#         href="#h_402237036916081680746737333">CommandResponse</a>, otherwise
#     it will raise an exception: Exception("Unexpected response from camera: "
#     + response.decode())<br>Internally, this works by using <a
#         href="#h_115052218953281680747095090">__Write</a> to send "GA?" as
#     specified by the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=9">Command
#         List</a> datasheet. The response of this command is an integer value.
# </p>
# <p>&nbsp;</p>
# <h3>SetAnalogBaseGain- Parameters: dB</h3>
# <table style="border-collapse: collapse; width: 77.5938%; height: 42px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0441%;">
#         <col style="width: 25%;">
#         <col style="width: 24.9559%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">dB</td>
#             <td style="height: 21px;">N/A</td>
#             <td style="height: 21px;">A valid dB specified in <a
#                     href="#h_217419339654671680745311753">AnalogBaseGainDB</a>
#             </td>
#         </tr>
#     </tbody>
# </table>
# <p>The parameter is verified to be an instance of (a value in) <a
#         href="#h_217419339654671680745311753">AnalogBaseGainDB </a>or an
#     integer value that can be converted to an instance of <a
#         href="#h_217419339654671680745311753">AnalogBaseGainDB</a>. If the
#     conversion is not possible a ValueError exception is raised:
#     ValueError("The geometry parameter must be an int or a AnalogBaseGainDB
#     Enum") After completing this conversion SetAnalogBaseGain uses&nbsp;<a
#         href="#h_115052218953281680747095090">__Write</a> to send
#     "ABG=&lt;dB&gt;" as specified in the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=9">Command
#         List</a>. The return is one of the&nbsp;<a
#         href="#h_402237036916081680746737333">CommandResponse</a> responses
#     or, if none match the response, then it raises the exception:
#     Exception("Unexpected response from camera: " + response.decode()).</p>
# <p>&nbsp;</p>
# <h3>GetAnalogBaseGain- Parameters: None</h3>
# <p>Queries the camera for its Analog Base Gain and returns it as an instance
#     of&nbsp;<a href="#h_217419339654671680745311753">AnalogBaseGainDB</a>. In
#     the event the response is not understood, it will return its matching <a
#         href="#h_402237036916081680746737333">CommandResponse</a>, otherwise
#     it will raise an exception: Exception("Unexpected response from camera: "
#     + response.decode())<br>Internally, this works by using <a
#         href="#h_115052218953281680747095090">__Write</a> to send "ABG?" as
#     specified by the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=9">Command
#         List</a> datasheet. The response of this command is an integer value
#     that can be converted to a <a
#         href="#h_217419339654671680745311753">AnalogBaseGainDB</a>.</p>
# <p>&nbsp;</p>
# <h3>SetDeviceTapGeometry - Parameters: geometry</h3>
# <table style="border-collapse: collapse; width: 77.5938%; height: 12px;"
#     border="1">
#     <colgroup>
#         <col style="width: 50.0441%;">
#         <col style="width: 25%;">
#         <col style="width: 24.9559%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Parameter Name</td>
#             <td style="height: 21px;">Default Value</td>
#             <td style="height: 21px;">Intended Values</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Geometry</td>
#             <td style="height: 21px;">N/A</td>
#             <td style="height: 21px;">A valid geometry specified in <a
#                     href="#h_536232016660211680745320718">DeviceTapGeometryEnum</a>
#             </td>
#         </tr>
#     </tbody>
# </table>
# <p>The parameter is verified to be an instance of (a value in) <a
#         href="#h_536232016660211680745320718">DeviceTapGeometryEnum</a> or an
#     integer value that can be converted to an instance of <a
#         href="#h_536232016660211680745320718">DeviceTapGeometryEnum</a>. If
#     the conversion is not possible a ValueError exception is raised:
#     ValueError("The geometry parameter must be an int or a
#     DeviceTapGeometryEnum Enum")&nbsp;After completing this conversion
#     SetDeviceTapGeometry uses&nbsp;<a
#         href="#h_115052218953281680747095090">__Write</a> to send
#     "TAGM=&lt;geometry&gt;" as specified in the <a
#         href="../datasheets/Command-List-SW-4000M8000M-PMCL.pdf#page=9">Command
#         List</a>. The return is one of the&nbsp;<a
#         href="#h_402237036916081680746737333">CommandResponse</a> responses
#     or, if none match the response, then it raises the exception:
#     Exception("Unexpected response from camera: " + response.decode()).</p>
# <p>&nbsp;</p>
# <h3>GetDeviceTapGeometry - Parameters: None</h3>
# <p>Queries the camera for its current tap geometry and returns it as an
#     instance of <a
#         href="#h_536232016660211680745320718">DeviceTapGeometryEnum</a>. In
#     the event the response is not understand, it will return its matching <a
#         href="#h_402237036916081680746737333">CommandResponse</a>, otherwise
#     it will raise an exception: Exception("Unexpected response from camera: "
#     + response.decode())<br>Internally, this works by using <a
#         href="#h_115052218953281680747095090">__Write</a> to send "TAGM?" as
#     specified by the <a
#         href="../datasheets//Command-List-SW-4000M8000M-PMCL.pdf#page=9">Command
#         List</a> datasheet. The response of this command is an integer value
#     that can be converted to a <a
#         href="#h_536232016660211680745320718">DeviceTapGeometryEnum</a>.</p>
# <p>&nbsp;</p>
# <h2>Python Imports</h2>
# <table style="border-collapse: collapse; width: 80.0172%; height: 81px;"
#     border="1">
#     <colgroup>
#         <col style="width: 33.4095%;">
#         <col style="width: 33.4095%;">
#         <col style="width: 33.178%;">
#     </colgroup>
#     <tbody>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Import&nbsp;</td>
#             <td style="height: 21px;">Library</td>
#             <td style="height: 21px;">Purpose</td>
#         </tr>
#         <tr style="height: 39px;">
#             <td style="height: 39px;">serial</td>
#             <td style="height: 39px;"><a
#                     href="https://pypi.org/project/pyserial/">PySerial</a>
#             </td>
#             <td style="height: 39px;">Standard Library for connecting to a
#                 computer's serial ports across multiple operating systems
#                 using uniform commands</td>
#         </tr>
#         <tr style="height: 21px;">
#             <td style="height: 21px;">Enum</td>
#             <td style="height: 21px;"><a
#                     href="https://docs.python.org/3/library/enum.html">enum</a>
#             </td>
#             <td style="height: 21px;">Python's Standard Implementation for
#                 Enumerations</td>
#         </tr>
#     </tbody>
# </table>
# <p>&nbsp;</p>
import serial  # pip install pyserial
from enum import Enum

#


class JAISerial:
    class CommandResponse(Enum):
        """
        The Command Status Enum is an Enum that contains the possible returns for the set command.
        """
        # <p>Command was successful</p>
        SUCCESS = b'COMPLETE\r\n'
        # <p>Command was unsuccessful due to an invalid command</p>
        UNKNOWN_COMMAND = b'01 Unknown Command!!\r\n'
        # <p>Command was unsuccessful due to an invalid parameter</p>
        BAD_PARAMETERS = b'02 Bad Parameters!!\r\n'

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

#
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
        self.XonXoff = XonXoff

        #
        self.lineRate = 500  # 500 lines per second (Camera Default)
        self.CCLK = self.CLClockMHz.MHZ_85  # 85 MHz (Camera Default)
        self.exposureMode = self.ExposureMode.TIMED  # Timed (Camera Default)
        self.gainLevel = 100  # 100 (Camera Default)
        #
        # 0dB (Camera Default)
        self.analogBaseGain = self.AnalogBaseGainDB.DB_0
        #
        # 1x4 (Camera Default)
        self.deviceTapGeometry = self.DeviceTapGeometryEnum.GEOMETRY_1X4_1Y

        self.serialHandle = None
        self.__Open()

    def __Open(self):
        """
        Opens the serial port, this is called when the class is initialized and when the baud rate is changed, it is intended to be used internally and should not be called directly by the user.
        """

        self.serialHandle = serial.Serial(
            self.serialPort, self.baudRate, self.dataLength, self.parity, self.stopBit, self.timeout, self.XonXoff)

    def __Close(self):
        """
        Closes the serial port, this is called when the baud rate is changed and when the class is destroyed, it is intended to be used internally and should not be called directly by the user.
        """

        if self.serialHandle is None:
            raise Exception("__Close(self) accessed before __Open(self)")

        self.serialHandle.close()

    def __ChangeBaudRate(self, baudRate):
        """
        Changes the baud rate of the serial port, this is called when the baud rate is changed by SetBaudRate, it is intended to be used internally and should not be called directly by the user.

        :param baudRate: The baud rate to change to in decimal (9600, 19200, 38400, 57600, 115200)
        :type baudRate: int
        """

        if self.serialHandle is None:
            raise Exception(
                "__ChangeBaudRate(self, baudRate) accessed before __Open(self)")

        self.__Close()
        self.serialHandle.baudrate = baudRate
        self.__Open()

    def __Write(self, command):
        """
        Writes a command to the serial port, it is intended to be used internally and should not be called directly by the user.

        :param command: The command to send to the serial port (ex. "CBDRT=1")
        :type command: str
        """
        # <p>Theoretically, serialHandle should not be None, but just in case it
        #     is, this will Raise an Exception</p>
        if self.serialHandle is None:
            raise Exception("__Write(self) accessed before __Open(self)")

        # <p>The command is encoded to a byte array and then a carriage return
        #     and line feed are added in accordance with the JAI Serial Protocol
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=3)</p>
        self.serialHandle.write(command.encode() + b'\r\n')

    def __Read(self):
        """
        Reads a response from the serial port, it is intended to be used internally and should not be called directly by the user. This function will block until a response is received or the timeout (see class constructor) is reached.
        """

        # <p>Theoretically, serialHandle should not be None, but just in case it
        #     is, this will Raise an Exception</p>
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

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=5)</p>
        self.__Write("SBDRT?")

        # <p>Read the Response</p>
        response = self.__Read()

        # <p>Expected Response Structure: b'SBDRT=\r\n'
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=5) Where
        #     HexBaud is a hex value of the supported baud rates: 00001 - 0x01 =
        #     9600 00011 - 0x03 = 19200 00111 - 0x07 = 38400 01111 - 0x0F =
        #     57600 11111 - 0x1F = 115200</p>

        # <p>If the response is b'01 Unknown Command!!\r\n' then the command was
        #     not recognized</p>
        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case _:
                # <p>If the response is not b'01 Unknown Command!!\r\n' then the
                #     command was recognized Check if the response is the
                #     expected length</p>
                if response[0:6] == b'SBDRT=':
                    # <p>Convert the response to a string</p>
                    response = response.decode()

                    # <p>I cannot confirm that the return includes leading
                    #     zeros, so instead I will find \r\n and remove it (more
                    #     reliable) Alternatively I was going to do something
                    #     similar to response = response[6:10] but I am not sure
                    #     if the return will always be 4 characters</p>
                    response = response.replace("\r\n", "")

                    # <p>Remove the SBDRT= from the response</p>
                    response = response.replace("SBDRT=", "")

                    # <p>Convert the response to an integer (base 16, accounts
                    #     for both 0x01 and 0x1, etc.)</p>
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
                else:
                    raise Exception(
                        "Unexpected response from camera: " + response.decode())

    def SetBaudRate(self, baudRate):
        """
        Sets the baud rate of the camera via (CBDRT) command.
        :param baudRate: The baud rate to change to in decimal (9600, 19200, 38400, 57600, 115200)
        :type baudRate: int
        :return: "COMPLETE" if the baud rate was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!, FAILED)
        :rtype: str
        """

        # <p>If the baud rate is already set to the desired baud rate then
        #     return "COMPLETE", do not send the command again self.baudRate is
        #     maintained by the class and is updated when the baud rate is
        #     changed</p>
        if baudRate == self.baudRate:
            return self.CommandResponse.SUCCESS

        # <p>Note: Need to confirm if baudRate needs to be decimal or hex This
        #     only supports decimal values for now (seemed to work in testing
        #     session with Trey Leonard)
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=5)</p>
        encodedBaudRate = 1  # 9600 by default

        if baudRate == 115200:
            encodedBaudRate = 16
        elif baudRate == 57600:
            encodedBaudRate = 8
        elif baudRate == 38400:
            encodedBaudRate = 4
        elif baudRate == 19200:
            encodedBaudRate = 2

        # <p>Send the command</p>
        self.__Write("CBDRT=" + str(encodedBaudRate))

        # <p>Read the Response</p>
        response = self.__Read()

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case self.CommandResponse.SUCCESS.value:
                # <p>If the response is b'COMPLETE\r\n' then the command was
                #     recognized and the baud rate was changed We must execute a
                #     confirmation command once the baud rate is changed to
                #     verify we are still communicating with the camera This
                #     protocol is described in the datasheet
                #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=4)
                # </p>
                self.__ChangeBaudRate(baudRate)
                self.__Write("CBDRT=" + str(encodedBaudRate))
                response = self.__Read()
                if response == self.CommandResponse.SUCCESS.value:
                    # <p>Update the baud rate</p>
                    self.baudRate = baudRate
                    return self.CommandResponse.SUCCESS
                else:
                    self.__ChangeBaudRate(9600)
                    raise Exception(
                        "Unexpected response from camera: " + response.decode())
            case _:
                raise Exception(
                    "Unexpected response from camera: " + response.decode())

    def GetBaudRate(self):
        """
        Gets the baud rate of the camera via (CBDRT?) command.
        :return: The current baud rate of the camera in decimal form or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: int or str
        """

        # <p>Send the command</p>
        self.__Write("CBDRT?")

        # <p>Read the Response</p>
        response = self.__Read()

        # <p>Expected Response Structure: b'CBDRT=\r\n'
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=5)</p>

        # <p>is a decimal value of the supported baud rates: 00001 - 1 = 9600
        #     00010 - 2 = 19200 00100 - 4 = 38400 01000 - 8 = 57600 10000 - 16 =
        #     115200</p>

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case _:
                # <p>If the response is not b'01 Unknown Command!!\r\n' then the
                #     command was recognized</p>
                if response[0:6] == b'CBDRT=':
                    # <p>Convert the response to a string</p>
                    response = response.decode()

                    # <p>Remove the \r\n from the response</p>
                    response = response.replace("\r\n", "")

                    # <p>Remove the CBDRT= from the response</p>
                    response = response.replace("CBDRT=", "")

                    # <p>Convert the response to an integer</p>
                    response = int(response)

                    # <p>Convert the response to a decimal value</p>
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
                else:
                    raise Exception(
                        "Unexpected response from camera: " + response.decode())

    def SetCLClock(self, clock):
        """
        Sets the clock of the camera via (CLC) command.
        :param clock: The MHz of the clock to change to 85 MHz (0), 63.75 MHz (1), 42.5 MHz(2), 31.875 (3)
        :type clock: Enum/int (See: CLClockEnum)
        :return: "COMPLETE" if the clock was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # <p>We are being extra cautious here and checking the type of the clock
        #     parameter to make sure it is an int or a CLClockEnum If it is not
        #     an int or a CLClockEnum then raise a ValueError exception and do
        #     not send the command</p>
        if not isinstance(clock, self.CLClockMHz) and isinstance(clock, int):
            # <p>See if the integer value is a valid CLClockMHz Enum This will
            #     throw a ValueError if the value is not a valid CLClockMHz Enum
            #     (and is intended to do so)</p>
            clock = self.CLClockMHz(clock)
        if not isinstance(clock, self.CLClockMHz) and not isinstance(clock, int):
            raise ValueError(
                "The clock parameter must be an int or a CLClockEnum")

        # <p>If the clock is already set to the desired clock then return
        #     "COMPLETE" and do not send the command</p>
        if self.clock == clock:
            return self.CommandResponse.SUCCESS

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=6``)</p>
        self.__Write("CLC=" + str(clock.value))  # type: ignore

        # <p>Read the Response</p>
        response = self.__Read()

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case self.CommandResponse.SUCCESS.value:
                # <p>If the response is b'COMPLETE\r\n' then the command was
                #     recognized and the clock was changed Update internal clock
                # </p>
                self.clock = clock
                return self.CommandResponse.SUCCESS
            case _:
                raise Exception(
                    "Unexpected response from camera: " + response.decode())

    def GetCLClock(self):
        """
        Gets the clock of the camera via (CLC?) command.
        :return: The current clock of the camera in enum form or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: Enum (See CLClockMHz) or str
        """

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=6)</p>
        self.__Write("CLC?")

        # <p>Read the Response</p>
        response = self.__Read()

        # <p>Expected Response Structure: b'CLC=\r\n'
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=6)</p>

        # <p>is a decimal value of the supported clocks: 0 - 85 MHz 1 - 63.75
        #     MHz 2 - 42.5 MHz 3 - 31.875 MHz</p>

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case _:
                # <p>If the response is not b'01 Unknown Command!!\r\n' then the
                #     command was recognized</p>
                if response[0:4] == b'CLC=':
                    # <p>Convert the response to a string</p>
                    response = response.decode()

                    # <p>Remove the \r\n from the response</p>
                    response = response.replace("\r\n", "")

                    # <p>Remove the CLC= from the response</p>
                    response = response.replace("CLC=", "")

                    # <p>Convert the response to an integer</p>
                    response = int(response)

                    # <p>Convert the response to a CLClockMHz Enum</p>
                    return self.CLClockMHz(response)
                else:
                    raise Exception(
                        "Unexpected response from camera: " + response.decode())

    def SetExposureMode(self, mode):
        """
        Sets the exposure mode of the camera via (EM) command.
        :param mode: The exposure mode to change to 0 (Off), 1 (Timed), or 2 (TriggerWidth)
        :type mode: Enum/int (See: ExposureMode)
        :return: "COMPLETE" if the exposure mode was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # <p>We are being extra cautious here and checking the type of the mode
        #     parameter to make sure it is an int or a ExposureMode If it is not
        #     an int or a ExposureMode then raise an exception and do not send
        #     the command</p>
        if not isinstance(mode, self.ExposureMode) and isinstance(mode, int):
            # <p>See if the integer value is a valid ExposureMode Enum This will
            #     throw a ValueError if the integer value is not a valid
            #     ExposureMode Enum (and is intended to do so)</p>
            mode = self.ExposureMode(mode)
        if not isinstance(mode, self.ExposureMode) and not isinstance(mode, int):
            raise ValueError(
                "The mode parameter must be an integer or a ExposureMode Enum")

        # <p>If the exposure mode is already set to the desired exposure mode
        #     then return "COMPLETE" and do not send the command</p>
        if self.exposureMode == mode:
            return self.CommandResponse.SUCCESS

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)</p>
        self.__Write("EM=" + str(mode.value))  # type: ignore

        # <p>Read the Response</p>
        response = self.__Read()

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case self.CommandResponse.SUCCESS.value:
                # <p>If the response is b'COMPLETE\r\n' then the command was
                #     recognized and the exposure mode was changed Update
                #     internal exposure mode</p>
                self.exposureMode = mode
                return self.CommandResponse.SUCCESS
            case _:
                raise Exception(
                    "Unexpected response from camera: " + response.decode())

    def GetExposureMode(self):
        """
        Gets the exposure mode of the camera via (EM?) command.
        :return: The current exposure mode of the camera in enum form or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: Enum (See ExposureMode) or str
        """

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)</p>
        self.__Write("EM?")

        # <p>Read the Response</p>
        response = self.__Read()

        # <p>Expected Response Structure: b'EM=\r\n'
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)</p>

        # <p>is a decimal value of the supported exposure modes: 0 - Off 1 -
        #     Timed 2 - TriggerWidth</p>

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case _:
                # <p>If the response is not b'01 Unknown Command!!\r\n' then the
                #     command was recognized</p>
                if response[0:3] == b'EM=':
                    # <p>Convert the response to a string</p>
                    response = response.decode()

                    # <p>Remove the \r\n from the response</p>
                    response = response.replace("\r\n", "")

                    # <p>Remove the EM= from the response</p>
                    response = response.replace("EM=", "")

                    # <p>Convert the response to an integer</p>
                    response = int(response)

                    # <p>Convert the response to a ExposureMode Enum</p>
                    return self.ExposureMode(response)
                else:
                    raise Exception(
                        "Unexpected response from camera: " + response.decode())

    def SetLineRate(self, rate):
        """
        Sets the line rate of the camera via (LR) command.
        :param rate: The line rate to change to 500 to 1515152
        :type rate: int
        :return: "COMPLETE" if the Line Rate was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # <p>If the line rate is already set to the desired line rate then
        #     return "COMPLETE" and do not send the command</p>
        if self.lineRate == rate:
            return self.CommandResponse.SUCCESS

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)</p>
        self.__Write("LR=" + str(rate))

        # <p>Read the Response</p>
        response = self.__Read()

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case self.CommandResponse.SUCCESS.value:
                # <p>If the response is b'COMPLETE\r\n' then the command was
                #     recognized and the line rate was changed Update internal
                #     line rate</p>
                self.lineRate = rate
                return self.CommandResponse.SUCCESS
            case _:
                raise Exception(
                    "Unexpected response from camera: " + response.decode())

    def GetLineRate(self):
        """
        Gets the line rate of the camera via (LR?) command.
        :return: The current line rate of the camera or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: int or str
        """

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)</p>
        self.__Write("LR?")

        # <p>Read the Response</p>
        response = self.__Read()

        # <p>Expected Response Structure: b'LR=\r\n'
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=7)</p>

        # <p>is a decimal value of the supported line rates: 500 to 1515152</p>

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case _:
                # <p>If the response is not b'01 Unknown Command!!\r\n' then the
                #     command was recognized</p>
                if response[0:3] == b'LR=':
                    # <p>Convert the response to a string</p>
                    response = response.decode()

                    # <p>Remove the \r\n from the response</p>
                    response = response.replace("\r\n", "")

                    # <p>Remove the LR= from the response</p>
                    response = response.replace("LR=", "")

                    # <p>Convert the response to an integer</p>
                    return int(response)
                else:
                    raise Exception(
                        "Unexpected response from camera: " + response.decode())

    def SetGainLevel(self, gain):
        """
        Sets the gain level of the camera via (GA) command.
        :param gain: The gain level to change to 100 to 6400
        :type gain: int
        :return: "COMPLETE" if the Gain Level was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # <p>If the gain level is already set to the desired gain level then
        #     return "COMPLETE" and do not send the command</p>
        if self.gainLevel == gain:
            return self.CommandResponse.SUCCESS

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)</p>
        self.__Write("GA=" + str(gain))

        # <p>Read the Response</p>
        response = self.__Read()

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case self.CommandResponse.SUCCESS.value:
                # <p>If the response is b'COMPLETE\r\n' then the command was
                #     recognized and the gain level was changed Update internal
                #     gain level</p>
                self.gainLevel = gain
                return self.CommandResponse.SUCCESS
            case _:
                raise Exception(
                    "Unexpected response from camera: " + response.decode())

    def GetGainLevel(self):
        """
        Gets the gain level of the camera via (GA?) command.
        :return: The current gain level of the camera or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: int or str
        """

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)</p>
        self.__Write("GA?")

        # <p>Read the Response</p>
        response = self.__Read()

        # <p>Expected Response Structure: b'GA=\r\n'
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)</p>

        # <p>is a decimal value of the supported gain levels: 100 to 6400</p>

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case _:
                # <p>If the response is not b'01 Unknown Command!!\r\n' then the
                #     command was recognized</p>
                if response[0:3] == b'GA=':
                    response = response.decode()

                    # <p>Remove the \r\n from the response</p>
                    response = response.replace("\r\n", "")

                    # <p>Remove the GA= from the response</p>
                    response = response.replace("GA=", "")

                    # <p>Convert the response to an integer</p>
                    return int(response)
                else:
                    raise Exception(
                        "Unexpected response from camera: " + response.decode())

    def SetAnalogBaseGain(self, dB):
        """
        Sets the analog base gain of the camera via (ABG) command.
        :param dB: The analog base gain to change to 0 (0dB), 1 (+6dB), 2 (+9.54dB), or 3 (+12dB)
        :type dB: Enum/int (See: AnalogBaseGain)
        :return: "COMPLETE" if the Analog Base Gain was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # <p>We are being extra cautious here and checking the type of the mode
        #     parameter to make sure it is an int or a AnalogBaseGain If it is
        #     not an int or a AnalogBaseGain then raise a ValueError exception
        #     and do not send the command</p>
        if not isinstance(dB, self.AnalogBaseGainDB) and isinstance(dB, int):
            # <p>See if the integer value is a valid AnalogBaseGain Enum This
            #     will throw a ValueError if the integer value is not a valid
            #     AnalogBaseGain Enum (and is intended to do so)</p>
            dB = self.AnalogBaseGainDB(dB)
        if not isinstance(dB, self.AnalogBaseGainDB) and not isinstance(dB, int):
            raise ValueError(
                "The dB parameter must be an int or a AnalogBaseGainDB Enum")

        # <p>If the AnalogBaseGain dB is already set to the desired gain mode
        #     then return "COMPLETE" and do not send the command</p>
        if self.analogBaseGain == dB:
            return self.CommandResponse.SUCCESS

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)</p>
        self.__Write("ABG=" + str(dB.value))  # type: ignore

        # <p>Read the Response</p>
        response = self.__Read()

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case self.CommandResponse.SUCCESS.value:
                # <p>If the response is b'COMPLETE\r\n' then the command was
                #     recognized and the analog base gain was changed Update
                #     internal analog base gain</p>
                self.analogBaseGain = dB
                return self.CommandResponse.SUCCESS
            case _:
                raise Exception(
                    "Unexpected response from camera: " + response.decode())

    def GetAnalogBaseGain(self):
        """
        Gets the analog base gain of the camera via (ABG?) command.
        :return: The current analog base gain of the camera or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: Enum/int (See: AnalogBaseGain) or str
        """

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)</p>
        self.__Write("ABG?")

        # <p>Read the Response</p>
        response = self.__Read()

        # <p>Expected Response Structure: b'ABG=\r\n'
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)</p>

        # <p>is a decimal value of the supported analog base gains: 0 (0dB), 1
        #     (+6dB), 2 (+9.54dB), or 3 (+12dB)</p>

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case _:
                # <p>If the response is not b'01 Unknown Command!!\r\n' then the
                #     command was recognized</p>
                if response[0:4] == b'ABG=':
                    # <p>Convert the response to a string</p>
                    response = response.decode()

                    # <p>Remove the \r\n from the response</p>
                    response = response.replace("\r\n", "")

                    # <p>Remove the ABG= from the response</p>
                    response = response.replace("ABG=", "")

                    # <p>Convert the response to an integer</p>
                    return self.AnalogBaseGainDB(int(response))
                else:
                    raise Exception(
                        "Unexpected response from camera: " + response.decode())

    def SetDeviceTapGeometry(self, geometry):
        """
        Sets the device tap geometry of the camera via (TAGM) command.
        :param geometry: The device tap geometry to change to 0 (Geometry_1X2_1Y), 1 (Geometry_1X3_1Y), 2 (Geometry_1X4_1Y), 3 (Geometry_1X8_1Y), or 4 (Geometry_1X10_1Y)
        :type geometry: Enum/int (See: DeviceTapGeometryEnum)
        :return: "COMPLETE" if the Device Tap Geometry was changed successfully or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: str
        """

        # <p>We are being extra cautious here and checking the type of the mode
        #     parameter to make sure it is an int or a DeviceTapGeometryEnum If
        #     it is not an int or a DeviceTapGeometry then raise a ValueError
        #     exception and do not send the command</p>
        if not isinstance(geometry, self.DeviceTapGeometryEnum) and isinstance(geometry, int):
            # <p>See if the integer value is a valid DeviceTapGeometry Enum This
            #     will throw a ValueError if the integer value is not a valid
            #     DeviceTapGeometryEnum entry (and is intended to do so)</p>
            geometry = self.DeviceTapGeometryEnum(geometry)
        if not isinstance(geometry, self.DeviceTapGeometryEnum) and not isinstance(geometry, int):
            raise ValueError(
                "The geometry parameter must be an int or a DeviceTapGeometryEnum Enum")

        # <p>If the DeviceTapGeometry geometry is already set to the desired
        #     geometry then return "COMPLETE" and do not send the command</p>
        if self.deviceTapGeometry == geometry:
            return self.CommandResponse.SUCCESS

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)</p>
        self.__Write("TAGM=" + str(geometry.value))  # type: ignore

        # <p>Read the Response</p>
        response = self.__Read()

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case self.CommandResponse.SUCCESS.value:
                # <p>If the response is b'COMPLETE\r\n' then the command was
                #     recognized and the device tap geometry was changed Update
                #     internal device tap geometry</p>
                self.deviceTapGeometry = geometry
                return self.CommandResponse.SUCCESS
            case _:
                raise Exception(
                    "Unexpected response from camera: " + response.decode())

    def GetDeviceTapGeometry(self):
        """
        Gets the device tap geometry of the camera via (TAGM?) command.
        :return: The current device tap geometry of the camera or an error message (01 Unknown Command!!, 02 Bad Parameters!!)
        :rtype: Enum/int (See: DeviceTapGeometry) or str
        """

        # <p>Send the command
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)</p>
        self.__Write("TAGM?")

        # <p>Read the Response</p>
        response = self.__Read()

        # <p>Expected Response Structure: b'TAGM=\r\n'
        #     (datasheets\Command-List-SW-4000M8000M-PMCL.pdf#page=9)</p>

        # <p>is a decimal value of the supported device tap geometries: 0
        #     (Geometry_1X2_1Y), 1 (Geometry_1X3_1Y), 2 (Geometry_1X4_1Y), 3
        #     (Geometry_1X8_1Y), or 4 (Geometry_1X10_1Y)</p>

        match response:
            case self.CommandResponse.UNKNOWN_COMMAND.value:
                return self.CommandResponse.UNKNOWN_COMMAND
            case self.CommandResponse.BAD_PARAMETERS.value:
                return self.CommandResponse.BAD_PARAMETERS
            case _:
                # <p>If the response is not b'01 Unknown Command!!\r\n' then the
                #     command was recognized</p>
                if response[0:5] == b'TAGM=':
                    # <p>Convert the response to a string</p>
                    response = response.decode()

                    # <p>Remove the \r\n from the response</p>
                    response = response.replace("\r\n", "")

                    # <p>Remove the TAGM= from the response</p>
                    response = response.replace("TAGM=", "")

                    # <p>Convert the response to an integer</p>
                    return self.DeviceTapGeometryEnum(int(response))
                else:
                    raise Exception(
                        "Unexpected response from camera: " + response.decode())
