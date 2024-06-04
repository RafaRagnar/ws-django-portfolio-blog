"""
This module contains custom validators for Django models.

Validators:
    validate_png: Validates that an image is a PNG file.
"""
from django.core.exceptions import ValidationError


def validate_png(image):
    """
    Validate that the image is a PNG file.

    This function checks if the image is a PNG file by checking its file
    extension. If the image is not a PNG file, it raises a ValidationError.
    """
    if not image.name.lower().endswith('.png'):
        raise ValidationError("Image must be a PNG file")
