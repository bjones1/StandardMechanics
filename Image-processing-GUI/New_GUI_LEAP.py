import tkinter
import tkinter.messagebox
import tkinter.filedialog
import customtkinter
import os
from ImageAcquisition import ImageAcquisitionManager
import cv2
import numpy as np
from PIL import Image, ImageTk
import cairo

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: can be a color ex: "blue", but also a .json file if available in the same folder as the program
customtkinter.set_default_color_theme("Theme.json")

JAISerialHandle = None
ImageAcquisitionHandle = None


class App(customtkinter.CTk):
    # Code that affects the GUI's design are put under def __init__(self)
    # functions for the widgets are defined under the class, but outside of def __init__(self)
    def __init__(self):
        super().__init__()
        self.ImageAcquisitionHandle = ImageAcquisitionManager(self.ImageHandler)
        # Data Members
        self.COMPort = "COM1"

        # Top-Level Window
        self.arm_settings_window = None

        # Configure window
        self.title("Standard Mechanics LEAP Tool")
        self.geometry(f"{1280}x{720}")
        self.minsize(1280, 720)

        # configure grid layout (weight = 0, the default, means the row/column only be as big to fit the widget inside.
        #  weight = 1 will have the row/column expand
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        # create sidebar frame; 'sticky = "nsew"' makes it so the sidebar sticks to the specified edges of the cell it's in
        # n = north, s = south, e = east, w = west
        self.topbar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.topbar_frame.grid(row=0, column=0, columnspan=9, sticky="new")
        self.topbar_frame.grid_rowconfigure(4, weight=1)
        self.topbar_frame.configure(bg_color="black")

        # Place the label Standard Mechanics
        # padx and pady creates space between the widget and the wall of the cell it occupies
        self.logo_label = customtkinter.CTkLabel(
            self.topbar_frame, text="Standard Mechanics", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=2, column=0, padx=10, pady=(10, 10))

        # Setup Image Canvas (it will use NoImage.png as a placeholder image)
        # Load the image
        image = Image.open("NoImage.png")
        # Resize the image to 300x300 pixels
        resized_image = image.resize((800, 400))
        photo = ImageTk.PhotoImage(resized_image)

        self.ImageCanvas = customtkinter.CTkLabel(self, image=photo, text="")
        self.ImageCanvas.grid(row=2, column=0, columnspan=4,
                              rowspan=4, padx=10, sticky="nsew")

        # Instead of having entire frames, we can use the TabView widget to show the different controls to the right of the image
        self.tab_view = customtkinter.CTkTabview(self)
        self.tab_view.grid(row=2, column=4, columnspan=5,
                           rowspan=4, padx=10, sticky="nsew")
        self.image_processing_tab = self.tab_view.add("Image Processing")
        self.serial_configuration_tab = self.tab_view.add(
            "Advanced Configuration")

        # Setup Image Processing Tab
        self.image_processing_frame = ImageProcessingFrame(
            self.image_processing_tab, corner_radius=0)

        # Setup Advanced Configuration Tab
        self.serial_configuration_frame = AdvancedConfigurationFrame(
            self.serial_configuration_tab, corner_radius=0)

        # Only show the Image Processing Tab on startup
        self.tab_view.set("Image Processing")

        # Creates the Freeze button
        self.FreezeButton = customtkinter.CTkButton(self, command=self.Freeze)
        self.FreezeButton.grid(row=6, column=0)
        self.FreezeButton.configure(text="Freeze")

        # Creates the Grab Button
        self.GrabButton = customtkinter.CTkButton(self, command=self.Grab)
        self.GrabButton.grid(row=6, column=1)
        self.GrabButton.configure(text="Live")

        # Creates the Snap Button
        self.SnapButton = customtkinter.CTkButton(self, command=self.Arm)
        self.SnapButton.grid(row=6, column=2)
        self.SnapButton.configure(text="Arm")

        # Creates the Load button
        self.Load = customtkinter.CTkButton(self, command=self.Load)
        self.Load.grid(row=7, column=0)
        self.Load.configure(text="Load")

        # Creates the save button
        self.Save = customtkinter.CTkButton(self, command=self.Save)
        self.Save.grid(row=7, column=2)
        self.Save.configure(text="Save")

        ################################################################################################
        # Default Initialization Values                                                                #
        ################################################################################################

        try:
            # Show a Popup Dialog asking for the COM port of the JAI camera
            self.COMPortDialog = customtkinter.CTkInputDialog(
                title="COM Port", text="Enter COM Port of JAI Camera:")
            COMPortInput = self.COMPortDialog.get_input()

            # If no COM port is entered, default to COM1
            if COMPortInput != "":
                self.COMPort = COMPortInput

            # JAISerialHandle is not a local variable, it is a global variable that is used in other classes and functions
            JAISerialHandle = JAISerial(self.COMPort, 115200)
        except Exception as e:
            # Popup warning message if no JAI camera is detected or if initialization fails. Show specific exception message
            tkinter.messagebox.showwarning(
                "Warning", "No JAI Camera Detected. Please check connection and try again. \n\n %s" % (repr(e)))

    def sidebar_button_event(self):
        print("sidebar_button click")

    def Freeze(self):
        if (ImageAcquisitionHandle is not None):
            xfer = ImageAcquisitionHandle.Freeze()
            if (xfer is not None and xfer.Grabbing is False):
                self.SnapButton.configure(state="enabled")
                self.GrabButton.configure(state="enabled")
                self.FreezeButton.configure(state="disabled")
            else:
                tkinter.messagebox.showwarning(
                    "Warning", "Frame Grabber did not respond. Please check connection and try again.")

    def Grab(self):
        if (ImageAcquisitionHandle is not None):
            xfer = ImageAcquisitionHandle.Grab()
            if (xfer is not None and xfer.Grabbing is True):
                self.SnapButton.configure(state="disabled")
                self.GrabButton.configure(state="disabled")
                self.FreezeButton.configure(state="enabled")
            else:
                # Display warning message saying that the Frame Grabber is not grabbing
                tkinter.messagebox.showwarning(
                    "Warning", "Frame Grabber did not respond. Please check connection and try again.")

    def Load(self):
        # TODO: Add code to load an image (not within scope of this team's work)
        print("Load")

    def Save(self):
        # TODO: Add code to save the image (not within scope of this team's work)
        print("Save")

    def ImageHandler(self, m_View):
        # Image Handle should be called whenever a new image is received (theoretically)

        # Get the image out of the m_View buffer
        m_Buffer = m_View.GetBuffer()
        np_Array = np.asarray(m_Buffer.GetRow(0), dtype=np.uint8)
        np_Img = np_Array.reshape(m_Buffer.GetHeight(), m_Buffer.GetWidth())

        # PIL Library is used to convert the image from a numpy array to a PIL Image
        pil_Img = Image.fromarray(np_Img)

        # Convert the PIL Image to a Tkinter Image
        tk_Img = ImageTk.PhotoImage(pil_Img)

        # Resize the image to fit the
        tk_Img = tk_Img.resize((800, 400))

        # Attach the image to the Frame in Image Acquisition
        self.ImageCanvas.configure(image=tk_Img)

    def Arm(self):
        if self.arm_settings_window is None or not self.arm_settings_window.winfo_exists():
            # create window if its None or destroyed
            self.arm_settings_window = ArmPopup(self)
        else:
            self.arm_settings_window.focus()  # if window exists focus it


class ImageProcessingFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create reset tool button
        self.reset_tool = customtkinter.CTkButton(
            master, command=self.image_processing_reset_tool, state="disabled")
        self.reset_tool.grid(row=7, column=1, padx=10, pady=10)
        self.reset_tool.configure(text="Reset Tool")

        # create calibrate distance button
        self.calibrate_dist = customtkinter.CTkButton(
            master, command=self.sidebar_button_event, state="disabled")
        self.calibrate_dist.grid(row=7, column=2, padx=10, pady=10)
        self.calibrate_dist.configure(text="Calibrate Dist")

        # Set entry labels
        self.linerate_label = customtkinter.CTkLabel(
            master, text="Line Rate (/s)", font=('Arial Black', 14))
        self.linerate_label.grid(row=0, column=1)
        self.line_rate = customtkinter.CTkEntry(
            master, placeholder_text='Lines/s')
        self.line_rate.grid(row=0, column=2)

        self.black_label = customtkinter.CTkLabel(
            master, text="Black Level", font=('Arial Black', 14))
        self.black_label.grid(row=1, column=1)
        self.black_level = customtkinter.CTkEntry(master)
        self.black_level.insert(0, '50')  # Places initial value
        self.black_level.grid(row=1, column=2)

        self.white_label = customtkinter.CTkLabel(
            master, text="White Level", font=('Arial Black', 14))
        self.white_label.grid(row=2, column=1)
        self.white_level = customtkinter.CTkEntry(master)
        self.white_level.insert(0, '200')
        self.white_level.grid(row=2, column=2)

        self.threshold_label = customtkinter.CTkLabel(
            master, text="Threshold", font=('Arial Black', 14), anchor='e')
        self.threshold_label.grid(row=3, column=1)
        self.threshold = customtkinter.CTkEntry(master)
        self.threshold.insert(0, '125')
        self.threshold.grid(row=3, column=2)

        self.lineLimit_label = customtkinter.CTkLabel(
            master, text="Line Limit", font=('Arial Black', 14))
        self.lineLimit_label.grid(row=4, column=1)
        self.line_limit = customtkinter.CTkEntry(master)
        self.line_limit.grid(row=4, column=2)

        self.blurradius_label = customtkinter.CTkLabel(
            master, text="Blur Radius (pix)", font=('Arial Black', 14))
        self.blurradius_label.grid(row=5, column=1)
        self.blur_radius = customtkinter.CTkEntry(master)
        self.blur_radius.insert(0, '5')
        self.blur_radius.grid(row=5, column=2)

        self.pix2dist_label = customtkinter.CTkLabel(
            master, text="Distance/Pix (um)", font=('Arial Black', 14))
        self.pix2dist_label.grid(row=6, column=1)
        self.pix2dist = customtkinter.CTkEntry(
            master, placeholder_text='Run Calibration')
        self.pix2dist.grid(row=6, column=2)

    def image_processing_reset_image_canvas(self):
        # Load the NoImage.png Image as a placeholder
        self.no_image = Image.open("NoImage.png")

        # Resize the image to fit the canvas
        self.no_image = self.no_image.resize(
            (self.ImageCanvas.winfo_width(), self.ImageCanvas.winfo_height()), Image.LANCZOS)

        self.no_image = ImageTk.PhotoImage(self.no_image)

        self.ImageCanvas.create_image(0, 0, image=self.no_image, anchor="nw")

    def image_processing_reset_tool(self):
        self.line_rate.delete(0, tkinter.END)
        self.black_level.delete(0, tkinter.END)
        self.white_level.delete(0, tkinter.END)
        self.threshold.delete(0, tkinter.END)
        self.line_limit.delete(0, tkinter.END)
        self.blur_radius.delete(0, tkinter.END)
        self.pix2dist.delete(0, tkinter.END)

        # All values are reset to 0, so now set them to their default values
        self.black_level.insert(0, "50")
        self.white_level.insert(0, "200")
        self.threshold.insert(0, "125")
        self.blur_radius.insert(0, "5")

        # Set the placeholder text for the line limit and pix2dist
        # These are internal calls that probably shouldn't be used, but it works
        self.line_rate._activate_placeholder()
        self.pix2dist._activate_placeholder()

        # Disable all the buttons
        self.reset_tool.configure(state="disabled")
        self.calibrate_dist.configure(state="disabled")
        self.make_video.configure(state="disabled")

        # Reset the image canvas
        self.image_processing_reset_image_canvas()

    def sidebar_button_event(self):
        print("sidebar_button click")

    def serial_configuration_set_baud(self):
        if (JAISerialHandle is None):
            tkinter.messagebox.showwarning(
                "Warning", "No JAI camera detected. Please check connection and try again.")
            return

        try:
            # Convert ComboBox value to int
            numericalBaud = int(self.baudrate_combo.get())

            JAISerialHandle.SetBaudRate(numericalBaud)
        except Exception as e:
            tkinter.messagebox.showwarning(
                "Warning", "Error setting baud rate. Please try again. \n\n" + repr(e))


