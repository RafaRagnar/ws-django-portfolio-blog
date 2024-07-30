import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from blog.tests.test_blog_base import BlogMixin


class TestBlogBaseFunctional(StaticLiveServerTestCase, BlogMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser(headless=False)
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
