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

# <p>Add the Sapera .dlls to the Path</p>
sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Components/NET/Bin")

# <p>We can reference the SapClassBasic and the Windows built-in forms to access
#     everything we should need.</p>
clr.AddReference("DALSA.SaperaLT.SapClassBasic")
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import *
from DALSA.SaperaLT.SapClassBasic import *

# <p>Here, we instantiate the .NET variables to use to define the acquisition
# </p>
m_Acquisition = SapAcquisition()
m_Buffers = SapBuffer()
#m_Xfer = SapAcqToBuf()
m_View = SapView()
m_IsSignalDetected = True

# <p>This acConfigDlg reads config settings, shows the dialogue window</p>
acConfigDlg = AcqConfigDlg(None, "", AcqConfigDlg.ServerCategory.ServerAcq)
dialog_result = acConfigDlg.ShowDialog()
print(dialog_result)
# <p>Set m_online based on if the Dialog populated correctly. This should work
#     if the Sapera server exists</p>
if (dialog_result == DialogResult.OK):
    m_online = True
else:
    m_online = False
print(m_online)

num_servers = SapManager.GetServerCount(SapManager.ResourceType.Acq)
print(num_servers)

m_ServerLocation = SapLocation()

# <p>Most buttons in the dialogue operate based on m_Xfer to determine how/when
#     to use them.</p>
# <p>The Line-scan/Area-scan buttons instead operate directly off of
#     m_Acquisition, and are only populated in the C++ version of the library.
# </p>
# <p>It would be possible to instantiate these buttons too, except that the
#     dialogues they would need to populate do not exist in the common C#
#     library of the demos.</p>
# <p>Creating the Linescan option seems to require writing a C# dialogue for
#     that</p>
