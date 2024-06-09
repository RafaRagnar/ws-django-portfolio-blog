"""
Module for defining Django models for site setup and menu links.

This module contains two models: SiteSetup and MenuLink. The SiteSetup model
represents the site's setup, and the MenuLink model represents a link in the
site's menu.
"""
from django.db import models
from utils.model_validators import validate_png
from utils.images import resize_image


class MenuLink(models.Model):
    """
    MenuLink model represents a link in the site's menu.

    Attributes:
        text (str): The text of the menu link.
        url_or_path (str): The URL or path of the menu link.
        new_tab (bool): Whether the link should open in a new tab.

    Returns:
        str: A string representation of the menu link.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    text: str = models.CharField(max_length=50)  # type: ignore
    url_or_path: str = models.CharField(max_length=2048)  # type: ignore
    new_tab: bool = models.BooleanField(default=False)  # type: ignore
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE, blank=True, null=True,
        default=None, related_name='menu',
    )  # type: ignore

    def __str__(self) -> str:
        return str(self.text)


class SiteSetup(models.Model):
    """
    SiteSetup model represents the site's setup.

    Attributes:
        title (str): The title of the site setup.
        description (str): The description of the site setup.
        show_header (bool): Whether to show the header.
        show_search (bool): Whether to show the search.
        show_menu (bool): Whether to show the menu.
        show_description (bool): Whether to show the description.
        show_pagination (bool): Whether to show the pagination.
        show_footer (bool): Whether to show the footer.

    Returns:
        str: A string representation of the site setup.
    """
    class Meta:
        """
        Meta class for Django models.
        """
        verbose_name = 'Setup Blog'
        verbose_name_plural = 'Setup Blog'

    title: str = models.CharField(max_length=65)  # type: ignore
    description: str = models.CharField(max_length=255)  # type: ignore

    show_header: bool = models.BooleanField(default=True)  # type: ignore
    show_search: bool = models.BooleanField(default=True)  # type: ignore
    show_menu: bool = models.BooleanField(default=True)  # type: ignore
    show_description: bool = models.BooleanField(default=True)  # type: ignore
    show_pagination: bool = models.BooleanField(default=True)  # type: ignore
    show_footer: bool = models.BooleanField(default=True)  # type: ignore

    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m/',
        blank=True, default='', validators=[validate_png],
    )

    def save(self, *args, **kwargs):
        """
        Save the object and resize the favicon if it has changed.

        This method overrides the default `save` method to check if the
        favicon has changed. If the favicon has changed, it resizes the
        favicon to a width of 32 pixels.

        Args:
            *args: Positional arguments for the `save` method.
            **kwargs: Keyword arguments for the `save` method.
        """
        current_favicon_name = str(self.favicon.name)
        # print('current_favicon_name', current_favicon_name)
        super().save(*args, **kwargs)
        favicon_changed = False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name

        # print('favicon_changed', favicon_changed)
        if favicon_changed:
            resize_image(self.favicon, 32)

    objects = models.Manager()

    def __str__(self) -> str:
        return str(self.title)