class AdvancedConfigurationFrame(customtkinter.CTkFrame):
    # TODO: Attach these to Serial Configuration Tool
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create Baudrate dropdown
        self.baudrate_label = customtkinter.CTkLabel(
            master, text=" Baud Rate (bps): ", font=('Arial Black', 14))
        self.baudrate_label.grid(row=0, column=1)
        self.baudrate_combo = customtkinter.CTkComboBox(
            master, state="readonly", values=["9600", "19200", "38400", "57600", "115200"])
        self.baudrate_combo.grid(row=0, column=2)
        self.baudrate_combo.set("115200")

        # Create CL_Clock dropdown
        self.CL_Clock_label = customtkinter.CTkLabel(
            master, text=" CL Clock: ", font=('Arial Black', 14))
        self.CL_Clock_label.grid(row=1, column=1)
        self.CL_Clock_combo = customtkinter.CTkComboBox(
            master, state="readonly", values=["0: 85 MHz", "1: 63.75 MHz", "2: 31.875 MHz"])
        self.CL_Clock_combo.grid(row=1, column=2)
        self.CL_Clock_combo.set("0: 85MHz")

        # Create ExposureMode dropdown
        self.ExposureMode_label = customtkinter.CTkLabel(
            master, text=" Exposure Mode: ", font=('Arial Black', 14))
        self.ExposureMode_label.grid(row=2, column=1)
        self.ExposureMode_combo = customtkinter.CTkComboBox(
            master, state="readonly", values=["0: Off", "1: Timed", "2: TriggerWidth"])
        self.ExposureMode_combo.grid(row=2, column=2)
        self.ExposureMode_combo.set("0: Off")

        # Create Gain Level
        self.Gain_Level_label = customtkinter.CTkLabel(
            master, text=" Gain Level (100-1600):", font=('Arial Black', 14))
        self.Gain_Level_label.grid(row=3, column=1)
        self.Gain_Level_level = customtkinter.CTkEntry(
            master, placeholder_text='100-1600')
        self.Gain_Level_level.grid(row=3, column=2)
        # self.Gain_Level_level.bind("<Return>", self.serial_configuration_set_linerate)

        # Create AnalogBaseGain dropdown
        self.AnalogBaseGain_label = customtkinter.CTkLabel(
            master, text=" Analog Base Gain: ", font=('Arial Black', 14))
        self.AnalogBaseGain_label.grid(row=4, column=1)
        self.AnalogBaseGain_combo = customtkinter.CTkComboBox(
            master, state="readonly", values=["0: 0dB", "1: +6dB", "2: +9.54dB", "3: +12 dB"])
        self.AnalogBaseGain_combo.grid(row=4, column=2)
        self.AnalogBaseGain_combo.set("0: 0dB")


