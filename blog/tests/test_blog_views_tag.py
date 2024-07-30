"""
Tests URL mapping for the blog tag view, ensuring it resolves to the correct
view class.
"""
from django.urls import reverse, resolve
from blog import views
from .test_blog_base import BlogTestBase, Post, Tag


class BlogViewsTagTest(BlogTestBase):
    """
    Tests the URL mapping for the blog tag view.
    """

    def setUp(self) -> None:
        self.tag = Tag.objects.create(
            name='Test Tag',
            slug='test_tag',
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test_post',
            content='Test post content',
            is_published=True,
        )
        self.post.tags.set([self.tag])
        return super().setUp()

    def test_blog_tag_view_function_is_correct(self):
        """
        Verifies that the blog posts by tag view function is mapped correctly
        to the 'blog:tag' URL with a slug.
        """
        view = resolve(reverse('blog:tag', kwargs={'slug': 'teste_tag'}))
        self.assertIs(view.func.view_class, views.TagListView)

    def test_blog_tag_returns_404_if_not_found(self):
        """
        Tests if the tag view returns 404 when no tag is found for the given
        slug.
        """
        response = self.client.get(
            reverse('blog:tag', kwargs={'slug': 'teste_tag'})
        )
        self.assertEqual(response.status_code, 404)

    def test_get_queryset(self):
        """Checks if get_queryset properly filters posts by tag."""
        view = views.TagListView()
        view.kwargs = {'slug': 'test_tag'}
        queryset = view.get_queryset()
        self.assertEqual(list(queryset), [self.post])

    def test_tag_list_view_context(self):
        """
        Verifica se a view TagListView inclui o título da página e o nome da
        tag no contexto.
        """
        response = self.client.get(
            reverse('blog:tag', kwargs={'slug': 'test_tag'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Tag - Tag - ')
        self.assertContains(response, 'Test Tag')
