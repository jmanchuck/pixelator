import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
from typing import Optional, Tuple

class ImagePixelator:
    def __init__(self, master: tk.Tk) -> None:
        self.master: tk.Tk = master
        self.master.title("Image Pixelator")
        
        self.original_image: Optional[Image.Image] = None
        self.pixelated_image: Optional[Image.Image] = None
        self.photo: Optional[ImageTk.PhotoImage] = None

        # Create GUI elements
        self.canvas: tk.Canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()

        load_button: tk.Button = tk.Button(master, text="Load Image", command=self.load_image)
        load_button.pack()

        self.pixel_size_slider: tk.Scale = tk.Scale(
            master, 
            from_=1, 
            to=100, 
            orient=tk.HORIZONTAL, 
            label="Pixel Size", 
            command=self.update_pixelation
        )
        self.pixel_size_slider.pack()

        save_button: tk.Button = tk.Button(master, text="Save Pixelated Image", command=self.save_image)
        save_button.pack() 

        invert_button: tk.Button = tk.Button(master, text="Invert Image", command=self.invert_colours)
        invert_button.pack()

    def invert_colours(self):
        if self.pixelate_image:
            self.pixelated_image = ImageOps.invert(self.pixelated_image)
            self.original_image = ImageOps.invert(self.original_image)
            self.display_image(self.pixelated_image)
    
    def load_image(self) -> None:
        file_path: str = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image)
            self.update_pixelation()

    def display_image(self, image: Image.Image) -> None:
        image.thumbnail((500, 500))  # Resize image to fit canvas
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(250, 250, image=self.photo, anchor=tk.CENTER)

    def pixelate_image(self, image: Image.Image, pixel_size: int) -> Image.Image:
        image = image.copy()  # Create a copy to avoid modifying the original
        image = image.resize(
            (image.size[0] // pixel_size, image.size[1] // pixel_size), 
            Image.NEAREST
        )
        image = image.resize(
            (image.size[0] * pixel_size, image.size[1] * pixel_size), 
            Image.NEAREST
        )
        return image

    def update_pixelation(self, *args: Tuple[str, ...]) -> None:
        if self.original_image:
            pixel_size: int = self.pixel_size_slider.get()
            self.pixelated_image = self.pixelate_image(self.original_image, pixel_size)
            self.display_image(self.pixelated_image)

    def save_image(self) -> None:
        if self.pixelated_image:
            file_path: str = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.pixelated_image.save(file_path)

def main() -> None:
    root: tk.Tk = tk.Tk()
    app: ImagePixelator = ImagePixelator(root)
    root.mainloop()

if __name__ == "__main__":
    main()