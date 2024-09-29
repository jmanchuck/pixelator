from unittest.mock import MagicMock
import pytest
from PIL import Image
from image_model import ImageModel


@pytest.fixture
def image_model():
    model = ImageModel()
    model.load_image("tests/images/test_image.png")  # Adjust the path as needed
    return model


def test_brightness_transformation(image_model):
    original_image = image_model.original_image
    transformed_image = image_model.apply_brightness(1.5)(original_image)
    # Check if the brightness transformation is applied correctly
    assert transformed_image is not None


def test_pixelation_transformation(image_model):
    original_image = image_model.original_image
    transformed_image = image_model.apply_pixelation(5)(original_image)
    # Check if the pixelation transformation is applied correctly
    assert transformed_image is not None


def test_pixelation_no_effect(image_model):
    original_image = image_model.original_image
    # Apply pixelation with pixel_size = 1 (no change expected)
    transformed_image = image_model.apply_pixelation(1)(original_image)
    assert transformed_image == original_image  # Should return the original image


def test_invert_colours_transformation(image_model):
    original_image = image_model.original_image
    transformed_image = image_model.invert_colours()(original_image)
    # Check if the color inversion transformation is applied correctly
    assert transformed_image is not None


def test_process_pipeline(image_model):
    final_image = image_model.process_pipeline()
    assert final_image is not None


def test_reset_pipeline(image_model):
    image_model.reset_pipeline()
    assert len(image_model.transformations) == 0


def test_load_image_invalid_path(image_model):
    with pytest.raises(FileNotFoundError):
        image_model.load_image("invalid/path/to/image.png")


def test_brightness_extreme_values(image_model):
    original_image = image_model.original_image
    # Brightness set to 0.0 (darken the image)
    dark_image = image_model.apply_brightness(0.0)(original_image)
    assert dark_image is not None

    # Brightness set to 2.0 (increase brightness)
    bright_image = image_model.apply_brightness(2.0)(original_image)
    assert bright_image is not None

    # Brightness set to None (should raise an error)
    with pytest.raises(TypeError):
        image_model.apply_brightness(None)(original_image)


def test_invert_colours_grayscale(image_model):
    # Convert the image to grayscale (mode "L")
    grayscale_image = image_model.original_image.convert("L")
    inverted_image = image_model.invert_colours()(grayscale_image)
    assert inverted_image is not None
    assert inverted_image.mode == "L"  # Ensure it's still grayscale


def test_invert_colours_rgba(image_model):
    # Convert the image to RGBA (if not already)
    rgba_image = image_model.original_image.convert("RGBA")
    inverted_image = image_model.invert_colours()(rgba_image)
    assert inverted_image is not None
    assert inverted_image.mode == "RGBA"  # Ensure it's still RGBA


def test_save_image_without_modification(image_model):
    # Clear the modified_image to simulate no modifications made
    image_model.modified_image = None

    # Saving without modifications should not raise an error, but no image will be saved
    image_model.save_image("tests/images/no_modifications_image.png")


def test_process_pipeline_no_image(image_model):
    # Simulate no image being loaded
    image_model.original_image = None

    # Call process_pipeline and ensure it returns None when no image is loaded
    final_image = image_model.process_pipeline()
    assert final_image is None


def test_save_image_no_modifications(image_model):
    # Set modified_image to None to simulate no modifications made
    image_model.modified_image = None

    # Call save_image (it shouldn't attempt to save anything)
    image_model.save_image("tests/images/no_modifications_image.png")

    # Since modified_image is None, no save should be attempted, and the test will pass if no error occurs.


def test_save_image_with_modifications(image_model):
    # Mock the modified_image to simulate that modifications have been made
    image_model.modified_image = MagicMock()

    # Mock the save method of the modified_image
    image_model.modified_image.save = MagicMock()

    # Call save_image and check that save is called
    image_model.save_image("tests/images/saved_image.png")

    # Assert that the save method was called with the correct file path
    image_model.modified_image.save.assert_called_once_with(
        "tests/images/saved_image.png"
    )
