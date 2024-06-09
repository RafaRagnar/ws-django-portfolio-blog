"""
This module defines custom admin interfaces for the blog application models:

- TagAdmin: Allows administrators to view and edit tag information.
- CategoryAdmin: Allows administrators to view and edit category information.
- PageAdmin: Allows administrators to view and edit page information.
- PostAdmin: Allows administrators to view and edit post information, including
  overriding the `save_model` method to set `created_by` and `updated_by`
  fields.

These admin interfaces provide a user-friendly way for administrators to manage
blog content and settings.
"""
from typing import Any
from django.contrib import admin
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin  # type: ignore
from blog.models import Tag, Category, Page, Post


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Tag model.

    This class defines a custom admin interface for the Tag model, which
    allows administrators to view and edit tag information.

    Attributes:
        list_display (tuple): A tuple of field names to display in the list
        view.
        list_display_links (tuple): A tuple of field names to use as links in
        the list view.
        search_fields (tuple): A tuple of field names to use for searching.
        list_per_page (int): The number of items to display per page in the
        list view.
        ordering (tuple): A tuple of field names to use for ordering the list
        view.
        prepopulated_fields (dict): A dictionary of field names to use for
        prepopulating fields in the form view.
    """
    list_display: tuple = ('id', 'name', 'slug')
    list_display_links: tuple = ('name',)
    search_fields: tuple = ('id', 'name', 'slug')
    list_per_page: int = 10
    ordering: tuple = ('-id',)
    prepopulated_fields: dict = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Category model.

    This class defines a custom admin interface for the Category model, which
    allows administrators to view and edit category information.

    Attributes:
        list_display (tuple): A tuple of field names to display in the list
        view.
        list_display_links (tuple): A tuple of field names to use as links in
        the list view.
        search_fields (tuple): A tuple of field names to use for searching.
        list_per_page (int): The number of items to display per page in the
        list view.
        ordering (tuple): A tuple of field names to use for ordering the list
        view.
        prepopulated_fields (dict): A dictionary of field names to use for
        prepopulating fields in the form view.
    """
    list_display: tuple = ('id', 'name', 'slug')
    list_display_links: tuple = ('name',)
    search_fields: tuple = ('id', 'name', 'slug')
    list_per_page: int = 10
    ordering: tuple = ('-id',)
    prepopulated_fields: dict = {'slug': ('name',)}


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    """
    Custom admin interface for the Page model.

    This class defines a custom admin interface for the Page model, which
    allows administrators to view and edit page information.

    Attributes:
        list_display (tuple): A tuple of field names to display in the list
        view.
        list_display_links (tuple): A tuple of field names to use as links in
        the list view.
        search_fields (tuple): A tuple of field names to use for searching.
        list_per_page (int): The number of items to display per page in the
        list view.
        list_filter (tuple): A tuple of field names to use for filtering the
        list view.
        list_editable (tuple): A tuple of field names to make editable in the
        list view.
        ordering (tuple): A tuple of field names to use for ordering the list
        view.
        prepopulated_fields (dict): A dictionary of field names to use for
        prepopulating fields in the form view.
    """
    summernote_fields = ('content',)
    list_display: tuple = ('id', 'title', 'is_published')
    list_display_links: tuple = ('title',)
    search_fields: tuple = ('id', 'slug', 'title', 'content')
    list_per_page: int = 50
    list_filter: tuple = ('is_published',)
    list_editable: tuple = ('is_published',)
    ordering: tuple = ('-id',)
    prepopulated_fields: dict = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Custom admin interface for the Post model.

    This class defines a custom admin interface for the Post model, which
    allows administrators to view and edit post information.

    Attributes:
        list_display (tuple): A tuple of field names to display in the list
            view.
        list_display_links (tuple): A tuple of field names to use as links in
            the list view.
        search_fields (tuple): A tuple of field names to use for searching.
        list_per_page (int): The number of items to display per page in the
            list view.
        list_filter (tuple): A tuple of field names to use for filtering the
            list view.
        list_editable (tuple): A tuple of field names to make editable in the
            list view.
        ordering (tuple): A tuple of field names to use for ordering the list
            view.
        readonly_fields (tuple): A tuple of field names to make read-only in
            the form view.
        prepopulated_fields (dict): A dictionary of field names to use for
            prepopulating fields in the form view.
        autocomplete_fields (tuple): A tuple of field names to use for
            autocompleting fields in the form view.

    Methods:
        save_model(request, obj, form, change)
            Override the default save method to set the created_by and
            updated_by fields.
    """
    summernote_fields = ('content',)
    list_display: tuple = ('id', 'title', 'is_published', 'created_by')
    list_display_links: tuple = ('title',)
    search_fields: tuple = ('id', 'slug', 'title', 'excerpt', 'content')
    list_per_page: int = 50
    list_filter: tuple = ('category', 'is_published')
    list_editable: tuple = ('is_published',)
    ordering: tuple = ('-id',)
    readonly_fields: tuple = (
        'created_at', 'updated_at', 'created_by', 'updated_by', 'link'
    )
    prepopulated_fields: dict = {'slug': ('title',)}
    autocomplete_fields: tuple = ('category', 'tags')

    def link(self, obj):
        """
        Generates an HTML link to the detail page of a given object.

        This method is likely used within a template context to create
        clickable links for objects (e.g., posts) rendered in the template.
        """
        if not obj.pk:
            return '-'

        url_of_post = obj.get_absolute_url()
        safe_link = mark_safe(
            f'<a target="_blank" href="{url_of_post}">Ver post</a>'
        )

        return safe_link

    def save_model(
            self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        obj.save()
