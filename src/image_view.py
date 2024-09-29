import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600

class ImageView:
    def __init__(self, master: tk.Tk, controller):
        self.master = master
        self.master.title("Image Pixelator")
        self.controller = controller

        # Canvas to display the image
        self.canvas = tk.Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack()

        # Load image button
        load_button = tk.Button(master, text="Load Image", command=self.controller.load_image)
        load_button.pack()

        # Pixelation slider
        self.pixel_size_slider = tk.Scale(
            master,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            label="Pixel Size",
            command=self.controller.update_pixelation
        )
        self.pixel_size_slider.pack()
        self.pixel_size_slider.set(1)

        # Brightness slider
        self.brightness_slider = tk.Scale(
            master,
            from_=0.5,  # Darker
            to=2.0,     # Brighter
            resolution=0.1,
            orient=tk.HORIZONTAL,
            label="Brightness",
            command=self.controller.update_brightness  # Call controller method
        )
        self.brightness_slider.pack()
        self.brightness_slider.set(1.0)

        # Save button
        save_button = tk.Button(master, text="Save Image", command=self.controller.save_image)
        save_button.pack()

        # Toggle for Invert Colors
        self.invert_var = tk.IntVar()  # Variable to track toggle state (0 or 1)
        invert_toggle = tk.Checkbutton(
            master,
            text="Invert Colors",
            variable=self.invert_var,
            command=self.controller.toggle_invert_colours
        )
        invert_toggle.pack()

        # To store the displayed image
        self.photo = None

    def display_image(self, image: Image.Image) -> None:
        """Display the image on the canvas."""
        image.thumbnail((CANVAS_WIDTH, CANVAS_HEIGHT))  # Resize image to fit the canvas
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, image=self.photo, anchor=tk.CENTER)

    def ask_open_filename(self) -> str:
        """Open file dialog to select an image."""
        file_path = filedialog.askopenfilename(
            title="Select an Image"
        )
        return file_path

    def ask_save_filename(self) -> str:
        """Open file dialog to save the modified image."""
        file_path = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png"
        )
        return file_path
