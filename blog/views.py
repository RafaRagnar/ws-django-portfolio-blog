# TODO docstring
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
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
    """
    model: type[Post] = Post
    template_name: str = 'blog/pages/index.html'
    context_object_name: str = 'posts'
    ordering: str = '-pk'
    paginate_by: int = PER_PAGE
    queryset: QuerySet[Post] = Post.objects.get_published()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Returns the context data for the template, including the page title.

        This method overrides the default behavior to add a custom `page_title`
        to the context.

        Args:
            kwargs: Keyword arguments passed to the method.

        Returns:
            A dictionary containing the context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home -'
        return context

    # def get_queryset(self) -> QuerySet[Any]:
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset

# def index(request):
#     # TODO docstring
#     posts = Post.objects.get_published()

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         }
#     )


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
