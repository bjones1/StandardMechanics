import tkinter
import tkinter.messagebox
import tkinter.filedialog
import customtkinter
from SerialManager import JAISerial
from ImageAcquisition import ImageAcquisitionManager
import cv2
import numpy as np
from PIL import Image, ImageTk

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

        global JAISerialHandle
        global ImageAcquisitionHandle

        # Data Members
        self.COMPort = "COM1"
        self.ImageProcessingImage = None

        # Configure window
        self.title("Standard Mechanics LEAP Tool")
        self.geometry(f"{1130}x{600}")

        # configure grid layout (weight = 0, the default, means the row/column only be as big to fit the widget inside.
        #  weight = 1 will have the row/column expand
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        # create sidebar frame; 'sticky = "nsew"' makes it so the sidebar sticks to the specified edges of the cell it's in
        # n = north, s = south, e = east, w = west
        self.topbar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.topbar_frame.grid(row=0, column=0, columnspan=6, sticky="new")
        self.topbar_frame.grid_rowconfigure(4, weight=1)
        self.topbar_frame.configure(bg_color="black")

        # Place the label Standard Mechanics
        # padx and pady creates space between the widget and the wall of the cell it occupies
        self.logo_label = customtkinter.CTkLabel(self.topbar_frame, text="Standard Mechanics", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # The buttons that allows switching frames between Image Acquisition and Image Processing
        self.swap_frame_buttons = customtkinter.CTkSegmentedButton(self.topbar_frame)
        self.swap_frame_buttons.configure(values=["Image Processing", "Image Acquisition", "Serial Configuration"], command=self.select_frame_by_name)

        # Swap Frame Buttons Should be on the far right of the sidebar
        self.swap_frame_buttons.grid(
            row=0, column=1, padx=20, pady=(20, 10), sticky="e")
        self.swap_frame_buttons.set("Image Processing")

        # Setup Image Processing Frame
        self.image_processing_frame = ImageProcessingFrame(
            self, corner_radius=0)

        # Setup Image Acquisition Frame
        self.image_acquisition_frame = ImageAcquistionFrame(
            self, corner_radius=0)

        # Brings up the Image Processing Frame on startup (This GUI frame is starts on 1 row below the top bar)
        # So buttons placed on this specific frame may start on column 0 to start at the beginning of this frame)
        self.image_processing_frame.grid(
            row=1, column=0, columnspan=6, rowspan=9, sticky="nsew")

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

        # Create the ImageAcquisitionManager
        # ImageAcquisitionHandle = ImageAcquisitionManager()

        self.image_processing_frame.image_processing_reset_image_canvas()

    # This section is for command functions of the GUI operations above

    # Function that changes the frame based on the name clicked

    def select_frame_by_name(self, name):
        if (name == "Image Processing"):
            self.image_processing_frame.grid(row=1, column=1, sticky="nsew")
            self.image_acquisition_frame.grid_forget()
        elif (name == "Image Acquisition"):
            self.image_acquisition_frame.grid(row=1, column=1, sticky="nsew")
            self.image_processing_frame.grid_forget()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def sidebar_button_event(self):
        print("sidebar_button click")


class ImageProcessingFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        global JAISerialHandle
        global ImageAcquisitionHandle

        # create select image button. Placeholder command is set to sidebar_button_event
        self.select_image = customtkinter.CTkButton(
            self, command=self.image_processing_select_image)
        self.select_image.grid(row=0, column=0, padx=10, pady=10)
        self.select_image.configure(text="Select Image")

        # create reset tool button
        self.reset_tool = customtkinter.CTkButton(
            self, command=self.image_processing_reset_tool, state="disabled")
        self.reset_tool.grid(row=1, column=0, padx=10, pady=10)
        self.reset_tool.configure(text="Reset Tool")

        # create calibrate distance button
        self.calibrate_dist = customtkinter.CTkButton(
            self, command=self.sidebar_button_event, state="disabled")
        self.calibrate_dist.grid(row=2, column=0, padx=10, pady=10)
        self.calibrate_dist.configure(text="Calibrate Dist")

        # create make video button
        self.make_video = customtkinter.CTkButton(
            self, command=self.sidebar_button_event, state="disabled")
        self.make_video.grid(row=3, column=0, padx=10, pady=10)
        self.make_video.configure(text="Make Video")

        # Image Canvas
        self.ImageCanvas = tkinter.Canvas(self)
        self.ImageCanvas.grid(row=0, column=1, columnspan=3,
                              rowspan=6, sticky="nsew")

        # Set entry labels
        self.linerate_label = customtkinter.CTkLabel(
            self, text="Line Rate (/s)", font=('Arial Black', 14))
        self.linerate_label.grid(row=0, column=5)
        self.line_rate = customtkinter.CTkEntry(
            self, placeholder_text='Lines/s')
        self.line_rate.grid(row=0, column=6)
        self.line_rate.bind("<Return>", self.set_linerate)

        self.black_label = customtkinter.CTkLabel(
            self, text="Black Level", font=('Arial Black', 14))
        self.black_label.grid(row=1, column=5)
        self.black_level = customtkinter.CTkEntry(self)
        self.black_level.insert(0, '50')  # Places initial value
        self.black_level.grid(row=1, column=6)

        self.white_label = customtkinter.CTkLabel(
            self, text="White Level", font=('Arial Black', 14))
        self.white_label.grid(row=2, column=5)
        self.white_level = customtkinter.CTkEntry(self)
        self.white_level.insert(0, '200')
        self.white_level.grid(row=2, column=6)

        self.threshold_label = customtkinter.CTkLabel(
            self, text="Threshold", font=('Arial Black', 14), anchor='e')
        self.threshold_label.grid(row=3, column=5)
        self.threshold = customtkinter.CTkEntry(self)
        self.threshold.insert(0, '125')
        self.threshold.grid(row=3, column=6)

        self.lineLimit_label = customtkinter.CTkLabel(
            self, text="Line Limit", font=('Arial Black', 14))
        self.lineLimit_label.grid(row=4, column=5)
        self.line_limit = customtkinter.CTkEntry(self)
        self.line_limit.grid(row=4, column=6)

        self.blurradius_label = customtkinter.CTkLabel(
            self, text="Blur Radius (pix)", font=('Arial Black', 14))
        self.blurradius_label.grid(row=5, column=5)
        self.blur_radius = customtkinter.CTkEntry(self)
        self.blur_radius.insert(0, '5')
        self.blur_radius.grid(row=5, column=6)

        self.pix2dist_label = customtkinter.CTkLabel(
            self, text="Distance/Pix (um)", font=('Arial Black', 14))
        self.pix2dist_label.grid(row=6, column=5)
        self.pix2dist = customtkinter.CTkEntry(
            self, placeholder_text='Run Calibration')
        self.pix2dist.grid(row=6, column=6)

        # Create Baudrate dropdown
        self.baudrate_label = customtkinter.CTkLabel(
            self, text="Baud Rate (bps): ", font=('Arial Black', 14))
        self.baudrate_label.grid(row=0, column=7)
        self.baudrate_combo = customtkinter.CTkComboBox(self, state="readonly", values=[
                                                        "9600", "19200", "38400", "57600", "115200"])
        self.baudrate_combo.grid(row=0, column=8)
        self.baudrate_combo.set("115200")

        self.set_buad_button = customtkinter.CTkButton(
            self, command=self.serial_configuration_set_baud)
        self.set_buad_button.grid(row=1, column=8)
        self.set_buad_button.configure(text="Set Baud Rate")

    def image_processing_select_image(self):
        file = tkinter.filedialog.askopenfilename(
            filetypes=[("Images (.bmp)", "*.bmp")])

        # If no file is selected, return
        if file == "" or file is None or file == ():
            print("No file selected")
            return

        # Load the image
        self.ImageProcessingImage = cv2.imread(file, 0)

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

    def set_linerate(self, event):
        # TODO: This is a placeholder function, it needs to be implemented
        print("set_linerate")


class ImageAcquistionFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        global JAISerialHandle
        global ImageAcquisitionHandle

        ImageAcquisitionHandle = ImageAcquisitionManager(self.ImageHandler)

        # Creates the Freeze button
        self.FreezeButton = customtkinter.CTkButton(
            self, command=self.Freeze)
        self.FreezeButton.grid(row=0, column=4, padx=20, pady=10)
        self.FreezeButton.configure(text="Freeze")

        # Creates the Grab Button
        self.GrabButton = customtkinter.CTkButton(
            self, command=self.Grab)
        self.GrabButton.grid(row=0, column=5, padx=20, pady=10)
        self.GrabButton.configure(text="Grab")

        # Creates the Snap Button
        self.SnapButton = customtkinter.CTkButton(
            self, command=self.Snap)
        self.SnapButton.grid(row=0, column=6, padx=20, pady=10)
        self.SnapButton.configure(text="Snap")

        # Creates the Load button
        self.Load = customtkinter.CTkButton(
            self, command=self.sidebar_button_event)
        self.Load.grid(row=0, column=7, padx=20, pady=10)
        self.Load.configure(text="Load")

        # Creates the save button
        self.Save = customtkinter.CTkButton(
            self, command=self.sidebar_button_event)
        self.Save.grid(row=0, column=8, padx=20, pady=10)
        self.Save.configure(text="Save")

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

    def Snap(self):
        if (ImageAcquisitionHandle is not None):
            xfer = ImageAcquisitionHandle.Snap()
            if (xfer is not None and xfer.Grabbing is True):
                self.SnapButton.configure(state="disabled")
                self.GrabButton.configure(state="disabled")
                self.FreezeButton.configure(state="enabled")
            else:
                tkinter.messagebox.showwarning(
                    "Warning", "Frame Grabber did not respond. Please check connection and try again.")
       
    def ImageHandler(self, m_View):
        # Image Handle should be called whenever a new image is received (theoretically)
        
        # Get the image out of the m_View buffer
        m_Buffer = m_View.GetBuffer()
        np_Array = np.asarray(m_Buffer.GetRow(0), dtype=np.uint8)
        np_Img = np_Array.reshape(m_Buffer.GetHeight(), m_Buffer.GetWidth())

        # Apply appropriate color space conversion to place formatting in the correct format for OpenCV
        cv_Img = cv2.cvtColor(np_Img, cv2.COLOR_GRAY2BGR)

        # TODO - Attach the image to the Frame in Image Processing
        print("Image Acquistion Frame - Image Handler")
        print(cv_Img)

# Runs the App, does not need to be changed
if __name__ == "__main__":
    app = App()
    app.mainloop()
