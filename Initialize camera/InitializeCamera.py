# Standard Libaray
import sys

# Third-party imports
import clr

sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Components/NET/Bin")

clr.AddReference("DALSA.SaperaLT.SapClassBasic")

from DALSA.SaperaLT.SapClassBasic import SapManager

num_servers = SapManager.GetServerCount(SapManager.ResourceType.Acq)
print(num_servers)