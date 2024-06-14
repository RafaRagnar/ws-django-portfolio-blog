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
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page'),
    path(
        'created_by/<int:author_pk>/',
        views.CreateByListView.as_view(), name='created_by'
    ),
    path(
        'category/<slug:slug>/',
        views.CategoryListView.as_view(), name='category'
    ),
    path('tag/<slug:slug>/', views.TagListView.as_view(), name='tag'),
]
