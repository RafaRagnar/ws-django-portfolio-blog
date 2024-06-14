"""
This test class validates that the URL patterns defined in the `blog`
application resolve to the correct view classes using Django's `reverse` and
`resolve` functions. Each test method checks if the URL pattern maps to the
intended view class.
"""
from django.urls import reverse, resolve
from blog import views
from .test_blog_base import BlogTestBase


class BlogViewsCategoryTest(BlogTestBase):
    """
    Tests the URL mapping for the blog category views.
    """

    def test_blog_category_view_function_is_correct(self):
        """
        Verifies that the blog posts by category view function is mapped
        correctly to the 'blog:category' URL with a slug.
        """
        view = resolve(reverse(
            'blog:category', kwargs={'slug': 'teste_category'}
        ))
        self.assertIs(view.func.view_class, views.CategoryListView)

    def test_blog_category_returns_404_if_no_category_found(self):
        """
        Tests if the category view returns 404 when no category is found.
        """
        response = self.client.get(
            reverse('blog:category', kwargs={'slug': 'teste_category'})
        )
        self.assertEqual(response.status_code, 404)

    def test_blog_category_view_returns_status_code_200_ok(self):
        """
        Tests if the category view returns status code 200 when a valid
        category is provided.
        """
        post = self.creating_post()
        response = self.client.get(reverse(
            'blog:category', kwargs={'slug': post.category.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_blog_category_template_loads_the_correct_category(self):
        """
        Tests if the category view template loads the correct category name
        and posts associated with it.
        """
        needed_name = (
            'This is a category - Loads all posts with the selected category')
        needed_slug = 'this_is_a_category'
        category = {'name': needed_name, 'slug': needed_slug}
        post = self.creating_post(category_data=category)
        response = self.client.get(reverse(
            'blog:category', kwargs={'slug': post.category.slug})
        )
        self.assertTemplateUsed(response, 'blog/pages/index.html')
        self.assertIn(needed_name, response.content.decode('utf-8'))
        self.assertEqual(
            response.context['posts'].first().category.name, needed_name)
