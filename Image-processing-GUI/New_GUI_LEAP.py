import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("Theme.json")  # Themes: can be a color ex: "blue", but also a .json file if available in the same folder as the program


class App(customtkinter.CTk):

    # Code that affects the GUI's design are put under def __init__(self)
    # functions for the widgets are defined under the class, but outside of def __init__(self)
    
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Standard Mechanics LEAP Tool")
        self.geometry(f"{1130}x{600}")

        # configure grid layout (weight = 0, the default, means the row/column only be as big to fit the widget inside.
        #  weight = 1 will have the row/column expand
        self.grid_columnconfigure((1,2,3,4,5), weight=1)

        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)

        # create sidebar frame; 'sticky = "nsew"' makes it so the sidebar sticks to the specified edges of the cell it's in
        # n = north, s = south, e = east, w = west
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="new")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Place the label Standard Mechanics
        # padx and pady creates space between the widget and the wall of the cell it occupies
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Standard Mechanics",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # The buttons that allows switching frames between Image Acquisition and Image Processing 
        self.swap_frame_buttons = customtkinter.CTkSegmentedButton(self.sidebar_frame)
        self.swap_frame_buttons.configure(values=["Image Processing", "Image Acquisition"], 
                                          command=self.swap_frame_button_callback)
        self.swap_frame_buttons.grid(row=1, column=0,padx=(10, 10), pady=(10, 10))
        self.swap_frame_buttons.set("Image Processing")

        ################################################################################################
        # Create Image Processing frame, buttons created below should be attached to this frame
        self.img_proc_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # Brings up the frame on startup (This GUI frame is starts on 1 column over from the sidebar
        # So buttons placed on this specific frame may start on column 0 to start at the beginning of this frame)
        self.img_proc_frame.grid(row=0, column=1, sticky="nsew")

        # create select image button. Placeholder command is set to sidebar_button_event
        self.select_image = customtkinter.CTkButton(self.img_proc_frame, command=self.sidebar_button_event)
        self.select_image.grid(row=1, column=0, padx=10, pady=10)
        self.select_image.configure(text="Select Image")

        # create reset tool button
        self.reset_tool = customtkinter.CTkButton(self.img_proc_frame, command=self.sidebar_button_event)
        self.reset_tool.grid(row=2, column=0, padx=10, pady=10)
        self.reset_tool.configure(text="Reset Tool")

        # create calibrate distance button
        self.calibrate_dist = customtkinter.CTkButton(self.img_proc_frame, command=self.sidebar_button_event)
        self.calibrate_dist.grid(row=3, column=0, padx=10, pady=10)
        self.calibrate_dist.configure(text="Calibrate Dist")

        # create make video button
        self.make_video = customtkinter.CTkButton(self.img_proc_frame, command=self.sidebar_button_event)
        self.make_video.grid(row=4, column=0, padx=10, pady=10)
        self.make_video.configure(text="Make Video")

        # Set entry labels
        self.linerate_label = customtkinter.CTkLabel(self.img_proc_frame, text = "Line Rate (/s)", font=('Arial Black',14))
        self.linerate_label.grid(row = 1, column = 5)
        self.line_rate = customtkinter.CTkEntry(self.img_proc_frame, placeholder_text='Lines/s')
        self.line_rate.grid(row = 1, column = 6)
     
        self.black_label = customtkinter.CTkLabel(self.img_proc_frame, text = "Black Level", font=('Arial Black',14))
        self.black_label.grid(row = 2, column = 5)
        self.black_level = customtkinter.CTkEntry(self.img_proc_frame)
        self.black_level.insert(0,'50') # Places initial value
        self.black_level.grid(row = 2, column = 6)

        self.white_label = customtkinter.CTkLabel(self.img_proc_frame, text = "White Level", font=('Arial Black',14))
        self.white_label.grid(row = 3, column = 5)
        self.white_level = customtkinter.CTkEntry(self.img_proc_frame)
        self.white_level.insert(0,'200')
        self.white_level.grid(row = 3, column = 6)
        
        self.threshold_label = customtkinter.CTkLabel(self.img_proc_frame, text = "Threshold", font=('Arial Black',14), anchor='e')
        self.threshold_label.grid(row = 4, column = 5)
        self.threshold = customtkinter.CTkEntry(self.img_proc_frame)
        self.threshold.insert(0,'125')
        self.threshold.grid(row = 4, column = 6)

        self.lineLimit_label = customtkinter.CTkLabel(self.img_proc_frame, text = "Line Limit", font=('Arial Black',14))
        self.lineLimit_label.grid(row = 5, column = 5)
        self.line_limit = customtkinter.CTkEntry(self.img_proc_frame)
        self.line_limit.grid(row = 5, column = 6)

        self.blurradius_label = customtkinter.CTkLabel(self.img_proc_frame, text = "Blur Radius (pix)", font=('Arial Black',14))
        self.blurradius_label.grid(row = 6, column = 5)
        self.blur_radius = customtkinter.CTkEntry(self.img_proc_frame)
        self.blur_radius.insert(0,'5')
        self.blur_radius.grid(row = 6, column = 6)

        self.pix2dist_label = customtkinter.CTkLabel(self.img_proc_frame, text = "Distance/Pix (um)", font=('Arial Black',14))
        self.pix2dist_label.grid(row = 7, column = 5)
        self.pix2dist = customtkinter.CTkEntry(self.img_proc_frame, placeholder_text='Run Calibration')
        self.pix2dist.grid(row = 7, column = 6)
    
        ################################################################################################
        # Create Image Acquisition frame, buttons created below should be attached to this frame
        self.img_acq_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Creates the Freeze button
        self.Freeze = customtkinter.CTkButton(self.img_acq_frame, command=self.sidebar_button_event)
        self.Freeze.grid(row=0, column=4, padx=20, pady=10)
        self.Freeze.configure(text="Freeze")

        # Creates the Live Button
        self.Live = customtkinter.CTkButton(self.img_acq_frame, command=self.sidebar_button_event)
        self.Live.grid(row=0, column=5 , padx=20, pady=10)
        self.Live.configure(text="Live")

        # Creates the Arm button
        self.Arm = customtkinter.CTkButton(self.img_acq_frame, command=self.sidebar_button_event)
        self.Arm.grid(row=0, column= 6, padx=20, pady=10)
        self.Arm.configure(text="Arm")

        # Creates the Load button
        self.Load = customtkinter.CTkButton(self.img_acq_frame, command=self.sidebar_button_event)
        self.Load.grid(row=0, column= 7, padx=20, pady=10)
        self.Load.configure(text="Load")

        # Creates the save button
        self.Save = customtkinter.CTkButton(self.img_acq_frame, command=self.sidebar_button_event)
        self.Save.grid(row = 0, column = 8, padx = 20, pady=10)
        self.Save.configure(text="Save")
        
    # This section is for command functions of the GUI operations above

    # Function that changes the frame based on the name clicked
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.img_proc_frame.configure(fg_color=("gray75", "gray25") if name == "Image Processing" else "transparent")
        self.img_acq_frame.configure(fg_color=("gray75", "gray25") if name == "Image Acquisition" else "transparent")

        # show selected frame, starts at column=1 so it doesn't overlap with the sidebar
        if name == "Image Processing":
            self.img_proc_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.img_proc_frame.grid_forget()
        if name == "Image Acquisition":
            self.img_acq_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.img_acq_frame.grid_forget()

    # Function that connects button press to changing the frame
    def swap_frame_button_callback(self, value):
        self.select_frame_by_name(value)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def sidebar_button_event(self):
        print("sidebar_button click")


# Runs the App, does not need to be changed
if __name__ == "__main__":
    app = App()
    app.mainloop()