import ttkbootstrap as ttk
from ttkbootstrap import font
from ttkbootstrap.constants import *
from PIL import ImageTk, Image

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 100

class Gui:
    def __init__(self):
        self.root = ttk.Window(size=(1024,600))
        motor1_img = ImageTk.PhotoImage(Image.open("shaft.png").resize((IMAGE_HEIGHT, IMAGE_WIDTH)))
        motor2_img = ImageTk.PhotoImage(Image.open("winding.png").resize((IMAGE_HEIGHT, IMAGE_WIDTH)))
        temp_img = ImageTk.PhotoImage(Image.open("temp.png").resize((IMAGE_HEIGHT, IMAGE_WIDTH)))

        self.buttons_enabled = False

        self.IMAGES = [motor1_img, motor2_img, temp_img]
        self.LABELS = ["Motor 1", "Motor 2", "Control de temperatura"]
        self.displays = []
        self.sum_buttons = []
        self.sub_buttons = []
        self.meters = []
#         print(self.meters)

        self.default_font = font.nametofont('TkDefaultFont')
        self.default_font['size'] = 20

        self.define_widgets()
        self.grid_configure()

    def define_widgets(self): ## Rueda motor
        for i in range(0, 2):
            self.meters.append(ttk.Meter(
                amountused=i,
                metertype="semi",
                textright="HZ",
                subtext="Frequency",
                bootstyle="success",
                ))
            
        self.meters.append(ttk.Meter( ## Rueda set temp
            amountused=30,
            metertype="semi",
            textright="°C",
            subtext="Set temperature",
            bootstyle="warning",
            ))
        
        self.meters.append(ttk.Meter( ## Rueda get temp
            amountused=0,
            metertype="semi",
            textright="°C",
            subtext="Tank temperature",
            bootstyle="info",
            ))

        for i in range(0, 3):
            if i < 2:
                ttk.Label(self.root, text=self.LABELS[i], anchor="center", bootstyle="inverse-info"
                ).grid(row=0, column=i, sticky="nesw")
                ttk.Label(self.root, image=self.IMAGES[i], anchor="center", bootstyle="info"
                ).grid(row=1, column=i, sticky="nsew")
            else:
                ttk.Label(self.root, text=self.LABELS[i], anchor="center", bootstyle="inverse-info"
                ).grid(row=0, column=i, sticky="nesw", columnspan = 2)
                ttk.Label(self.root, image=self.IMAGES[i], anchor="center", bootstyle="info"
                ).grid(row=1, column=i, sticky="nsew", columnspan = 2)

            self.meters[i].grid(row=2, column=i, sticky="nsew")
            self.sum_buttons.append(ttk.Button(self.root, bootstyle="info", text="+"))
            self.sum_buttons[i].grid(row=3, column=i, sticky="nsew")
            self.sub_buttons.append(ttk.Button(self.root, bootstyle="info", text="-" ))
            self.sub_buttons[i].grid(row=4, column=i, sticky="nsew")
        
        self.meters[-1].grid(row=2, column=3, sticky="nsew")
        self.sum_buttons[-1].grid(row=3, column=i, sticky="nsew", columnspan = 2)
        self.sub_buttons[-1].grid(row=4, column=i, sticky="nsew", columnspan = 2)
        
        self.start_button = ttk.Button(self.root, bootstyle="success", text="Start")
        self.start_button.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.stop_button = ttk.Button(self.root, bootstyle="danger", text="Stop", state="disabled")
        self.stop_button.grid(row=5, column=2, sticky="nsew", columnspan = 2)
        
    def switch(self):
        # For the stop button
        if not self.buttons_enabled:
            self.stop_button.configure(state="normal")
            self.start_button.configure(state="disabled")
            self.buttons_enabled = True
            
            for i in range(0, 3):
                self.sum_buttons[i].configure(state="disabled")
                self.sub_buttons[i].configure(state="disabled")
            return
        # For the start button
        if self.buttons_enabled:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.buttons_enabled = False
        
            for i in range(0, 3):
                self.sum_buttons[i].configure(state="normal")
                self.sub_buttons[i].configure(state="normal")
            return
        
    
    def grid_configure(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=2)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=2)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

#     def prompt_user():

# test = Gui()