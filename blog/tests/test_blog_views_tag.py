"""
Tests URL mapping for the blog tag view, ensuring it resolves to the correct
view class.
"""
from django.urls import reverse, resolve
from blog import views
from .test_blog_base import BlogTestBase


class BlogViewsTagTest(BlogTestBase):
    """
    Tests the URL mapping for the blog tag view.
    """

    def test_blog_tag_view_function_is_correct(self):
        """
        Verifies that the blog posts by tag view function is mapped correctly
        to the 'blog:tag' URL with a slug.
        """
        view = resolve(reverse('blog:tag', kwargs={'slug': 'teste_tag'}))
        self.assertIs(view.func.view_class, views.TagListView)

    def test_blog_tag_returns_404_if_not_found(self):
        """
        Tests if the tag view returns 404 when no tag is found for the given
        slug.
        """
        response = self.client.get(
            reverse('blog:tag', kwargs={'slug': 'teste_tag'})
        )
        self.assertEqual(response.status_code, 404)
