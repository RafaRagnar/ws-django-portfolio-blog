from django.core.exceptions import ValidationError
from django.urls import reverse
from parameterized import parameterized  # type: ignore
from .test_blog_base import BlogTestBase, Post
from utils.rands import slugify_new


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

    def test_post_string_representation(self):
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
        Test whether get_absolute_url returns the correct URL for a published
        post.
        """
        post = Post.objects.create(
            title='Test Post', slug='test_post', is_published=True)
        expected_url = reverse('blog:post', args=(post.slug,))
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_post_get_absolute_url_not_published(self):
        """
        Test if get_absolute_url returns the index URL for an unpublished post.
        """
        post = Post.objects.create(
            title='Test Post', slug='test_post', is_published=False)
        expected_url = reverse('blog:index')
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_post_save_generates_slug(self):
        """
        Test whether the save method generates a only slug when it does not
        exist.
        """
        post = Post(title='My Post')
        post.save()
        self.assertIsNotNone(post.slug)
        self.assertNotEqual(post.slug, slugify_new(post.slug, 4))
