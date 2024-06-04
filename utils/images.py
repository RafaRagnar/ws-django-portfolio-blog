"""
Module for image processing functions.

This module contains functions for processing and manipulating images.
"""
from pathlib import Path

from django.conf import settings
from PIL import Image


def resize_image(image_django, new_width=800, optimize=True, quality=60):
    """
    Resize an image to a specified width.

    This function resizes an image to a specified width using the Pillow
    library. It also optimizes the image for web use and reduces its quality
    to save space.

    Args:
        image_django (File): The Django file object to resize.
        new_width (int): The new width of the image. Default is 800.
        optimize (bool): Whether to optimize the image for web use. Default
        is True.
        quality (int): The quality of the image. Default is 60.

    Returns:
        Image: The resized image.
    """
    image_path = Path(settings.MEDIA_ROOT / image_django.name).resolve()
    image_pillow = Image.open(image_path)
    original_width, original_height = image_pillow.size

    if original_width <= new_width:
        image_pillow.close()
        return image_pillow

    new_height = round(new_width * original_height / original_width)

    new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

    new_image.save(
        image_path,
        optimize=optimize,
        quality=quality,
    )

    return new_image
