# <h1>Python implementation for Grab Demo</h1>
# <p>The code within this file contains an attempt at initializing the needed
#     classes to perform the functions from the Sapera SDK. This file is
#     intended to mimic how the grab demo initializes the components. The
#     variable names and function names are the same in this file and within the
#     grab demo.&nbsp;</p>
import sys
import clr

sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Demos/NET/GrabDemo/CSharp/bin/Debug")

clr.AddReference("SapNETCSharpGrabDemo")

from DALSA.SaperaLT.Demos.NET.CSharp.GrabDemo import *
from DALSA.SaperaLT.SapClassGui import *

grabDemo = GrabDemoDlg()

# <p>Attempt to call on click button function. This does end in an error, but it
#     proves that the function can be found &amp; called. To run without error
#     it just needs the correct arguments provided.</p>
#grabDemo.button_New_Click()

sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Components/NET/Bin")

clr.AddReference("DALSA.SaperaLT.SapClassBasic")
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import *
from DALSA.SaperaLT.SapClassBasic import *

# <p>This is the start of the <a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#GrabDemoDlg">GrabDemoDlg()</a>
#     function within the grab demo. This function is originally called from
#     Main() in <a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemo.cs">GrabDemo.cs</a>
# </p>

m_Acquisition = SapAcquisition()
m_Buffers = SapBuffer()
m_Xfer = SapAcqToBuf(m_Acquisition, m_Buffers)
m_View = SapView()
m_IsSignalDetected = True
m_ServerLocation = SapLocation()

# <p>AcqConfigDlg() is a function within the grab demo. It needs to be
#     determined if this function is fine as is called directly from the grab
#     functions dll, needs to be ported over to python, or for the values to be
#     hard coded.</p>
acConfigDlg = AcqConfigDlg(None, "", AcqConfigDlg.ServerCategory.ServerAcq)
if (acConfigDlg.ShowDialog() == DialogResult.OK):
    m_online = True
else:
    m_online = False
print(m_online)

num_servers = SapManager.GetServerCount(SapManager.ResourceType.Acq)
print(num_servers)


# <p>GrabDemoDlg() calls a function named <a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#CreateNewObjects1">CreateNewObjects()</a>.
#     This is the implementation of that function. There are errors within this
#     function due to trying to tryinig to use the create() function for
#     SapAcquisition() with no server. SapTransfer.Create() will also fail due
#     to SapAcquisition not creating successfully. SapAcquisition.Create() has
#     to be ran first and be successful for SapTransfer.Create() to succeed.</p>
def CreateNewObjects(acConfigDlg, Restore):
    global m_Acquisition
    global m_Buffers
    global m_Xfer
    global m_View
    global m_ServerLocation
    
    if (m_online):
        if (not Restore):
            m_ServerLocation = acConfigDlg.ServerLocation
            m_ConfigFileName = acConfigDlg.ConfigFile
        
        m_Acquisition = SapAcquisition(m_ServerLocation, m_ConfigFileName)
        print(m_ServerLocation)
        print(m_ConfigFileName)

        if (SapBuffer.IsBufferTypeSupported(m_ServerLocation, SapBuffer.MemoryType.ScatterGather)):
            m_Buffers = SapBufferWithTrash(2, m_Acquisition, SapBuffer.MemoryType.ScatterGather)
            print(1)
        else:
            m_Buffers = SapBufferWithTrash(2, m_Acquisition, SapBuffer.MemoryType.ScatterGatherPhysical)
            print(2)
        m_Xfer = SapAcqToBuf(m_Acquisition, m_Buffers)
        m_View = SapView(m_Buffers)
        print(m_Buffers.TrashType)
        print(m_Xfer)
        print(m_View)

        m_Xfer.Pairs[0].EventType = SapXferPair.XferEventType.EndOfFrame
        
        # <p>These Notify functions need to be looked further into to determine
        #     what needs to be added here.</p>
        #m_Xfer.XferNotify += SapXferNotifyHandler(grabDemo.xfer_XferNotify)
        #m_Xfer.XferNotifyContext = grabDemo
        

        #m_Acquisition.SignalNotify += SapSignalNotifyHandler(grabDemo.GetSignalStatus)
        #m_Acquisition.SignalNotifyContext = grabDemo
    else:
        m_Buffers = SapBuffer()
        m_View = SapView(m_Buffers)

    # <p>Within the first CreateNewObjects() function it calls another <a
    #         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#CreateNewObjects2">CreateNewObjects()</a>
    #     function.There are quite a few CreateNewObjects() functions within the
    #     grab demo due to function overloading. This is the start of the next
    #     function and where the errors occur.&nbsp;</p>
    if (m_Acquisition != None and not m_Acquisition.Initialized):
        if (m_Acquisition.Create() == False):
            print("m_Acquisition create failed")
        else:
            print("m_Acquisition create success")
    
    if (m_Buffers != None and not m_Buffers.Initialized):
        if (m_Buffers.Create() == False):
            print("m_Buffers create failed")
        else:
            print("m_Buffers create success")
    
    if (m_View != None and not m_View.Initialized):
        if (m_View.Create() == False):
            print("m_View create failed")
        else:
            print("m_View create success")
    
    if (m_Xfer != None and not m_Xfer.Initialized):
        if (m_Xfer.Create() == False):
            print("m_Xfer create failed")
        else:
            print("m_Xfer create success")
    
    # <p>Attempt to use the Grab function from SapTransfer(). This should be
    #     successful if m_Xfer can create successfully. It needs a server
    #     connection to create successfully so currently this function is
    #     failing also due to the unsuccessful create. As seen within the grab
    #     demo, this function Grab() can be used for the grab button. There are
    #     also functions under SapTransfer for Freeze and Snap that can be used
    #     for those buttons similar to how the grab demo is using them.</p>
    m_Xfer.Grab()
CreateNewObjects(acConfigDlg, False)

# <p>This function,<a
#         href="../Sapera-Demos/Net/GrabDemo/CSharp/GrabDemoDlg.cs#EnableSignalStatus">
#         EnableSignalStatus()</a>, is called from the first CreateNewObjects()
#     function within the grab demo.</p>
def EnableSignalStatus():
    if (m_Acquisition != None):
        print(m_Acquisition.SignalStatus)
        print(SapAcquisition.AcqSignalStatus(0))
        m_IsSignalDetected = (m_Acquisition.SignalStatus != (SapAcquisition.AcqSignalStatus(0)))
        if (not m_IsSignalDetected):
            print("Online... No camera signal detected")
        else:
            print("Online... camera signal detected")
        m_Acquisition.SignalNotifyEnable = True

EnableSignalStatus()



