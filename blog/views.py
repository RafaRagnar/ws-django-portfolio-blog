"""
This file contains class-based views for managing blog content, including posts
, pages, and search functionality.
"""
import re
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from blog.models import Post, Page


PER_PAGE = 9


class PostListView(ListView):
    """
    Class-based view for displaying a paginated list of published posts.

    This view inherits from Django's `ListView` and provides filtering,
    pagination, sorting, and context data for rendering the list of posts
    in a template.

    Attributes:
        model: The model class representing the posts.
        template_name: The HTML template for rendering the list of posts.
        context_object_name: The name of the context variable containing the
                             posts.
        ordering: The default ordering for the posts (by primary key in
                  descending order).
        paginate_by: The number of posts displayed per page.
        queryset: The queryset of published posts.
    Methods:
        get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            Overrides the default method to add a custom `page_title` to the
            context.
            Returns the context data for the template.
    """
    model: type[Post] = Post
    template_name: str = 'blog/pages/index.html'
    context_object_name: str = 'posts'
    ordering: str = '-pk'
    paginate_by: int = PER_PAGE
    queryset: QuerySet[Post] = Post.objects.get_published()  # type: ignore

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home -'
        return context


class CreateByListView(PostListView):
    """
    Class-based view specifically tailored for displaying posts created by a
    particular user.

    Extends `PostListView` to filter displayed posts based on the provided
    author's primary key. Provides context data including the author's full
    name and a customized page title.

    Attributes:
        _temp_context (dict[str, Any]): Temporary context data storage
        (private).

    Methods:
        __init__(self, **kwargs: Any) -> None:
            Initializes the view and creates a temporary context dictionary.
        get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            Overrides the base class method to incorporate author-specific
            information in the context.
        get_queryset(self) -> QuerySet[Post]:
            Overrides the base class method to filter the queryset based on the
            author's primary key.
            Raises a 404 (Not Found) error if the author is not found.
        get(self, request: HttpRequest, *args: Any,
        **kwargs: Any) -> HttpResponse:
            Handles GET requests, retrieves the author from the request URL,
            and filters the queryset if an author is found. Raises a 404 error
            if the author is not found.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f"{user.first_name} {user.last_name}"
        page_title = 'Posts de ' + user_full_name + ' - '

        ctx.update({'page_title': page_title, })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:  # type: ignore
        qs = super().get_queryset()
        qs = qs.filter(  # type: ignore
            created_by__pk=self._temp_context['user'].pk)
        return qs  # type: ignore

    def get(
            self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            # return redirect('blog:index') if you want to redirect
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    """
    Class-based view for displaying a paginated list of published posts
    filtered by a specific category.

    This view inherits from `PostListView` and further filters the queryset
    based on the provided category slug. It also updates the page title
    to reflect the selected category.

    Attributes:
        allow_empty: Specifies that the view should not allow empty
                     querysets, thus raising a 404 error if no posts
                     are found for the given category.

    Methods:
        get_queryset(self) -> QuerySet[Any]:
            Overrides the parent method to filter the queryset by the
            category slug provided in the URL.
            Returns the filtered queryset of posts.
        get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            Overrides the parent method to add a custom `page_title`
            based on the category name.
            Returns the context data for the template.
    """
    allow_empty: bool = False

    def get_queryset(self) -> QuerySet[Any]:  # type: ignore
        return super().get_queryset().filter(  # type: ignore
            category__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Categoria - '
        ctx.update({'page_title': page_title, })
        return ctx


class TagListView(PostListView):
    """
    Class-based view for displaying a paginated list of published posts
    filtered by a specific tag.

    This view inherits from `PostListView` and further filters the queryset
    based on the provided tag slug. It also updates the page title
    to reflect the selected tag. Additionally, it handles cases where
    no posts are found for the given tag or the tag itself doesn't exist.

    Attributes:
        allow_empty: Specifies that the view should not allow empty
                     querysets, thus raising a 404 error if no posts
                     are found for the given tag.

    Methods:
        get_queryset(self) -> QuerySet[Any]:
            Overrides the parent method to filter the queryset by the
            tag slug provided in the URL.
            Returns the filtered queryset of posts.
        get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            Overrides the parent method to add a custom `page_title`
            based on the tag name and handles cases where the tag
            doesn't exist or no posts are found for that tag.
            Returns the context data for the template.
    """
    allow_empty: bool = False

    def get_queryset(self) -> QuerySet[Any]:  # type: ignore
        return super().get_queryset().filter(  # type: ignore
            tags__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        posts = self.get_queryset()  # Get filtered posts

        if not posts:  # Check if there are any posts
            raise Http404("Nenhum post encontrado com essa tag")

        # Get the first tag object from the first post's tags
        tag_object = posts[0].tags.filter(slug=slug).first()

        if tag_object:
            page_title = f'{tag_object.name} - Tag - '
        else:
            raise Http404("Tag não encontrada")

        ctx.update({'page_title': page_title, })
        return ctx


class SearchListView(PostListView):
    """
    Class-based view for displaying a paginated list of published posts
    filtered by a search query.

    This view inherits from `PostListView` and filters the queryset
    based on the search query provided in the URL. It also updates
    the page title and provides the search query in the context.

    Attributes:
        _search_value: Stores the sanitized search query.

    Methods:
        setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
            Overrides the parent method to extract and sanitize the search
            query from the request.
        get_queryset(self) -> QuerySet[Any]:
            Overrides the parent method to filter the queryset based on
            the search query.
        get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            Overrides the parent method to add a custom `page_title`
            and the search query to the context.
        get(
            self, request: HttpRequest, *args: Any, **kwargs: Any
            ) -> HttpResponse:
            Overrides the default get method to redirect to the home page
            if no search query is provided.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = sanitize_search_query(
            request.GET.get('q', '').strip()
        )
        # self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:  # type: ignore
        search_value = self._search_value
        return super().get_queryset().filter(  # type: ignore
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[0:PER_PAGE]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            'page_title': f'{search_value[:30]} - Search - ',
            'search_value': search_value,
        })
        return ctx

    def get(
            self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)


