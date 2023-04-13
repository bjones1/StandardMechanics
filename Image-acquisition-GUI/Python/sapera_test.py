# <h1>Python implementation</h1>
# <p>This demonstrates using <a
#         href="https://pythonnet.github.io/pythonnet/">Python.NET</a> to gain
#     easy access to the Sapera LT .NET API. To use this:</p>
# <ul>
#     <li>Install Python.</li>
#     <li>Install the <a
#             href="https://www.teledynedalsa.com/en/products/imaging/vision-software/sapera-lt/download/">Sapera
#             SDK</a>.</li>
#     <li><a
#             href="https://pythonnet.github.io/pythonnet/python.html#installation">Install
#             Python.NET</a>, using <code>pip install pythonnet</code>. (I
#         recommend doing this in a <a
#             href="https://docs.python.org/3/library/venv.html">Python virtual
#             environment</a>; here's a <a
#             href="https://realpython.com/python-virtual-environments-a-primer/">tutorial</a>.)
#     </li>
#     <li>Run this program.</li>
# </ul>
# <h2>Imports</h2>
# <div>
#     <div>These are listed in the order prescribed by <a
#             href="http://www.python.org/dev/peps/pep-0008/#imports">PEP 8</a>.
#     </div>
#     <div>
#         <div>
#             <h3>Standard library</h3>
#         </div>
#     </div>
# </div>
import sys
# <div>
#     <h3>Third-party imports</h3>
# </div>
import clr

# <p>Add the path to Sapera .NET libraries. Update this if you installed
#     the&nbsp;<a
#         href="https://www.teledynedalsa.com/en/products/imaging/vision-software/sapera-lt/download/">Sapera
#         SDK</a> in some other location. Per Python.NET's <a
#         href="https://pythonnet.github.io/pythonnet/python.html#importing-modules">importing
#         modules docs</a>, any .NET modules to be imported should be added to
#     the Python path.</p>
sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Components/NET/Bin")

# <p>Per the same docs, add a reference to assembly, so we can import them.</p>
clr.AddReference("DALSA.SaperaLT.SapClassBasic")

# <p>Now, we can import the Sapera .NET libraries. Per <a
#         href="../Sapera.NET.pdf#page=14" target="_blank" rel="noopener">these
#         docs</a>, the namespace for all the Sapera libraries is
#     <code>DALSA.SaperaLT.SapClassBasic</code>.</p>
from DALSA.SaperaLT.SapClassBasic import SapManager

from DALSA.SaperaLT.SapClassBasic import SapAcquisition

# <p>After the import, simply call functions. The following code would probably
#     be ported from the existing C#/C++ code. Here, the initialization sequence
#     in the existing code begins by looking for servers (frame grabbers) to
#     talk to. This just demonstrates that these functions work, but doesn't do
#     (much) useful work.</p>
num_servers = SapManager.GetServerCount(SapManager.ResourceType.Acq)
print(num_servers)

#print(dir(SapAcquisition.Prm))
#print(SapAcquisition.Prm.ACQ_DEVICE_INDEX)
print(SapAcquisition.Val)
#print(dir(SapAcquisition.Val))
print(SapAcquisition.Val.ACTIVE_HIGH)
print(SapAcquisition.Val.INTERFACE_DIGITAL)
#print(SapAcquisition.Val.DECIMATE_EVEN)
#val = SapAcquisition.Val()
#print(SapAcquisition.GetParameterType(SapAcquisition.Prm.ACQ_DEVICE_INDEX))
#result = SapAcquisition.GetParameter(SapAcquisition.Prm.ACQ_DEVICE_INDEX, id(val))
#print(result, val)
print(SapAcquisition.SaveParameters("params.txt"))
