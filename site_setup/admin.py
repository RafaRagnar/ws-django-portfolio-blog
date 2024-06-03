from django.contrib import admin
from site_setup.models import MenuLink


@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'text', 'url_or_path')
    list_display_links = ('id', 'text', 'url_or_path')
    search_fields: tuple = ('id', 'text', 'url_or_path')
