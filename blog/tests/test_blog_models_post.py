"""
Tests for the Post model in the blog application.
"""
from django.core.exceptions import ValidationError
from django.urls import reverse
from parameterized import parameterized  # type: ignore
from utils.rands import slugify_new
from .test_blog_base import BlogTestBase, Post


class BlogPostModelTest(BlogTestBase):
    """
    Tests for the Post model.
    """

    def setUp(self) -> None:
        self.post = self.creating_post()
        return super().setUp()

    def creating_post_no_defaults(self):
        """
        Creates a Post instance with is_published set to False.
        """
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
    def test_post_fields_max_length(self, field, max_length):
        """
        Tests that the 'title', 'slug', and 'excerpt' fields have the correct
        maximum length.
        """
        setattr(self.post, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_post_is_published_is_false_by_default(self):
        """
        Tests that the 'is_published' field defaults to False.
        """
        post = self.creating_post_no_defaults()
        self.assertFalse(post.is_published,
                         msg='Post is_published is not False')

    def test_post_string_representation(self):
        """
        Tests that the string representation of a Post object is its title.
        """
        needed = 'Testing Representation'
        self.post.title = 'Testing Representation'
        self.post.full_clean()
        self.post.save()
        self.assertEqual(
            str(self.post), needed,
            msg=f'Post string representation must be'
            f'"{needed}" but "{str(self.post)}" was received.')

    def test_post_get_absolute_url_published(self):
        """
        Tests that `get_absolute_url` returns the correct URL for a published
        post.
        """
        post = Post.objects.create(
            title='Test Post', slug='test_post', is_published=True)
        expected_url = reverse('blog:post', args=(post.slug,))
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_post_get_absolute_url_not_published(self):
        """
        Tests that `get_absolute_url` returns the index URL for an unpublished
        post.
        """
        post = Post.objects.create(
            title='Test Post', slug='test_post', is_published=False)
        expected_url = reverse('blog:index')
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_post_save_generates_slug(self):
        """
        Tests that the `save` method generates a unique slug when it does not
        exist.
        """
        post = Post(title='My Post')
        post.save()
        self.assertIsNotNone(post.slug)
        self.assertNotEqual(post.slug, slugify_new(post.slug, 4))
