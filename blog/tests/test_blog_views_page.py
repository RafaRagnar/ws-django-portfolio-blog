"""
Tests URL mapping for the blog page detail view, ensuring it resolves to the
correct view class and renders the expected template.
"""
from django.urls import reverse, resolve
from blog import views
from .test_blog_base import BlogTestBase


class BlogViewsPageTest(BlogTestBase):
    """
    Tests the URL mapping for the blog page detail view.
    """

    def test_page_detail_view_function_is_correct(self):
        """
        Verifies that the blog page view function is mapped correctly to the
        'blog:page' URL with a slug.
        """
        view = resolve(reverse('blog:page', kwargs={'slug': 'teste_page'}))
        self.assertIs(view.func.view_class, views.PageDetailView)

    def test_page_detail_view_returns_404_if_not_found(self):
        """
        Tests if the page detail view returns 404 when no page is found for the
        given slug.
        """
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': 'teste_page'})
        )
        self.assertEqual(response.status_code, 404)

    def test_page_detail_view_returns_status_code_200(self):
        """
        Tests if the page detail view returns status code 200 when a valid page
        slug is provided.
        """
        page = self.creating_page()
        response = self.client.get(reverse(
            'blog:page', kwargs={'slug': page.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_page_detail_template_loads_correct_page(self):
        """
        Tests if the page detail template loads the correct page based on the
        slug.
        """
        needed_title = 'This is a detail page - It load one page'
        needed_slug = 'this_is_a_detail_page'
        page = self.creating_page(
            title=needed_title, slug=needed_slug)
        response = self.client.get(reverse(
            'blog:page', kwargs={'slug': page.slug})
        )
        response_content = response.content.decode('utf-8')
        response_context_page = response.context['page']

        self.assertTemplateUsed(response, 'blog/pages/page.html')
        self.assertIn(needed_title, response_content)
        self.assertEqual(response_context_page, page)

    def test_page_detail_view_returns_404_for_unpublished_page(self):
        """
        Tests if the page detail view returns 404 when trying to access an
        unpublished page.
        """
        page = self.creating_page(is_published=False)
        response = self.client.get(reverse(
            'blog:page', kwargs={'slug': page.slug})
        )
        self.assertEqual(response.status_code, 404)
