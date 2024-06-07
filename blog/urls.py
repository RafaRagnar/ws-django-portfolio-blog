"""
Defines URL patterns for the blog application.

This module maps URL paths to corresponding views in the `blog.views` module.
It handles various functionalities, including:

- Displaying a list of published posts (index view)
- Showing detailed information about a specific post (PostDetailView)
- Displaying the content of a static page (PageDetailView)
- Filtering posts by author (CreateByListView)
- Listing posts within a specific category (CategoryListView)
- Grouping posts by tag (TagListView)
- Providing search functionality for posts (SearchListView)

The `app_name` variable is set to 'blog' for easier namespacing of URLs.
"""
from django.urls import path
from blog.views import (PostDetailView, PageDetailView, CategoryListView,
                        TagListView, SearchListView, PostListView,
                        CreateByListView)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path(
        'created_by/<int:author_pk>/',
        CreateByListView.as_view(), name='created_by'
    ),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
    path('search/', SearchListView.as_view(), name='search'),
]
