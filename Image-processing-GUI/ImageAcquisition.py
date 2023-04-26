import sys
import os
import clr

sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Demos/NET/GrabDemo/CSharp/bin/Debug")
sys.path.append("C:/Program Files/Teledyne DALSA/Sapera/Components/NET/Bin")
clr.AddReference("SapNETCSharpGrabDemo")
clr.AddReference("DALSA.SaperaLT.SapClassBasic")
clr.AddReference("System.Windows.Forms")

from DALSA.SaperaLT.SapClassBasic import SapManager, SapAcquisition, SapBuffer, SapAcqToBuf, SapLocation, SapBufferWithTrash, SapAcqDeviceToBuf, SapXferPair, SapView, SapXferNotifyHandler, SapSignalNotifyHandler, SapSignalNotifyEventArgs
from DALSA.SaperaLT.SapClassGui import *

class ImageAcquisitionManager:
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

    # Init Replaces the "CreateObjects" function in the original: grab_demo_testing.py
    def __init__(self, image_handler):
        # Image Handler is a function that takes in the image buffer and works on it.
        # This is handled in New_GUI_LEAP.py
        self.image_handler = image_handler

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

            # Event Handler for when an image is received from the camera
            self.m_Xfer.pairs[0].EventType = SapXferPair.XferEventType.EndOfFrame
            self.m_Xfer.XferNotify += SapXferNotifyHandler(self.BufferHandler)
            self.m_Xfer.XferNotifyContext = self

            # Event Handler for when a signal is received from the camera
            self.m_Acquisition.SignalNotify += SapSignalNotifyHandler(
                self.EnableSignalStatus)
            self.m_Acquisition.SignalNotifyContext = self

        else:
            if (self.m_Acquisition is not None and not self.m_Acquisition.Initialized and self.m_Acquisition.Create() is False):
                print("Unable to create acquisition object. (m_Acquisition)")
                self.DestroyDisposeObjects()

            if (self.m_Buffers is not None and not self.m_Buffers.Initialized and self.m_Buffers.Create() is False):
                print("Unable to create buffer object. (m_Buffers)")
                self.DestroyDisposeObjects()

            if (self.m_Xfer is not None and not self.m_Xfer.Initialized and self.m_Xfer.Create() is False):
                self.DestroyDisposeObjects()

            if (self.m_View is not None and not self.m_View.Initialized and self.m_View.Create() is False):
                self.DestroyDisposeObjects()

    def EnableSignalStatus(self, sender, eventArgs):
        SapAcquisition.AcqSignalStatus = eventArgs.SignalStatus
        sender.m_IsSignalDetected = (SapAcquisition.AcqSignalStatus != 0)
        if (not sender.m_IsSignalDetected):
            print("Signal found")
        else:
            print("Signal detected")

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

    # Begin "recording" from the camera, this is a continuous stream of images
    def Grab(self):
        if (self.m_Xfer is not None):
            self.m_Xfer.Grab()
            return self.m_Xfer

    # Gets a singular frame from the camera
    def Snap(self):
        if (self.m_Xfer is not None):
            self.m_Xfer.Snap()
            return self.m_Xfer

    # This pretty much just stops the camera from grabbing images, works on both Grab and Snap
    def Freeze(self):
        if (self.m_Xfer is not None):
            self.m_Xfer.Freeze()
            return self.m_Xfer

    # This may not be necessary, but it is here for now
    def ShowView(self):
        if (self.m_View is not None):
            self.m_View.Show()

    # Called when an image is (theoretically) ready to be processed, this is where we will pass the image data to the GUI
    # ImageHandler is passed in by New_GUI_Leap when the class is instantiated
    def BufferHandler(self, sender, eventArgs):
        # We are leveraging the SapView object to handle the image data, but a future implementation should rely on the buffer object not the view object as we have our own "view" object in the GUI
        self.image_handler(self.m_View)

    def SetExternalLineTrigger(self, state):
        # This likely won't work but I couldn't find the correct val to set
        if (self.m_Acquisition is not None):
            self.m_Acquisition.SetParameter(SapAcquisition.Prm.EXT_LINE_TRIGGER_ENABLE, state)

    def SetExternalLineTriggerDetection(self, state):
        if (self.m_Acquisition is not None):
            self.m_Acquisition.SetParameter(SapAcquisition.Prm.EXT_LINE_TRIGGER_DETECTION, SapAcquisition.Val.RISING_EDGE if state else SapAcquisition.Val.FALLING_EDGE)

    def SetExternalLineTriggerLevel(self, state):
        if (self.m_Acquisition is not None):
            self.m_Acquisition.SetParameter(SapAcquisition.Prm.EXT_LINE_TRIGGER_LEVEL, SapAcquisition.Val.LEVEL_TTL if state else SapAcquisition.Val.LEVEL_422)

    def SetExternalFrameTrigger(self, state):
        # This likely won't work but I couldn't find the correct val to set
        if (self.m_Acquisition is not None):
            self.m_Acquisition.SetParameter(SapAcquisition.Prm.EXT_FRAME_TRIGGER_ENABLE, state)

    def SetExternalFrameTriggerDetection(self, state):
        if (self.m_Acquisition is not None):
            self.m_Acquisition.SetParameter(SapAcquisition.Prm.EXT_FRAME_TRIGGER_DETECTION, SapAcquisition.Val.RISING_EDGE if state else SapAcquisition.Val.FALLING_EDGE)

    def SetExternalFrameTriggerLevel(self, state):
        if (self.m_Acquisition is not None):
            self.m_Acquisition.SetParameter(SapAcquisition.Prm.EXT_FRAME_TRIGGER_LEVEL, SapAcquisition.Val.LEVEL_TTL if state else SapAcquisition.Val.LEVEL_422)