class ArmPopup(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x600")
        self.title("Line Scan Camera Control")
        self.resizable(False, False)
        self.master = args[0]
        # Setup Grids and Rows for the window
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=1)

        self.external_linetrigger_label = customtkinter.CTkLabel(
            self, text="External Line Trigger", font=('Arial Black', 14))
        self.external_linetrigger_label.grid(row=1, column=0, sticky="w")

        # Add CTK Switch for Line Trigger Enable
        self.external_linetrigger_enable = customtkinter.CTkSwitch(
            self, text="Enable", font=('Arial Black', 14), command=self.external_linetrigger_enable_handler)
        self.external_linetrigger_enable.grid(row=2, column=0, sticky="w")

        # Add Option Box for Detection Edge
        self.external_linetrigger_detection_edge_label = customtkinter.CTkLabel(
            self, text="Detection Edge", font=('Arial Black', 14))
        self.external_linetrigger_detection_edge_label.grid(
            row=2, column=1, sticky="w")
        self.external_linetrigger_detection_edge_combo = customtkinter.CTkComboBox(
            self, state="readonly", values=["0: Rising Edge", "1: Falling Edge"], command=self.external_linetrigger_detection_edge_handler)
        self.external_linetrigger_detection_edge_combo.grid(
            row=2, column=2, sticky="e")
        self.external_linetrigger_detection_edge_combo.set("0: Rising Edge")
        self.external_linetrigger_detection_edge_combo.configure(
            state="disabled")

        # Add Option Box for Level (TTL or RS422)
        self.external_linetrigger_level_label = customtkinter.CTkLabel(
            self, text="Level", font=('Arial Black', 14))
        self.external_linetrigger_level_label.grid(row=3, column=1, sticky="w")
        self.external_linetrigger_level_combo = customtkinter.CTkComboBox(
            self, state="readonly", values=["0: TTL", "1: RS422"], command=self.external_linetrigger_level_handler)
        self.external_linetrigger_level_combo.grid(row=3, column=2, sticky="e")
        self.external_linetrigger_level_combo.set("1: RS422")
        self.external_linetrigger_level_combo.configure(state="disabled")

        # Add External Frame Trigger Label
        self.external_frametrigger_label = customtkinter.CTkLabel(
            self, text="External Frame Trigger", font=('Arial Black', 14))
        self.external_frametrigger_label.grid(row=4, column=0, sticky="w")

        # Add CTK Switch for External Frame Trigger Enable
        self.external_frametrigger_enable = customtkinter.CTkSwitch(
            self, text="Enable", font=('Arial Black', 14), command=self.external_frametrigger_enable_handler)
        self.external_frametrigger_enable.grid(row=5, column=0, sticky="w")

        # Add Option Box for Detection Edge
        self.external_frametrigger_detection_edge_label = customtkinter.CTkLabel(
            self, text="Detection Edge", font=('Arial Black', 14))
        self.external_frametrigger_detection_edge_label.grid(
            row=5, column=1, sticky="w")
        self.external_frametrigger_detection_edge_combo = customtkinter.CTkComboBox(
            self, state="readonly", values=["0: Rising Edge", "1: Falling Edge"], command=self.external_frametrigger_detection_edge_handler)
        self.external_frametrigger_detection_edge_combo.grid(
            row=5, column=2, sticky="e")
        self.external_frametrigger_detection_edge_combo.set("0: Rising Edge")
        self.external_frametrigger_detection_edge_combo.configure(
            state="disabled")

        # Add Option Box for Level (TTL or RS422)
        self.external_frametrigger_level_label = customtkinter.CTkLabel(
            self, text="Level", font=('Arial Black', 14))
        self.external_frametrigger_level_label.grid(
            row=6, column=1, sticky="w")
        self.external_frametrigger_level_combo = customtkinter.CTkComboBox(
            self, state="readonly", values=["0: TTL", "1: RS422"], command=self.external_frametrigger_level_handler)
        self.external_frametrigger_level_combo.grid(
            row=6, column=2, sticky="e")
        self.external_frametrigger_level_combo.set("0: TTL")
        self.external_frametrigger_level_combo.configure(state="disabled")

    # Handle External Line Trigger Enable
    def external_linetrigger_enable_handler(self):
        if self.external_linetrigger_enable.get() == 1:
            self.external_linetrigger_detection_edge_combo.configure(
                state="normal")
            self.external_linetrigger_level_combo.configure(state="normal")

            # Disable External Frame Trigger Options and Enable Switch
            self.external_frametrigger_enable.deselect()
            self.external_frametrigger_enable.configure(state="disabled")
            self.external_frametrigger_detection_edge_combo.configure(state="disabled")
            self.external_frametrigger_level_combo.configure(state="disabled")
            self.master.ImageAcquisitionHandle.SetExternalLineTrigger(1)
        else:
            # Disable External Line Trigger Options and Enable Both Switches
            self.external_linetrigger_detection_edge_combo.configure(state="disabled")
            self.external_linetrigger_level_combo.configure(state="disabled")
            self.external_frametrigger_enable.configure(state="normal")
            self.master.ImageAcquisitionHandle.SetExternalLineTrigger(0)

    # Handle External Frame Trigger Enable
    def external_frametrigger_enable_handler(self):
        if self.external_frametrigger_enable.get() == 1:
            self.external_frametrigger_detection_edge_combo.configure(state="normal")
            self.external_frametrigger_level_combo.configure(state="normal")

            # Disable External Line Trigger Options and Enable Switch
            self.external_linetrigger_enable.deselect()
            self.external_linetrigger_enable.configure(state="disabled")
            self.external_linetrigger_detection_edge_combo.configure(state="disabled")
            self.external_linetrigger_level_combo.configure(state="disabled")
            self.master.ImageAcquisitionHandle.SetExternalFrameTrigger(1)
        else:
            # Disable External Frame Trigger Options and Enable Both Switches
            self.external_frametrigger_detection_edge_combo.configure(state="disabled")
            self.external_frametrigger_level_combo.configure(state="disabled")
            self.external_linetrigger_enable.configure(state="normal")
            self.master.ImageAcquisitionHandle.SetExternalFrameTrigger(0)
    
    # Handle External Line Trigger Detection Edge
    def external_linetrigger_detection_edge_handler(self, choice):
        if self.external_linetrigger_detection_edge_combo.get() == "0: Rising Edge":
            self.master.ImageAcquisitionHandle.SetExternalLineTriggerDetection(1)
        else:
            self.master.ImageAcquisitionHandle.SetExternalLineTriggerDetection(0)

    # Handle External Line Trigger Level
    def external_linetrigger_level_handler(self, choice):
        if self.external_linetrigger_level_combo.get() == "0: TTL":
            self.master.ImageAcquisitionHandle.SetExternalLineTriggerLevel(1)
        else:
            self.master.ImageAcquisitionHandle.SetExternalLineTriggerLevel(0)

    # Handle External Frame Trigger Detection Edge
    def external_frametrigger_detection_edge_handler(self, choice):
        if self.external_frametrigger_detection_edge_combo.get() == "0: Rising Edge":
            self.master.ImageAcquisitionHandle.SetExternalFrameTriggerDetection(1)
        else:
            self.master.ImageAcquisitionHandle.SetExternalFrameTriggerDetection(0)

    # Handle External Frame Trigger Level
    def external_frametrigger_level_handler(self, choice):
        if self.external_frametrigger_level_combo.get() == "0: TTL":
            self.master.ImageAcquisitionHandle.SetExternalFrameTriggerLevel(1)
        else:
            self.master.ImageAcquisitionHandle.SetExternalFrameTriggerLevel(0)


# Runs the App, does not need to be changed
if __name__ == "__main__":
    app = App()
    app.mainloop()
