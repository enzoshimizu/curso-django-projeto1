from django.urls import reverse
from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def test_the_test(self):
        url = self.live_server_url + reverse('authors:register')
        self.browser.get(url)
        self.sleep()
