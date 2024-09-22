import tkinter as tk
from image_model import ImageModel
from image_view import ImageView

class ImageController:
    def __init__(self, root: tk.Tk):
        self.model = ImageModel()
        self.view = ImageView(root, self)

    def load_image(self) -> None:
        file_path = self.view.ask_open_filename()
        if file_path:
            self.model.load_image(file_path)
            self.view.display_image(self.model.original_image)

    def update_pixelation(self, *args) -> None:
        pixel_size = self.view.get_pixel_size()
        pixelated_image = self.model.pixelate_image(pixel_size)
        if pixelated_image:
            self.view.display_image(pixelated_image)

    def save_image(self) -> None:
        file_path = self.view.ask_save_filename()
        if file_path:
            self.model.save_image(file_path)

    def invert_colours(self) -> None:
        inverted_image = self.model.invert_colours()
        if inverted_image:
            self.view.display_image(inverted_image)

def main():
    root = tk.Tk()
    app = ImageController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
