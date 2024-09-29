import tkinter as tk
from image_model import ImageModel
from image_view import ImageView


class ImageController:
    def __init__(self, root: tk.Tk):
        self.model = ImageModel()
        self.view = ImageView(root, self)
        self.brightness_value = 1.0  # Default brightness value
        self.pixel_size = 1  # Default pixel size
        self.invert_active = False  # Track whether invert is active

    def load_image(self) -> None:
        """Load an image from the file system and reset the pipeline."""
        file_path = self.view.ask_open_filename()
        if file_path:
            self.model.load_image(file_path)
            self.model.reset_pipeline()  # Clear any previous transformations
            self.update_image_pipeline()

    def update_brightness(self, *args) -> None:
        """Update the brightness based on the slider and reapply the pipeline."""
        self.brightness_value = self.view.brightness_slider.get()
        self.reapply_pipeline()

    def update_pixelation(self, *args) -> None:
        """Update pixelation based on the slider and reapply the pipeline."""
        self.pixel_size = self.view.pixel_size_slider.get()
        self.reapply_pipeline()

    def toggle_invert_colours(self) -> None:
        """Toggle the invert colors option and reapply the pipeline."""
        self.invert_active = bool(
            self.view.invert_var.get()
        )  # Get the current toggle state
        self.reapply_pipeline()

    def reapply_pipeline(self) -> None:
        """Reapply the pipeline from scratch."""
        # Reset the pipeline
        self.model.reset_pipeline()

        # Apply brightness transformation
        self.model.add_transformation(
            self.model.apply_brightness(self.brightness_value)
        )

        # Apply pixelation if needed
        if self.pixel_size > 1:
            self.model.add_transformation(self.model.apply_pixelation(self.pixel_size))

        # Apply color inversion if toggle is active
        if self.invert_active:
            self.model.add_transformation(self.model.invert_colours())

        # Process and display the updated image
        self.update_image_pipeline()

    def update_image_pipeline(self) -> None:
        """Process the pipeline and display the final result."""
        final_image = self.model.process_pipeline()
        if final_image:
            self.view.display_image(final_image)

    def save_image(self) -> None:
        """Save the final processed image to the file system."""
        file_path = self.view.ask_save_filename()
        if file_path:
            self.model.save_image(file_path)


if __name__ == "__main__":  # pragma: no cover
    root = tk.Tk()
    app = ImageController(root)  # Initialize the controller
    root.mainloop()  # Start the Tkinter event loop
