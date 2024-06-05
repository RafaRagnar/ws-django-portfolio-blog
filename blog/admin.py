from django.contrib import admin
from blog.models import Tag, Category


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
