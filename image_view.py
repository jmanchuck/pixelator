import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

class ImageView:
    def __init__(self, master: tk.Tk, controller):
        self.master = master
        self.master.title("Image Pixelator")
        self.controller = controller

        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()

        load_button = tk.Button(master, text="Load Image", command=self.controller.load_image)
        load_button.pack()

        self.pixel_size_slider = tk.Scale(
            master,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            label="Pixel Size",
            command=self.controller.update_pixelation
        )
        self.pixel_size_slider.pack()

        save_button = tk.Button(master, text="Save Pixelated Image", command=self.controller.save_image)
        save_button.pack()

        invert_button = tk.Button(master, text="Invert Image", command=self.controller.invert_colours)
        invert_button.pack()

        grayscale_button = tk.Button(master, text="Convert to Grayscale", command=self.controller.convert_to_grayscale)
        grayscale_button.pack()

        self.photo = None

    def display_image(self, image: Image.Image) -> None:
        image.thumbnail((500, 500))
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(250, 250, image=self.photo, anchor=tk.CENTER)

    def get_pixel_size(self) -> int:
        return self.pixel_size_slider.get()

    def ask_open_filename(self) -> str:
        return filedialog.askopenfilename()

    def ask_save_filename(self) -> str:
        return filedialog.asksaveasfilename(defaultextension=".png")
