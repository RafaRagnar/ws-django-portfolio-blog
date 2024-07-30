import pytest
from selenium.webdriver.common.by import By
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


@pytest.mark.functional_test
class TestBlogHomePageFunctional(TestBlogBaseFunctional):

    def test_blog_home_no_post_error_message_no_post(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep(15)
        self.assertIn('Nenhum post encontrado aqui 🥲', body.text)
