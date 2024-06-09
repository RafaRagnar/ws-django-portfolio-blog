"""
This test class validates that URL patterns defined in the blog application
resolve to the correct view classes using Django's `reverse` and `resolve`
functions.

- `reverse` takes a named URL pattern and any required arguments as keywords,
  and returns the corresponding absolute URL.
- `resolve` takes a URL and returns the URL pattern (including the view
  function) that matches that URL.

These tests ensure that the URL patterns in your blog app's `urls.py` file map
to the intended view classes. Each test method follows a similar structure:

1. It defines a clear test name, indicating the specific URL pattern being
   tested.
2. It uses `reverse` to generate the URL for the corresponding named view.
3. It uses `resolve` to retrieve the view function associated with the
   generated URL.
4. It asserts that the resolved view function's class is the expected view
   class using `self.assertIs(view.func.view_class, ExpectedViewClass)`.

By including a comprehensive docstring, you make your test suite more
informative, maintainable, and collaborative for other developers working on
the project.

Additional Considerations:
- You might consider mentioning the specific `views.py` file containing the
  tested view classes for better context.

Note: Ensure that the view classes (`ExpectedViewClass`) are correctly imported
from your `views.py` file.
"""
from django.test import TestCase
from django.urls import reverse, resolve
from blog import views


class BlogViewsTest(TestCase):
    """
    Test class to verify that blog view functions are mapped correctly to URLs.
    """

    def test_blog_index_view_function_is_correct(self):
        """
        Verifies that the blog index view function is mapped correctly to the
        'blog:index' URL.
        """
        view = resolve(reverse('blog:index'))
        self.assertIs(view.func.view_class, views.PostListView)

    def test_blog_post_view_function_is_correct(self):
        """
        Verifies that the blog post view function is mapped correctly to the
        'blog:post' URL with a slug.
        """
        view = resolve(reverse('blog:post', kwargs={'slug': 'teste_post'}))
        self.assertIs(view.func.view_class, views.PostDetailView)

    def test_blog_page_view_function_is_correct(self):
        """
        Verifies that the blog page view function is mapped correctly to the
        'blog:page' URL with a slug.
        """
        view = resolve(reverse('blog:page', kwargs={'slug': 'teste_page'}))
        self.assertIs(view.func.view_class, views.PageDetailView)

    def test_blog_created_by_view_function_is_correct(self):
        """
        Verifies that the blog posts by author view function is mapped
        correctly to the 'blog:created_by' URL with an author primary key.
        """
        view = resolve(reverse('blog:created_by', kwargs={'author_pk': 1}))
        self.assertIs(view.func.view_class, views.CreateByListView)

    def test_blog_category_view_function_is_correct(self):
        """
        Verifies that the blog posts by category view function is mapped
        correctly to the 'blog:category' URL with a slug.
        """
        view = resolve(reverse(
            'blog:category', kwargs={'slug': 'teste_category'}
        ))
        self.assertIs(view.func.view_class, views.CategoryListView)

    def test_blog_tag_view_function_is_correct(self):
        """
        Verifies that the blog posts by tag view function is mapped correctly
        to the 'blog:tag' URL with a slug.
        """
        view = resolve(reverse('blog:tag', kwargs={'slug': 'teste_tag'}))
        self.assertIs(view.func.view_class, views.TagListView)

    def test_blog_search_view_function_is_correct(self):
        """
        Verifies that the blog search view function is mapped correctly to the
        'blog:search' URL.
        """
        view = resolve(reverse('blog:search'))
        self.assertIs(view.func.view_class, views.SearchListView)
