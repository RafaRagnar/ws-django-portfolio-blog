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
from django.contrib.auth.models import User
from utils.rands import slugify_new
from utils.images import resize_image
from django_summernote.models import AbstractAttachment


class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save


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


class Post(models.Model):
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title: str = models.CharField(max_length=65)
    slug: str = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )
    excerpt: str = models.CharField(max_length=150)
    is_published: bool = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado'
            'para o post ser exibida publicamente.'
        ),
    )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m',
                              blank=True, default='')
    cover_in_post_content: bool = models.BooleanField(
        default=True,
        help_text=('Se marcado, exibirá a capa dentro do post.'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='post_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='post_updated_by'
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)

        current_cover_name = str(self.cover.name)
        # print('current_cover_name', current_cover_name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        # print('cover_changed', cover_changed)
        if cover_changed:
            resize_image(self.cover, 900, True, 70)

        return super_save
