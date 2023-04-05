# <h1>Python implementation for Grab Demo</h1>
import sys
import clr

sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Demos/NET/GrabDemo/CSharp/bin/Debug")

clr.AddReference("SapNETCSharpGrabDemo")

from DALSA.SaperaLT.Demos.NET.CSharp.GrabDemo import *

grabDemo = GrabDemoDlg()

# <p>Attempt to call on click button function. This does end in an error, but it
#     proves that the function can be found &amp; called. To run without error
#     it just needs the correct arguments provided.</p>
grabDemo.button_New_Click()
