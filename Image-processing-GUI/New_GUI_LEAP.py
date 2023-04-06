import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("Theme.json")  # Themes: can be a color ex: "blue", but also a .json file


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Standard Mechanics LEAP Tool")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Standard Mechanics",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.select_image = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.select_image.grid(row=1, column=0, padx=20, pady=10)
        self.reset_tool = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.reset_tool.grid(row=2, column=0, padx=20, pady=10)
        self.calibrate_dist = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.calibrate_dist.grid(row=3, column=0, padx=20, pady=10)
        self.make_video = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.make_video.grid(row=4, column=0, padx=20, pady=10)
   

        self.linerate_label = customtkinter.CTkLabel(self, text = "Line Rate (/s)", font=('Arial Black',14))
        self.linerate_label.grid(row = 1, column = 5)
        self.line_rate = customtkinter.CTkEntry(self, placeholder_text='Lines/s')
        self.line_rate.grid(row = 1, column = 6)
     


        # set default values
        self.select_image.configure(text="Select Image")
        self.reset_tool.configure(text="Reset Tool")
        self.calibrate_dist.configure(text="Calibrate Dist")
        self.make_video.configure(text="Make Video")
        

    # This section is for functions of the GUI operations above
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def sidebar_button_event(self):
        print("sidebar_button click")


# Runs the App, does not need to be changed
if __name__ == "__main__":
    app = App()
    app.mainloop()