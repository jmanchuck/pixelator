from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from typing import Optional

class ImageModel:
    def __init__(self):
        self.original_image: Optional[Image.Image] = None
        self.pixelated_image: Optional[Image.Image] = None

    def load_image(self, file_path: str) -> None:
        self.original_image = Image.open(file_path)
        self.pixelated_image = self.original_image

    def pixelate_image(self, pixel_size: int) -> Optional[Image.Image]:
        if self.original_image:
            image = self.original_image.copy()
            image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST)
            image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST)
            self.pixelated_image = image
            return image
        return None

    def invert_colours(self) -> Optional[Image.Image]:
        if self.pixelated_image:
            self.pixelated_image = ImageOps.invert(self.pixelated_image)
            return self.pixelated_image
        return None

    def adjust_brightness(self, value: float) -> Optional[Image.Image]:
        if self.pixelated_image:
            enhancer = ImageEnhance.Brightness(self.pixelated_image)
            self.pixelated_image = enhancer.enhance(value)
            return self.pixelated_image
        return None

    def apply_filter(self, filter_type: str) -> Optional[Image.Image]:
        if self.pixelated_image:
            if filter_type == "BLUR":
                self.pixelated_image = self.pixelated_image.filter(ImageFilter.BLUR)
            elif filter_type == "SHARPEN":
                self.pixelated_image = self.pixelated_image.filter(ImageFilter.SHARPEN)
            return self.pixelated_image
        return None

    def save_image(self, file_path: str) -> None:
        if self.pixelated_image:
            self.pixelated_image.save(file_path)
