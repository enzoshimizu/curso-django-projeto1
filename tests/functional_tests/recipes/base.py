from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import time

from recipes.tests.test_recipe_base import RecipeMixin
from utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.close()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
