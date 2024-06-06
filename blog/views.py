# TODO docstring
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import render
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
    queryset: QuerySet[Post] = Post.objects.get_published()

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

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(
            self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            # return redirect('blog:index') caso queira redirecionar
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


def created_by(request, author_pk):
    # TODO docstring
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()

    posts = Post.objects.get_published().filter(created_by__pk=author_pk)
    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'
    page_title = 'Posts de ' + user_full_name + ' - '

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def category(request, slug):
    # TODO docstring
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if len(posts) == 0:
        raise Http404()

    page_title = f'{page_obj[0].category.name} - Categoria - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def tag(request, slug):
    # TODO docstring
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if len(posts) == 0:
        raise Http404()

    page_title = f'{page_obj[0].tags.first().name} - Tag - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def search(request):
    # TODO docstring
    search_value = request.GET.get('search', '').strip()
    posts = Post.objects.get_published().filter(
        Q(title__icontains=search_value) |
        Q(excerpt__icontains=search_value) |
        Q(content__icontains=search_value)
    )[0:PER_PAGE]

    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )


def page(request, slug):
    # TODO docstring
    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()

    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )


def post(request, slug):
    # TODO docstring
    post_obj = Post.objects.get_published().filter(slug=slug).first()

    if post_obj is None:
        raise Http404()

    page_title = f'{post_obj.title} - Página - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
