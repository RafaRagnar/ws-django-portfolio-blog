from .test_blog_base import BlogTestBase, Post
from django.core.exceptions import ValidationError
from parameterized import parameterized


class BlogPostModelTest(BlogTestBase):
    def setUp(self) -> None:
        self.post = self.creating_post()
        return super().setUp()

    def creating_post_no_defaults(self):
        post = Post(
            category=self.creating_category(
                name='Test Default Category', slug='test_default_category'),
            title='Post is_published is false by default',
            slug='post_is_published_is_false_by_default',
            excerpt='Post excerpt',
            content='Criando um post para pytest.',
        )
        post.full_clean()
        post.save()
        return post

    @parameterized.expand([
        ('title', 65),
        ('slug', 255),
        ('excerpt', 150),
    ])
    def test_post_fields_max_length(self, field, max_lenght):
        setattr(self.post, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_post_is_published_is_false_by_default(self):
        post = self.creating_post_no_defaults()
        self.assertFalse(post.is_published,
                         msg='Post is_published is not False')
