"""
Tests URL mapping for blog views related to posts created by a specific author.
Ensures they resolve to the correct view classes.
"""
from django.urls import reverse, resolve
from blog import views
from .test_blog_base import BlogTestBase


class BlogViewsCreatedByTest(BlogTestBase):
    """
    Tests the URL mapping for the blog views related to posts created by a
    specific author.
    """

    def test_blog_created_by_view_function_is_correct(self):
        """
        Verifies that the blog posts by author view function is mapped
        correctly to the 'blog:created_by' URL with an author primary key.
        """
        view = resolve(reverse('blog:created_by', kwargs={'author_pk': 1}))
        self.assertIs(view.func.view_class, views.CreateByListView)

    def test_blog_created_by_returns_404_if_no_created_by_found(self):
        """
        Tests if the view returns 404 when no author is found for the provided
        author PK.
        """
        response = self.client.get(
            reverse('blog:created_by', kwargs={'author_pk': 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_created_by_view_returns_status_code_200_ok(self):
        """
        Tests if the view returns status code 200 when a valid author PK is
        provided.
        """
        created_by = self.creating_author()
        response = self.client.get(
            reverse('blog:created_by', kwargs={'author_pk': created_by.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_created_by_template_loads_the_correct_created_by(self):
        """
        Tests if the view template loads the correct author and their posts.
        """
        created_by = self.creating_post()
        response = self.client.get(
            reverse('blog:created_by', args=(1,))
        )
        response_content = response.content.decode('utf-8')
        # response_context_created_by = response.context['created_by']

        self.assertTemplateUsed(response, 'blog/pages/index.html')
        self.assertIn('user name', response_content)
        self.assertEqual(response.context['post'], created_by)
