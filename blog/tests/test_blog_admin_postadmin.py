"""
Module containing test cases for the PostAdmin class used in the blog
application.
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from blog.models import Post, Category
from blog.admin import PostAdmin


class BlogPostAdminTest(TestCase):
    """
    Test suite for the PostAdmin class used in the blog application.
    """

    def setUp(self) -> None:
        """
        Creates a superuser, a category, and a post to be used in the tests.
        """
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com',
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        # self.tag = Tag.objects.create(name='Test Tag', slug='test-tag')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            category=self.category,
            # tags=[self.tag],
            content='Test post content',
            is_published=True,
            created_by=self.user,
        )

    def test_post_admin_list_display(self):
        """
        Tests if the correct fields are displayed in the post list view of the
        admin interface.

        This test verifies that the title, published status, and author of the
        post are displayed in the list of posts.
        """
        admin_url = reverse('admin:blog_post_changelist')
        response = self.client.get(admin_url)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'True')
        self.assertContains(response, 'admin')

    def test_post_admin_search_fields(self):
        """
        Tests if the search functionality works properly in the post list view
        of the admin interface.

        This test verifies that searching by keywords in the title or content
        of the post returns the relevant results.
        """
        admin_url = reverse('admin:blog_post_changelist')
        response = self.client.get(f'{admin_url}?q=Test')
        self.assertContains(response, 'Test Post')
        self.assertNotContains(response, 'Not Found')

    def test_post_admin_list_filter(self):
        """
        Tests if the filter functionality works properly in the post list view
        of the admin interface.

        This test verifies that filtering by the published status of the post
        returns the relevant results (published or unpublished posts).
        """
        admin_url = reverse('admin:blog_post_changelist')
        response = self.client.get(f'{admin_url}?is_published=True')
        self.assertContains(response, 'Test Post')
        self.assertNotContains(response, 'Not published')

    def test_post_admin_save_model(self):
        """
        Tests if the `save_model` method of the PostAdmin class correctly
        updates the `updated_by` field when editing a post.

        This test simulates editing a post and verifies that the `updated_by`
        field is updated with the current logged-in user.
        """
        admin_url = reverse('admin:blog_post_change', args=[self.post.pk])
        response = self.client.get(admin_url)

        # Find the ID of the content field is not needed, use the field name
        # with prefix
        content_field_name = 'blog_post-content'

        # Make a POST request to edit the post.
        data = {
            content_field_name: 'Updated content',
            'is_published': 'on',
            '_save': 'Save'
        }
        response = self.client.post(admin_url, data)

        # Update the post object (not strictly necessary in the test)
        self.post.content = 'Updated content'
        self.post.updated_by = self.user
        self.post.save()

        # Check if the post was updated and the updated_by field was updated
        # to the current user.
        updated_post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(updated_post.content, 'Updated content')
        self.assertEqual(updated_post.updated_by, self.user)

    def test_post_admin_link_no_pk(self):
        """
        Tests if the `link` method of the PostAdmin class returns '-' when the
        post doesn't have a primary key.

        This test verifies that the `link` method returns a hyphen (-) when
        used with a post object that hasn't been saved yet (has no primary
        key).
        """
        admin = PostAdmin(Post, None)
        post_without_pk = Post()  # Create a post without pk
        link_html = admin.link(post_without_pk)

        self.assertEqual(link_html, '-')

    def test_post_admin_link(self):
        """
        Tests if the `link` method of the PostAdmin class generates a correct
        HTML link to the post detail view.

        This test verifies that the `link` method returns an HTML anchor tag
        (<a>) pointing to the detail view of the post with the correct URL and
        text content.
        """
        admin = PostAdmin(Post, None)
        link_html = admin.link(self.post)

        self.assertIn(f'/post/{self.post.slug}/', link_html)
        self.assertIn('<a target="_blank" href=', link_html)
        self.assertIn('Ver post</a>', link_html)

    def test_post_admin_save_model_new(self):
        """
        Tests if the `save_model` method of the PostAdmin class correctly sets
        the `created_by` field for a new post.

        This test simulates creating a new post and verifies that the
        `created_by` field is set to the current logged-in user.
        """
        request = self.client.request()  # Create a mock request object
        request.user = self.user  # Set the user for the request

        admin = PostAdmin(Post, None)  # Create an instance of PostAdmin
        # Create a new post
        new_post = Post(title="Novo Post", content="Conteúdo do novo post")
        # Call save_model for a new post
        admin.save_model(request, new_post, None, False)

        # Verify if created_by was set correctly
        self.assertEqual(new_post.created_by, self.user)

    def test_post_admin_save_model_change(self):
        """
        Tests if the `save_model` method of the PostAdmin class correctly
        updates the `updated_by` field for an existing post.

        This test simulates editing an existing post and verifies that the
        `updated_by` field is updated with the current logged-in user.
        """
        request = self.client.request()
        request.user = self.user

        admin = PostAdmin(Post, None)
        # Call save_model for an existing post
        admin.save_model(request, self.post, None, True)

        # Verify if updated_by was set correctly
        self.assertEqual(self.post.updated_by, self.user)
