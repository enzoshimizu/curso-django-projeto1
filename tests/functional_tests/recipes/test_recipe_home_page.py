from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from unittest.mock import patch

import pytest

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('No recipes found!', body.text)

    @patch('recipes.views.PER_PAGE', 2)
    def test_recipe_home_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        search_input.click()
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        body = self.browser.find_element(
            By.CLASS_NAME, 'main-content-container'
        )

        self.assertIn(title_needed, body.text)

    @patch('recipes.views.PER_PAGE', 2)
    def test_recipe_home_pagination(self):
        self.make_recipe_in_batch()

        self.browser.get(self.live_server_url)

        page2 = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Go to page 2"]'
        )

        page2.click()

        qty_recipes = len(self.browser.find_elements(By.CLASS_NAME, 'recipe'))

        self.assertEqual(qty_recipes, 2)
