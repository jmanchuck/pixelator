from PIL import Image, ImageOps, ImageEnhance
from typing import Optional, List, Callable


class ImageModel:
    def __init__(self):
        self.original_image: Optional[Image.Image] = None
        self.modified_image: Optional[Image.Image] = None
        self.transformations: List[Callable[[Image.Image], Image.Image]] = (
            []
        )  # Holds pipeline transformations

    def load_image(self, file_path: str) -> None:
        """Load the original image."""
        self.original_image = Image.open(file_path)
        self.modified_image = self.original_image

    def add_transformation(
        self, transformation: Callable[[Image.Image], Image.Image]
    ) -> None:
        """Add a transformation to the pipeline."""
        self.transformations.append(transformation)

    def apply_brightness(
        self, brightness_value: float
    ) -> Callable[[Image.Image], Image.Image]:
        """Return a transformation that adjusts brightness."""

        def transformation(image: Image.Image) -> Image.Image:
            enhancer = ImageEnhance.Brightness(image)
            return enhancer.enhance(brightness_value)

        return transformation

    def apply_pixelation(self, pixel_size: int) -> Callable[[Image.Image], Image.Image]:
        """Return a transformation that applies pixelation."""

        def transformation(image: Image.Image) -> Image.Image:
            # Downscale and then upscale to create pixelation
            if pixel_size > 1:
                pixelated = image.resize(
                    (image.size[0] // pixel_size, image.size[1] // pixel_size),
                    Image.NEAREST,
                )
                return pixelated.resize(
                    (pixelated.size[0] * pixel_size, pixelated.size[1] * pixel_size),
                    Image.NEAREST,
                )
            return image

        return transformation

    def invert_colours(self) -> Callable[[Image.Image], Image.Image]:
        """Return a transformation that inverts colors."""

        def transformation(image: Image.Image) -> Image.Image:
            if image.mode == "RGBA":
                r, g, b, a = image.split()  # Separate alpha channel
                inverted_image = ImageOps.invert(
                    Image.merge("RGB", (r, g, b))
                )  # Invert RGB channels
                return Image.merge(
                    "RGBA",
                    (
                        inverted_image.split()[0],
                        inverted_image.split()[1],
                        inverted_image.split()[2],
                        a,
                    ),
                )
            else:
                return ImageOps.invert(image)

        return transformation

    def process_pipeline(self) -> Optional[Image.Image]:
        """Apply all transformations in the pipeline, starting from the original image."""
        if not self.original_image:
            return None
        image = self.original_image  # Always start with the original image
        for transformation in self.transformations:
            image = transformation(image)
        self.modified_image = image
        return self.modified_image

    def reset_pipeline(self) -> None:
        """Clear the current transformation pipeline."""
        self.transformations.clear()

    def save_image(self, file_path: str) -> None:
        """Save the final processed image."""
        if self.modified_image:
            self.modified_image.save(file_path)
