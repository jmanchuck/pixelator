import pytest
from unittest.mock import MagicMock, patch
from image_controller import ImageController
from image_view import ImageView


@pytest.fixture
def image_controller():
    with patch("tkinter.IntVar"), patch("tkinter.StringVar"):
        root = MagicMock()  # Mock the Tkinter root
        controller = ImageController(root)
        controller.view = MagicMock(spec=ImageView)  # Mock the ImageView
        controller.view.invert_var = MagicMock()  # Mock the IntVar
        return controller


def test_load_image(image_controller):
    image_controller.view.ask_open_filename = MagicMock(
        return_value="tests/images/test_image.png"
    )
    image_controller.load_image()
    assert image_controller.model.original_image is not None


def test_save_image(image_controller):
    image_controller.model.save_image = MagicMock()

    image_controller.view.ask_save_filename = MagicMock(
        return_value="tests/images/saved_image.png"
    )
    image_controller.save_image()
    # Check if save_image was called on the model
    image_controller.model.save_image.assert_called_once_with(
        "tests/images/saved_image.png"
    )


def test_update_brightness(image_controller):
    image_controller.view.brightness_slider = MagicMock()
    image_controller.view.brightness_slider.get = MagicMock(return_value=1.5)
    image_controller.update_brightness()
    assert image_controller.brightness_value == 1.5


def test_update_pixelation(image_controller):
    image_controller.view.pixel_size_slider = MagicMock()
    image_controller.view.pixel_size_slider.get = MagicMock(return_value=5)
    image_controller.update_pixelation()
    assert image_controller.pixel_size == 5


def test_toggle_invert_colours(image_controller):
    image_controller.view.invert_var.get = MagicMock(return_value=1)
    image_controller.toggle_invert_colours()
    assert image_controller.invert_active is True
