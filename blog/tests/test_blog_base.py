from django.test import TestCase
from blog.models import Page, Post, Category, Tag, User


class BlogTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def creating_category(self, name='Test Category', slug='test_category'):
        return Category.objects.create(name=name, slug=slug)

    def creating_tag(self, name='Test Tag', slug='test_tag'):
        return Tag.objects.create(name=name, slug=slug)

    def creating_author(
            self,
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
    ):
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
        return Page.objects.create(
            title=title,
            slug=slug,
            is_published=is_published,
            content=content,
        )
