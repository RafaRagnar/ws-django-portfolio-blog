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
from django.urls import reverse, resolve
from blog import views
from .test_blog_base import BlogTestBase


class BlogViewsTest(BlogTestBase):
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

    def test_blog_index_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

    def test_blog_index_view_loads_correct_template(self):
        response = self.client.get(reverse('blog:index'))
        self.assertTemplateUsed(response, 'blog/pages/index.html')

    def test_blog_index_template_shows_no_posts_found_if_on_the_blog(self):
        response = self.client.get(reverse('blog:index'))
        self.assertIn(
            '<h1>Nenhum post encontrado aqui 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_blog_index_template_loads_post(self):
        self.creating_post()
        response = self.client.get(reverse('blog:index'))
        response_content = response.content.decode('utf-8')
        response_context_post = response.context['posts']
        self.assertEqual(len(response_context_post), 1)
        self.assertEqual(response_context_post.first().title, 'Post Title')
        self.assertIn('Post Title', response_content)
        self.assertIn('post_title', response_content)
        self.assertIn('Post excerpt', response_content)

    def test_blog_index_template_dont_load_post_not_published(self):
        """Test for template post is_published equal to false do not show"""
        self.creating_post(is_published=False)

        response = self.client.get(reverse('blog:index'))
        response_content = response.content.decode('utf-8')

        self.assertIn(
            '<h1>Nenhum post encontrado aqui 🥲</h1>',
            response_content
        )

    def test_post_detail_view_function_is_correct(self):
        """
        Verifies that the blog post view function is mapped correctly to the
        'blog:post' URL with a slug.
        """
        view = resolve(reverse('blog:post', kwargs={'slug': 'teste_post'}))
        self.assertIs(view.func.view_class, views.PostDetailView)

    def test_post_detail_view_returns_404_if_no_post_found(self):
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': 'teste_post'})
        )
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_returns_status_code_200_ok(self):
        post = self.creating_post()
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': post.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_post_detail_template_loads_the_correct_post(self):
        """
        Test whether view 'post_detail' render the correct template
        and passes the expected context.
        """
        needed_title = 'This is a detail post - It load one post'
        needed_slug = 'this_is_a_detail_post'
        post = self.creating_post(title=needed_title, slug=needed_slug)
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': needed_slug})
        )
        # response = self.client.get(f'http://127.0.0.1:8000/post/{post.slug}/')
        response_content = response.content.decode('utf-8')
        response_context_post = response.context['post']

        self.assertTemplateUsed(response, 'blog/pages/post.html')
        self.assertIn(needed_title, response_content)
        self.assertEqual(response_context_post, post)

    def test_post_detail_template_dont_load_post_not_published(self):
        """Test for template post is_published equal to false do not show"""
        post = self.creating_post(is_published=False)
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': post.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_page_detail_view_function_is_correct(self):
        """
        Verifies that the blog page view function is mapped correctly to the
        'blog:page' URL with a slug.
        """
        view = resolve(reverse('blog:page', kwargs={'slug': 'teste_page'}))
        self.assertIs(view.func.view_class, views.PageDetailView)

    def test_page_detail_view_returns_404_if_no_page_found(self):
        response = self.client.get(reverse(
            'blog:post', kwargs={'slug': 'teste_page'})
        )
        self.assertEqual(response.status_code, 404)

    def test_page_detail_view_returns_status_code_200_ok(self):
        page = self.creating_page()
        response = self.client.get(reverse(
            'blog:page', kwargs={'slug': page.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_page_detail_template_loads_the_correct_page(self):
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

    def test_page_detail_template_dont_load_page_not_published(self):
        page = self.creating_page(is_published=False)
        response = self.client.get(reverse(
            'blog:page', kwargs={'slug': page.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_blog_created_by_view_function_is_correct(self):
        """
        Verifies that the blog posts by author view function is mapped
        correctly to the 'blog:created_by' URL with an author primary key.
        """
        view = resolve(reverse('blog:created_by', kwargs={'author_pk': 1}))
        self.assertIs(view.func.view_class, views.CreateByListView)

    def test_blog_created_by_returns_404_if_no_created_by_found(self):
        response = self.client.get(
            reverse('blog:created_by', kwargs={'author_pk': 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_created_by_view_returns_status_code_200_ok(self):
        created_by = self.creating_author()
        response = self.client.get(
            reverse('blog:created_by', kwargs={'author_pk': created_by.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_created_by_template_loads_the_correct_created_by(self):
        created_by = self.creating_post()
        response = self.client.get(
            reverse('blog:created_by', args=(1,))
        )
        response_content = response.content.decode('utf-8')
        # response_context_created_by = response.context['created_by']

        self.assertTemplateUsed(response, 'blog/pages/index.html')
        self.assertIn('user name', response_content)
        self.assertEqual(response.context['post'], created_by)

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
        response = self.client.get(
            reverse('blog:category', kwargs={'slug': 'teste_category'})
        )
        self.assertEqual(response.status_code, 404)

    def test_blog_category_view_returns_status_code_200_ok(self):
        post = self.creating_post()
        response = self.client.get(reverse(
            'blog:category', kwargs={'slug': post.category.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_blog_category_template_loads_the_correct_category(self):
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

    def test_blog_tag_view_function_is_correct(self):
        """
        Verifies that the blog posts by tag view function is mapped correctly
        to the 'blog:tag' URL with a slug.
        """
        view = resolve(reverse('blog:tag', kwargs={'slug': 'teste_tag'}))
        self.assertIs(view.func.view_class, views.TagListView)

    def test_blog_tag_returns_404_if_no_tag_found(self):
        response = self.client.get(
            reverse('blog:tag', kwargs={'slug': 'teste_tag'})
        )
        self.assertEqual(response.status_code, 404)

    # def test_tag_view_returns_status_code_200_ok(self):
    #     tag = self.creating_tag()
    #     response = self.client.get(
    #         reverse('blog:tag', kwargs={'slug': tag.slug})
    #     )
    #     self.assertEqual(response.status_code, 200)

    def test_blog_search_view_function_is_correct(self):
        """
        Verifies that the blog search view function is mapped correctly to the
        'blog:search' URL.
        """
        view = resolve(reverse('blog:search'))
        self.assertIs(view.func.view_class, views.SearchListView)

    def test_blog_search_view_loads_correct_template(self):
        response = self.client.get(reverse('blog:search') + '?search=teste')
        ...
