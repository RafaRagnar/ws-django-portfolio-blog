from django.contrib import admin
from django.http import HttpRequest
from site_setup.models import MenuLink, SiteSetup


# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     """
#     Custom admin interface for the MenuLink model.

#     This class defines a custom admin interface for the MenuLink model, which
#     allows administrators to view and edit menu link information.
#     """
#     list_display: tuple = ('id', 'text', 'url_or_path')
#     list_display_links: tuple = ('id', 'text', 'url_or_path')
#     search_fields: tuple = ('id', 'text', 'url_or_path')


class MenuLinkInline(admin.TabularInline):
    """
    MenuLinkInline class for displaying MenuLink objects in the admin
    interface.
    """
    model = MenuLink
    extra: int = 1


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the SiteSetup model.

    This class defines a custom admin interface for the SiteSetup model, which
    allows administrators to view and edit site setup information.
    """
    list_display: tuple = ('title', 'description')
    inlines: tuple = (MenuLinkInline,)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Returns a boolean indicating whether the user has permission to add
        a new SiteSetup object.
        """
        return not SiteSetup.objects.exists()
