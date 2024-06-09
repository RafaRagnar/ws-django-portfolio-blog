"""
This test class validates that the URL patterns defined in the blog application
are reversed correctly using the `reverse` function from Django's `django.urls`
module.

The `reverse` function takes a named URL pattern and any required arguments as
keywords, and returns the corresponding absolute URL. These tests ensure that
the URL patterns you've defined in your blog app's `urls.py` file map to the
expected URLs when reversed.

Each test function follows a similar structure:

- It defines a clear test name, indicating the specific URL pattern being
tested.
- It uses `reverse` to generate the URL for the corresponding named view.
- It asserts that the generated URL matches the expected path using
`self.assertEqual`.

These tests provide essential confidence in your application's URL routing
mechanism, guaranteeing that users can access different sections of your blog
using the correct URLs.
"""
from django.test import TestCase
from django.urls import reverse


class BlogURLsTest(TestCase):
    """
    This test class validates that the URL patterns defined in the blog
    application are reversed correctly using the `reverse` function from
    Django's `django.urls` module.
    """

    def test_blog_index_url_is_correct(self):
        '''Tests that the URL for the blog index view is reversed correctly.'''
        url = reverse('blog:index')
        self.assertEqual(url, '/')

    def test_blog_post_url_is_correct(self):
        '''
        Tests that the URL for a specific blog post is reversed correctly.
        '''
        url = reverse('blog:post', kwargs={'slug': 'teste_post'})
        self.assertEqual(url, '/post/teste_post/')

    def test_blog_page_url_is_correct(self):
        '''
        Tests that the URL for a specific blog page is reversed correctly.
        '''
        url = reverse('blog:page', kwargs={'slug': 'teste_page'})
        self.assertEqual(url, '/page/teste_page/')

    def test_blog_created_by_url_is_correct(self):
        '''
        Tests that the URL for filtering posts by author is reversed correctly.
        '''
        url = reverse('blog:created_by', kwargs={'author_pk': 1})
        self.assertEqual(url, '/created_by/1/')

    def test_blog_category_url_is_correct(self):
        '''
        Tests that the URL for filtering posts by category is reversed
        correctly.
        '''
        url = reverse('blog:category', kwargs={'slug': 'teste_category'})
        self.assertEqual(url, '/category/teste_category/')

    def test_blog_tag_url_is_correct(self):
        '''
        Tests that the URL for filtering posts by tag is reversed correctly.
        '''
        url = reverse('blog:tag', kwargs={'slug': 'teste_tag'})
        self.assertEqual(url, '/tag/teste_tag/')

    def test_blog_search_url_is_correct(self):
        '''
        Tests that the URL for the blog search view is reversed correctly.
        '''
        url = reverse('blog:search')
        self.assertEqual(url, '/search/')
