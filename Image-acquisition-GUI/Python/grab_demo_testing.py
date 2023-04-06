# <h1>Python implementation for Grab Demo</h1>
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

m_Acquisition = SapAcquisition()
m_Buffers = SapBuffer()
#m_Xfer = SapAcqToBuf()
m_View = SapView()
m_IsSignalDetected = True

acConfigDlg = AcqConfigDlg(None, "", AcqConfigDlg.ServerCategory.ServerAcq)
if (acConfigDlg.ShowDialog() == DialogResult.OK):
    m_online = True
else:
    m_online = False
print(m_online)

num_servers = SapManager.GetServerCount(SapManager.ResourceType.Acq)
print(num_servers)


m_ServerLocation = SapLocation()


