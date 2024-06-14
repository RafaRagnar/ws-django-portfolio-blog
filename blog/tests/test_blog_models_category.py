"""
Tests for the Category model in the blog application.
"""
from django.core.exceptions import ValidationError
from parameterized import parameterized  # type: ignore
from .test_blog_base import BlogTestBase, Category


class BlogCategoryModelTest(BlogTestBase):
    """
    Tests for the Category model.
    """

    def setUp(self) -> None:
        """
        Sets up a Category instance for testing.
        """
        self.category = self.creating_category(
            name='Category Testing',
            slug='category_testing',
        )
        return super().setUp()

    @parameterized.expand([
        ('name', 255),
        ('slug', 255),
    ])
    def test_category_fields_max_length(self, field, max_length):
        """
        Tests that the 'name' and 'slug' fields have the correct maximum
        length.
        """
        setattr(self.category, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_category_save_generates_slug(self):
        """
        Tests that the `save` method generates a unique slug when it does not
        exist.
        """
        category = Category(name='Test category save generates slug')
        category.save()
        self.assertIsNotNone(category.slug)
        # self.assertEqual(post.slug, slugify_new(post.title, 4))

    def test_category_string_representation(self):
        """
        Tests that the string representation of a Category object is its name.
        """
        self.assertEqual(str(self.category), self.category.name)
