"""
Tests that the URL patterns defined in the blog application's `urls.py` file
are reversed correctly using Django's `reverse` function. Each test checks if
the generated URL matches the expected path.
"""
from django.test import TestCase
from django.urls import reverse


class BlogURLsTest(TestCase):
    """
    Tests that URL patterns in the blog application are reversed correctly.
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
