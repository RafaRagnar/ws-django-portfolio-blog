"""
This module provides a base test class (`BlogTestBase`) for testing the blog
application.

The `BlogTestBase` class offers helper methods to create test instances of
various models used in the blog application, simplifying the process of setting
up test data.
"""
from django.test import TestCase
from blog.models import Page, Post, Category, Tag, User


class BlogMixin:
    def creating_category(self, name='Test Category', slug='test_category'):
        """
        Creates a Category instance.

        Args:
            name (str): The name of the category.
            slug (str): The slug of the category.

        Returns:
            Category: The created Category instance.
        """
        return Category.objects.create(name=name, slug=slug)

    def creating_tag(self, name='Test Tag', slug='test_tag'):
        """
        Creates a Tag instance.

        Args:
            name (str): The name of the tag.
            slug (str): The slug of the tag.

        Returns:
            Tag: The created Tag instance.
        """
        return Tag.objects.create(name=name, slug=slug)

    def creating_author(
            self,
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
    ):
        """
        Creates a User instance (author).

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            username (str): The username of the user.
            password (str): The password of the user.
            email (str): The email of the user.

        Returns:
            User: The created User instance.
        """
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def creating_post(
            self,
            category_data=None,
            title='Post Title',
            slug='post_title',
            excerpt='Post excerpt',
            is_published=True,
            created_by_data=None,
            content='Criando um post para pytest.',
            cover_in_post_content=True,
    ):
        """
        Creates a Post instance.

        Args:
            category_data (dict, optional): Data for creating the category of
                                            the post. Defaults to None.
            title (str, optional): The title of the post. Defaults to 'Post
                                   Title'.
            slug (str, optional): The slug of the post. Defaults to
                                  'post_title'.
            excerpt (str, optional): The excerpt of the post. Defaults to
                                     'Post excerpt'.
            is_published (bool, optional): Whether the post is published.
            Defaults to True.
            created_by_data (dict, optional): Data for creating the author of
                                              the post. Defaults to None.
            content (str, optional): The content of the post. Defaults to
                                     'Criando um post para pytest.'.
            cover_in_post_content (bool, optional): Whether the post has a
                                                cover image. Defaults to True.

        Returns:
            Post: The created Post instance.
        """
        if category_data is None:
            category_data = {}

        if created_by_data is None:
            created_by_data = {}

        return Post.objects.create(
            category=self.creating_category(**category_data),
            title=title,
            slug=slug,
            excerpt=excerpt,
            is_published=is_published,
            created_by=self.creating_author(**created_by_data),
            content=content,
            cover_in_post_content=cover_in_post_content,
        )

    def creating_page(
            self,
            title='Page title',
            slug='page_title',
            is_published=True,
            content='Criando uma página para pytest',
    ):
        """
        Creates a Page instance.

        Args:
            title (str, optional): The title of the page. Defaults to 'Page
                                   title'.
            slug (str, optional): The slug of the page. Defaults to
                                  'page_title'.
            is_published (bool, optional): Whether the page is published.
                                           Defaults to True.
            content (str, optional): The content of the page. Defaults to
                                     'Criando uma página para pytest'.

        Returns:
            Page: The created Page instance.
        """
        return Page.objects.create(
            title=title,
            slug=slug,
            is_published=is_published,
            content=content,
        )

    def creating_posts_in_batch(self, qtd=10):
        posts = []
        for i in range(qtd):
            kwargs = {'slug': f'r{i}'}
            kwargs_category = {'name': f'Cat{i}', 'slug': f'cat{i}'}
            post = self.creating_post(
                category_data=kwargs_category, slug=kwargs)
            posts.append(post)
        return posts


class BlogTestBase(TestCase, BlogMixin):
    """
    Base class for blog application tests, providing helper methods for
    creating test objects.
    """

    def setUp(self) -> None:
        """
        Sets up the test environment.
        """
        return super().setUp()
