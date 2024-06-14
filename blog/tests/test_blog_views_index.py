"""
Tests URL mapping for the blog index view, ensuring it resolves to the correct
view class and renders the expected template.
"""
from django.urls import reverse, resolve
from blog import views
from .test_blog_base import BlogTestBase


class BlogViewsIndexTest(BlogTestBase):
    """
    Tests the URL mapping for the blog index view.
    """

    def test_index_view_function_is_correct(self):
        """
        Verifies that the blog index view function is mapped correctly to the
        'blog:index' URL.
        """
        view = resolve(reverse('blog:index'))
        self.assertIs(view.func.view_class, views.PostListView)

    def test_index_view_returns_status_code_200(self):
        """
        Tests if the index view returns status code 200.
        """
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_loads_template(self):
        """
        Tests if the index view loads the correct template.
        """
        response = self.client.get(reverse('blog:index'))
        self.assertTemplateUsed(response, 'blog/pages/index.html')

    def test_index_shows_no_posts_message(self):
        """
        Tests if the index template displays "No posts found" message when
        there are no published posts.
        """
        response = self.client.get(reverse('blog:index'))
        self.assertIn(
            '<h1>Nenhum post encontrado aqui 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_index_template_loads_post(self):
        """
        Tests if the index template loads the post correctly when a published
        post exists.
        """
        self.creating_post()
        response = self.client.get(reverse('blog:index'))
        response_content = response.content.decode('utf-8')
        response_context_post = response.context['posts']
        self.assertEqual(len(response_context_post), 1)
        self.assertEqual(response_context_post.first().title, 'Post Title')
        self.assertIn('Post Title', response_content)
        self.assertIn('post_title', response_content)
        self.assertIn('Post excerpt', response_content)

    def test_index_does_not_load_unpublished_post(self):
        """
        Tests if the index template does not display a post if it's not
        published.
        """
        self.creating_post(is_published=False)

        response = self.client.get(reverse('blog:index'))
        response_content = response.content.decode('utf-8')

        self.assertIn(
            '<h1>Nenhum post encontrado aqui 🥲</h1>',
            response_content
        )
