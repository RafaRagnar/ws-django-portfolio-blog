from django.core.exceptions import ValidationError
from parameterized import parameterized  # type: ignore
from .test_blog_base import BlogTestBase, Category


class BlogCategoryModelTest(BlogTestBase):
    def setUp(self) -> None:
        self.category = self.creating_category(
            name='Category Testing',
            slug='category_testing',
        )
        return super().setUp()

    @parameterized.expand([
        ('name', 255),
        ('slug', 255),
    ])
    def test_category_fields_max_length(self, field, max_lenght):
        setattr(self.category, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_category_save_generates_slug(self):
        """
        Test whether the save method generates a only slug when it does not
        exist.
        """
        category = Category(name='Test category save generates slug')
        category.save()
        self.assertIsNotNone(category.slug)
        # self.assertEqual(post.slug, slugify_new(post.title, 4))

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)
