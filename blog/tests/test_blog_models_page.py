"""
Tests for the Page model in the blog application.
"""
from django.core.exceptions import ValidationError
from django.urls import reverse
from parameterized import parameterized  # type: ignore
from .test_blog_base import BlogTestBase, Page


class BlogPageModelTest(BlogTestBase):
    """
    Tests for the Page model.
    """

    def setUp(self) -> None:
        self.page = self.creating_page()
        return super().setUp()

    def creating_page_no_defaults(self):
        """
        Creates a Page instance with is_published set to False.
        """
        page = Page(
            title='Page is_published is false by default',
            slug='page_is_published_is_false_by_default',
            content='Creating a unique page for pytest'
        )
        page.full_clean()
        page.save()
        return page

    @parameterized.expand([
        ('title', 65),
        ('slug', 255),
    ])
    def test_page_fields_max_length(self, field, max_length):
        """
        Tests that the 'title' and 'slug' fields have the correct maximum
        length.
        """
        setattr(self.page, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.page.full_clean()

    def test_page_is_published_is_false_by_default(self):
        """
        Tests that the 'is_published' field defaults to False.
        """
        page = self.creating_page_no_defaults()
        self.assertFalse(page.is_published,
                         msg='Page is_published is not False')

    def test_page_string_representation(self):
        """
        Tests that the string representation of a Page object is its title.
        """
        needed = 'Testing Representation'
        self.page.title = 'Testing Representation'
        self.page.full_clean()
        self.page.save()
        self.assertEqual(
            str(self.page), needed,
            msg=f'Page string representation must be'
            f'"{needed}" but "{str(self.page)}" was received.')

    def test_page_get_absolute_url_published(self):
        """
        Tests that `get_absolute_url` returns the correct URL for a published
        page.
        """
        page = Page.objects.create(
            title='Test Page', slug='test_page', is_published=True)
        expected_url = reverse('blog:page', args=(page.slug,))
        self.assertEqual(page.get_absolute_url(), expected_url)

    def test_page_get_absolute_url_not_published(self):
        """
        Tests that `get_absolute_url` returns the index URL for an unpublished
        page.
        """
        page = Page.objects.create(
            title='Test Page', slug='test_page', is_published=False)
        expected_url = reverse('blog:index')
        self.assertEqual(page.get_absolute_url(), expected_url)

    def test_page_save_generates_slug(self):
        """
        Tests that the `save` method generates a unique slug when it does not
        exist.
        """
        page = Page(title='My Page')
        page.save()
        self.assertIsNotNone(page.slug)
        # self.assertEqual(post.slug, slugify_new(post.title, 4))
