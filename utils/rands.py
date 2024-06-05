"""
This module contains functions for generating random strings of alphanumeric
characters and slugified strings with random strings appended to them.

Functions:
    random_letters(k=5)
        Generate a random string of alphanumeric characters with the specified
        length `k`.

    slugify_new(text)
        Generate a slugified string with a random string of 4 alphanumeric
        characters appended to it.

"""
import string
from random import SystemRandom
from django.utils.text import slugify


def random_letters(k=5):
    """
    Generate a random string of alphanumeric characters with the specified
    length `k`.

    :param k: int, optional, default=5. The length of the random string.
    :return: str. A random string of alphanumeric characters with length `k`.
    """
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase + string.digits, k=k
    ))


def slugify_new(text, k=5):
    """
    Generate a slugified string with a random string of 4 alphanumeric
    characters appended to it.

    :param text: str. The text to be slugified.
    :return: str. A slugified string with a random string of 4 alphanumeric
    characters appended to it.
    """
    return slugify(text) + '-' + random_letters(k)
