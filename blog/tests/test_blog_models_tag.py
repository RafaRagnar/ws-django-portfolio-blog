from django.core.exceptions import ValidationError
from parameterized import parameterized  # type: ignore
from .test_blog_base import BlogTestBase, Tag


class BlogTagModelTest(BlogTestBase):
    def setUp(self) -> None:
        self.tag = self.creating_category(
            name='Tag Testing',
            slug='tag_testing',
        )
        return super().setUp()

    @parameterized.expand([
        ('name', 255),
        ('slug', 255),
    ])
    def test_tag_fields_max_length(self, field, max_lenght):
        setattr(self.tag, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.tag.full_clean()

    def test_tag_save_generates_slug(self):
        """
        Test whether the save method generates a only slug when it does not
        exist.
        """
        tag = Tag(name='Test tag save generates slug')
        tag.save()
        self.assertIsNotNone(tag.slug)
        # self.assertEqual(post.slug, slugify_new(post.title, 4))

    def test_tag_string_representation(self):
        self.assertEqual(str(self.tag), self.tag.name)
