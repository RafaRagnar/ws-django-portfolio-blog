"""
This module contains the `Tag` and `Category` models, which represent a tag
and a category in the application, respectively.

Classes:
    Tag
        A model representing a tag in the application.
    Category
        A model representing a category in the application.

Methods:
    save(*args, **kwargs)
        Override the default save method to generate a unique slug for the
        tag or category if it does not already have one.
"""
from django.db import models
from utils.rands import slugify_new


class Tag(models.Model):
    """
    A model representing a tag in the application.

    Attributes:
        name (str): The name of the tag.
        slug (str): A unique slug for the tag.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name: str = models.CharField(max_length=255)
    slug: str = models.SlugField(
        unique=True, default=None, null=True, blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        """
        Override the default save method to generate a unique slug for the
        tag or category if it does not already have one.

        Args:
            *args: Additional positional arguments to be passed to the
                superclass's save method.
            **kwargs: Additional keyword arguments to be passed to the
                superclass's save method.
        """
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Category(models.Model):
    """
    A model representing a category in the application.

    Attributes:
        name (str): The name of the category.
        slug (str): A unique slug for the category.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name: str = models.CharField(max_length=255)
    slug: str = models.SlugField(
        unique=True, default=None, null=True, blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        """
        Override the default save method to generate a unique slug for the
        tag or category if it does not already have one.

        Args:
            *args: Additional positional arguments to be passed to the
                superclass's save method.
            **kwargs: Additional keyword arguments to be passed to the
                superclass's save method.
        """
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Page(models.Model):
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title: str = models.CharField(max_length=65)
    slug: str = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )
    is_published: bool = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado'
            'para a página ser exibida publicamente.'
        ),
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.title)
