from django.contrib import admin
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
class PageAdmin(admin.ModelAdmin):
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
    list_display: tuple = ('id', 'title', 'is_published')
    list_display_links: tuple = ('title',)
    search_fields: tuple = ('id', 'slug', 'title', 'content')
    list_per_page: int = 50
    list_filter: tuple = ('is_published',)
    list_editable: tuple = ('is_published',)
    ordering: tuple = ('-id',)
    prepopulated_fields: dict = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
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
    """
    list_display: tuple = ('id', 'title', 'is_published', 'created_by')
    list_display_links: tuple = ('title',)
    search_fields: tuple = ('id', 'slug', 'title', 'excerpt', 'content')
    list_per_page: int = 50
    list_filter: tuple = ('category', 'is_published')
    list_editable: tuple = ('is_published',)
    ordering: tuple = ('-id',)
    readonly_fields: tuple = (
        'created_at', 'updated_at', 'created_by', 'updated_by'
    )
    prepopulated_fields: dict = {'slug': ('title',)}
    autocomplete_fields: tuple = ('category', 'tags')
