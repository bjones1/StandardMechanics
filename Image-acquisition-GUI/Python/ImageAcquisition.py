import sys
import os
import clr

sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Demos/NET/GrabDemo/CSharp/bin/Debug")
sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Components/NET/Bin")
clr.AddReference("SapNETCSharpGrabDemo")
clr.AddReference("DALSA.SaperaLT.SapClassBasic")
clr.AddReference("System.Windows.Forms")

from DALSA.SaperaLT.SapClassGui import *
from DALSA.SaperaLT.SapClassBasic import SapManager, SapAcquisition, SapBuffer, SapAcqToBuf, SapLocation, SapBufferWithTrash, SapAcqDeviceToBuf, SapXferPair, SapView


class ImageAcquisitionManager():
    # Device Configuration
    m_ServerName = None
    m_ConfigFile = os.getcwd() + "/JAI_SW-4000M.ccf"
    m_ServerIndex = 0
    m_ResourceIndex = 0
    m_ServerLocation = SapLocation()

    m_Acquisition = SapAcquisition()
    m_Buffers = SapBuffer()
    m_Xfer = SapAcqToBuf(m_Acquisition, m_Buffers)
    m_View = SapView(m_Buffers)
    m_IsSignalDetected = True

    def __init__(self):
        # Dr. Leonard specified we could assume configuration file defaults.
        # We know we are interfacing with a Frame-Grabber, this replaces the functionality of the previous AcqConfigDlg
        # The default server location is 0, this may need to be changed after testing to whatever the Frame Grabber reports as

        didAcquireServer = SapManager.GetResourceCount(
            self.m_ServerIndex, SapManager.ResourceType.Acq) > 0
        if (didAcquireServer):
            self.m_ServerName = SapManager.GetServerName(self.m_ServerIndex)
            self.m_Acquisition = SapAcquisition(
                self.m_ServerName, self.m_ConfigFile)
            self.m_ServerLocation = SapLocation(
                self.m_ServerName, self.m_ResourceIndex)

            if (SapBuffer.IsBufferTypeSupported(self.m_ServerLocation, SapBuffer.MemoryType.ScatterGather)):
                self.m_Buffers = SapBufferWithTrash(
                    2, self.m_Acquisition, SapBuffer.MemoryType.ScatterGather)
            else:
                self.m_Buffers = SapBufferWithTrash(
                    2, self.m_Acquisition, SapBuffer.MemoryType.ScatterGatherPhysical)

            self.m_Xfer = SapAcqDeviceToBuf(self.m_Acquisition, self.m_Buffers)
            self.m_View = SapView(self.m_Buffers)

            # TODO: Event Handler for Xfer
            self.m_Xfer.pairs[0].EventType = SapXferPair.XferEventType.EndOfFrame

            # TODO: Event Handler for Signal Status

            self.EnableSignalStatus()

        else:
            if (self.m_Acquisition is not None and not self.m_Acquisition.Initialized and self.m_Acquisition.Create() is False):
                print("Unable to create acquisition object. (m_Acquisition)")
                self.DestroyDisposeObjects()
                # raise Exception("Unable to create acquisition object. (m_Acquisition)")

            if (self.m_Buffers is not None and not self.m_Buffers.Initialized and self.m_Buffers.Create() is False):
                print("Unable to create buffer object. (m_Buffers)")
                self.DestroyDisposeObjects()
                # raise Exception("Unable to create acquisition object. (m_Buffers)")

            if (self.m_Xfer is not None and not self.m_Xfer.Initialized and self.m_Xfer.Create() is False):
                self.DestroyDisposeObjects()
                # raise Exception("Unable to create acquisition object. (m_XFer)")

            if (self.m_View is not None and not self.m_View.Initialized and self.m_View.Create() is False):
                self.DestroyDisposeObjects()
                # raise Exception("Unable to create acquisition object. (m_View)")

    def EnableSignalStatus(self):
        if (self.m_Acquisition is not None):
            self.m_IsSignalDetected = (self.m_Acquisition.SignalStatus != (SapAcquisition.AcqSignalStatus(0)))
            if (not self.m_IsSignalDetected):
                print("Online: No camera signal detected. (m_Acquisition)")
            else:
                print("Online: Camera signal detected. (m_Acquisition)")
            self.m_Acquisition.SignalNotifyEnable = True

    def DestroyDisposeObjects(self):
        didDestroy = False
        if (self.m_View is not None and self.m_View.Initialized):
            self.m_View.Destroy()
            didDestroy = True
        if (self.m_Xfer is not None and self.m_Xfer.Initialized):
            self.m_Xfer.Destroy()
            didDestroy = True
        if (self.m_Buffers is not None and self.m_Buffers.Initialized):
            self.m_Buffers.Destroy()
            didDestroy = True
        if (self.m_Acquisition is not None and self.m_Acquisition.Initialized):
            self.m_Acquisition.Destroy()
            didDestroy = True
        
        if (didDestroy):
            self.m_View.Dispose()
            self.m_Xfer.Dispose()
            self.m_Buffers.Dispose()
            self.m_Acquisition.Dispose()
            self.m_View = None
            self.m_Xfer = None
            self.m_Buffers = None
            self.m_Acquisition = None

    def Grab(self):
        print("Grab")
        if (self.m_Xfer is not None):
            self.m_Xfer.Grab()

    def Snap(self):
        print("Snap")
        if (self.m_Xfer is not None):
            self.m_Xfer.Snap()

    def Freeze(self):
        print("Freeze")
        if (self.m_Xfer is not None):
            self.m_Xfer.Freeze()


ImageAcquisitionManager()
