"""
Tests URL mapping for the blog search view, ensuring it resolves to the
correct view class and renders the expected template.
"""
from django.urls import reverse, resolve
from blog import views
from .test_blog_base import BlogTestBase


class BlogViewsSearchTest(BlogTestBase):
    """
    Test class to verify that blog view functions are mapped correctly to URLs.
    """

    def test_blog_search_uses_correct_view_function(self):
        """
        Verifies that the blog search view function is mapped correctly to the
        'blog:search' URL.
        """
        response = resolve(reverse('blog:search'))
        self.assertIs(response.func.view_class, views.SearchListView)

    def test_blog_search_no_results_found_shows_message(self):
        """
        Tests that searching for a non-existent term displays an appropriate
        message indicating no posts were found.
        """
        url = reverse('blog:search') + '?q=teste'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<h1>Nenhum post encontrado aqui 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_blog_search_empty_query_redirects_to_index(self):
        """
        Tests that an empty search query redirects to the blog index page.
        """
        url = reverse('blog:search') + '?q=+'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('blog:index'))

    def test_blog_search_loads_correct_template(self):
        """
        Tests if the search view loads the correct template.
        """
        response = self.client.get(reverse('blog:index'))
        self.assertTemplateUsed(response, 'blog/base.html')

    def test_blog_search_can_find_recipe_by_title(self):
        """
        Tests if the search view can find a recipe by its title.
        """
        title1 = 'This is post one'
        slug1 = 'this_is_post_one'
        title2 = 'This is post two'
        slug2 = 'this_is_post_two'
        category1 = {'name': 'TestCase one', 'slug': 'test_case_one'}
        category2 = {'name': 'TestCase two', 'slug': 'test_case_two'}
        author = {
            'first_name': 'user',
            'last_name': 'name',
            'username': 'username1',
            'password': '123456',
            'email': 'username@email.com',
        }
        post1 = self.creating_post(
            category_data=category1, title=title1, slug=slug1,
            created_by_data=author
        )
        post2 = self.creating_post(
            category_data=category2, title=title2, slug=slug2,
        )

        search_url = reverse('blog:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(post1, response1.context['posts'])
        self.assertNotIn(post2, response1.context['posts'])

        self.assertIn(post2, response2.context['posts'])
        self.assertNotIn(post1, response2.context['posts'])

        self.assertIn(post1, response_both.context['posts'])
        self.assertIn(post2, response_both.context['posts'])