def sanitize_search_query(query: str) -> str:
    """
    Sanitizes a search query string to improve search functionality and
    security.

    This function performs the following actions:

    1. **Replaces special characters:** It replaces all characters that are
    not alphanumeric (letters, numbers, and underscores) or whitespace with
    spaces. This helps prevent unexpected behavior in search results and
    reduces the risk of security vulnerabilities like cross-site scripting
    (XSS) attacks.
    2. **Removes extra spaces:** It removes any extra spaces that may be
    present in the query string. This ensures consistency and improves the
    readability of the search query.
    3. **Converts to lowercase:** It converts all characters in the query
    string to lowercase. This makes the search case-insensitive, improving
    the user experience by matching searches regardless of capitalization.

    Args:
        query (str): The search query string to be sanitized.

    Returns:
        str: The sanitized search query string.
    """
    query = re.sub(r'[^\w\s]', ' ', query)
    query = ' '.join(query.lower().split())
    return query


class PageDetailView(DetailView):
    """
    Displays the details of an individual page in a blog.

    This class inherits from Django's `DetailView` and is used to manage the
    display of specific pages. It retrieves the page based on the `slug`,
    filters to show only published pages, sets the page title, and passes
    relevant data to the HTML template.

    Attributes:
        model (Model): Defines the model managed by the view, in this case,
        `Page`.
        template_name (str): Specifies the HTML template used for rendering.
        slug_field (str): Indicates the field used to look up the individual
                        page. By default, `DetailView` uses the `pk` field
                        (primary key), but here you explicitly define that the
                        `slug` field should be used.
        context_object_name (str): Defines the name of the context variable
                                used to access the page object in the template.

    Methods:
        get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            This method is called to add context data to the template. It
            retrieves the default context from the parent class, retrieves the
            page object using `self.get_object()`, constructs the page title,
            and updates the context with the `page_title`. Returns the updated
            context.

        get_queryset(self) -> QuerySet[Any]:
            This method is called to filter the query result set. It retrieves
            the default result set from the parent class and filters the result
            set to include only published pages (`filter(is_published=True)`).
            Returns the filtered result set.
    """
    model: type[Page] = Page
    template_name: str = 'blog/pages/page.html'
    slug_field: str = 'slug'
    context_object_name: str = 'page'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_obj = self.get_object()
        page_title = f'{page_obj.title} - Página - '
        ctx.update({'page_title': page_title, })

        return ctx

    def get_queryset(self) -> QuerySet[Any]:  # type: ignore
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    """
    Displays the details of an individual blog post.

    This class inherits from Django's `DetailView` and is used to manage the
    display of specific blog posts. It retrieves the post based on the `slug`,
    filters to show only published posts, sets the page title, and passes
    relevant data to the HTML template.

    Attributes:
        model (Type[Post]): Defines the model managed by the view, in this case
                            , `Post`. Specifying the type using `Type[Post]`
                            improves type checking.
        template_name (str): Specifies the HTML template used for rendering the
                            post details.
        slug_field (str): Indicates the field used to look up the specific post
                        By default, `DetailView` uses the `pk` field (primary
                        key), but here you're explicitly defining `slug`.
        context_object_name (str): Defines the name of the context variable
                        used to access the post object in the template.

    Methods:
        get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            This method is called to add additional data to the context
            dictionary that will be passed to the template. It retrieves the
            default context from the parent class, retrieves the current post
            object, constructs the page title, updates the context with the
            `page_title`, and returns the updated context.

        get_queryset(self) -> QuerySet[Post]:  # Corrected type annotation
            This method is called to filter the queryset of posts. It retrieves
            the default queryset from the parent class, filters the queryset to
            include only published posts, and returns the filtered queryset.
            The type annotation is corrected to `QuerySet[Post]` to reflect the
            actual content.
    """
    model: type[Post] = Post
    template_name: str = 'blog/pages/post.html'
    slug_field: str = 'slug'
    context_object_name: str = 'post'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        post_obj = self.get_object()
        page_title = f'{post_obj.title} - Post - '
        ctx.update({'page_title': page_title, })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:  # type: ignore
        return super().get_queryset().filter(is_published=True)
