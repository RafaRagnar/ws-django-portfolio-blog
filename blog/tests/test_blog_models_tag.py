"""
Tests for the Tag model in the blog application.
"""
from django.core.exceptions import ValidationError
from parameterized import parameterized  # type: ignore
from .test_blog_base import BlogTestBase, Tag


class BlogTagModelTest(BlogTestBase):
    """
    Tests for the Tag model.
    """

    def setUp(self) -> None:
        self.tag = self.creating_tag(
            name='Tag Testing',
            slug='tag_testing',
        )
        return super().setUp()

    @parameterized.expand([
        ('name', 255),
        ('slug', 255),
    ])
    def test_tag_fields_max_length(self, field, max_length):
        """
        Tests that the 'name' and 'slug' fields have the correct maximum
        length.
        """
        setattr(self.tag, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.tag.full_clean()

    def test_tag_save_generates_slug(self):
        """
        Tests that the `save` method generates a unique slug when it does not
        exist.
        """
        tag = Tag(name='Test tag save generates slug')
        tag.save()
        self.assertIsNotNone(tag.slug)
        # self.assertEqual(post.slug, slugify_new(post.title, 4))

    def test_tag_string_representation(self):
        """
        Tests that the string representation of a Tag object is its name.
        """
        needed = 'Testing Tag Representation'
        self.tag.name = 'Testing Tag Representation'
        self.tag.full_clean()
        self.tag.save()
        self.assertEqual(
            str(self.tag), needed,
            msg=f'Tag string representation must be'
            f'"{needed}" but "{str(self.tag)}" was received.')
