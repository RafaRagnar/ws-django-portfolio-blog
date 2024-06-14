"""
Tests URL mapping for the blog post detail view, ensuring it resolves to the
correct view class and renders the expected template.
"""
from django.urls import reverse, resolve
from blog import views
from .test_blog_base import BlogTestBase


class BlogViewsPostTest(BlogTestBase):
    """
    Tests the URL mapping for the blog post detail view.
    """

    def test_post_detail_view_function_is_correct(self):
        """
        Verifies that the blog post view function is mapped correctly to the
        'blog:post' URL with a slug.
        """
        view = resolve(reverse('blog:post', kwargs={'slug': 'teste_post'}))
        self.assertIs(view.func.view_class, views.PostDetailView)

    def test_post_detail_view_returns_404_if_not_found(self):
        """
        Tests if the post detail view returns 404 when no post is found for
        the given slug.
        """
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': 'teste_post'})
        )
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_returns_status_code_200(self):
        """
        Tests if the post detail view returns status code 200 when a valid
        post slug is provided.
        """
        post = self.creating_post()
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': post.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_post_detail_template_loads_correct_post(self):
        """
        Tests if the post detail template loads the correct post based on the
        slug.
        """
        needed_title = 'This is a detail post - It load one post'
        needed_slug = 'this_is_a_detail_post'
        post = self.creating_post(title=needed_title, slug=needed_slug)
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': needed_slug})
        )
        # response = self.client.get(f'http://127.0.0.1:8000/post/{post.slug}
        # /')
        response_content = response.content.decode('utf-8')
        response_context_post = response.context['post']

        self.assertTemplateUsed(response, 'blog/pages/post.html')
        self.assertIn(needed_title, response_content)
        self.assertEqual(response_context_post, post)

    def test_post_detail_view_returns_404_for_unpublished_post(self):
        """
        Tests if the post detail view returns 404 when trying to access an
        unpublished post.
        """
        post = self.creating_post(is_published=False)
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': post.slug})
        )
        self.assertEqual(response.status_code, 404)
