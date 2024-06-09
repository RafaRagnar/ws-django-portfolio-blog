"""
This module contains the `Tag`, `Category`, `Page` and `Post` models,
which represent a tag, a category, a page and a post in the application,
respectively.

Classes:
    Tag
        A model representing a tag in the application.
    Category
        A model representing a category in the application.
    Page
        A model representing a page in the application.
    Post
        A model representing a post in the application.

Methods:
    save(*args, **kwargs)
        Override the default save method to generate a unique slug for the
        tag, category, page or post if it does not already have one.
"""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment  # type: ignore
from utils.rands import slugify_new
from utils.images import resize_image


class PostAttachment(AbstractAttachment):
    """
    Represents an attachment for a post.
    """

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to set the file name
        and resize the image if needed.

        Args:
            *args: Additional positional arguments to be passed to the
                superclass's save method.
            **kwargs: Additional keyword arguments to be passed to the
                superclass's save method.
        """
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        # pylint: disable=assignment-from-no-return
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

    name: str = models.CharField(max_length=255)  # type: ignore
    slug: str = models.SlugField(
        unique=True, default=None, null=True, blank=True,
        max_length=255,  # type: ignore
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

    name: str = models.CharField(max_length=255)  # type: ignore
    slug: str = models.SlugField(
        unique=True, default=None, null=True, blank=True,
        max_length=255,  # type: ignore
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
    """
    A model representing a page in the application.

    Attributes:
        title (str): The title of the page.
        slug (str): A unique slug for the page.
        is_published (bool): Whether the page is published or not.
        content (str): The content of the page.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title: str = models.CharField(max_length=65)  # type: ignore
    slug: str = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )  # type: ignore
    is_published: bool = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado'
            'para a página ser exibida publicamente.'
        ),
    )  # type: ignore
    content = models.TextField()  # type: ignore

    def get_absolute_url(self):
        """
        Returns the absolute URL for the detail page of the object.

        This method is used to generate the canonical URL for the object, which
        can be used for linking in templates or other contexts.
        """
        if not self.is_published:
            return reverse('blog:index')

        return reverse('blog:page', args=(self.slug,))

    def save(self, *args, **kwargs):
        """
        Override the default save method to generate a unique slug for the
        page if it does not already have one.

        Args:
            *args: Additional positional arguments to be passed to the
                superclass's save method.
            **kwargs: Additional keyword arguments to be passed to the
                superclass's save method.
        """
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.title)


class PostManager(models.Manager):
    """
    Custom manager for the Post model.
    """

    def get_published(self):
        """
        Returns a queryset of published posts ordered by descending pk.
        """
        return self.filter(is_published=True).order_by('-pk')


class Post(models.Model):
    """
    A model representing a post in the application.

    Attributes:
        title (str): The title of the post.
        slug (str): A unique slug for the post.
        excerpt (str): A short excerpt of the post.
        is_published (bool): Whether the post is published or not.
        content (str): The content of the post.
        cover (ImageField): The cover image of the post.
        cover_in_post_content (bool): Whether to display the cover
            image within the post's content.
        created_at (DateTimeField): The date and time the post was created.
        created_by (ForeignKey): The user who created the post.
        updated_at (DateTimeField): The date and time the post was updated.
        updated_by (ForeignKey): The user who updated the post.
        category (ForeignKey): The category the post belongs to.
        tags (ManyToManyField): The tags associated with the post.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title: str = models.CharField(max_length=65)  # type: ignore
    slug: str = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )  # type: ignore
    excerpt: str = models.CharField(max_length=150)  # type: ignore
    is_published: bool = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado'
            'para o post ser exibida publicamente.'
        ),
    )  # type: ignore
    content = models.TextField()  # type: ignore
    cover = models.ImageField(upload_to='posts/%Y/%m',
                              blank=True, default='')
    cover_in_post_content: bool = models.BooleanField(
        default=True,
        help_text=('Se marcado, exibirá a capa dentro do post.'),
    )  # type: ignore

    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='post_created_by'
    )  # type: ignore
    updated_at = models.DateTimeField(auto_now=True)  # type: ignore
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='post_updated_by'
    )  # type: ignore

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )  # type: ignore
    tags = models.ManyToManyField(Tag, blank=True, default='')  # type: ignore

    def get_absolute_url(self):
        """
        Returns the absolute URL for the detail page of the post.

        This method is used to generate the canonical URL for the post,
        which can be used for linking in templates or other contexts.
        """
        if not self.is_published:
            return reverse('blog:index')

        return reverse('blog:post', args=(self.slug,))

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args, **kwargs):
        """
        Override the default save method to generate a unique slug for the
        post and resize the cover image if needed.

        Args:
            *args: Additional positional arguments to be passed to the
                superclass's save method.
            **kwargs: Additional keyword arguments to be passed to the
                superclass's save method.
        """
        if not self.slug:
            self.slug = slugify_new(self.title, 4)

        current_cover_name = str(self.cover.name)
        # pylint: disable=assignment-from-none
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900, True, 70)

        return super_save
