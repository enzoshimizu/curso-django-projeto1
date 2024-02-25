from django.urls import reverse, resolve
from unittest.mock import patch

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        url = reverse('recipes:home')
        view = resolve(url)
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        url = reverse('recipes:home')
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertGreaterEqual(len(context_recipes), 1)

    def test_recipe_home_template_do_not_load_unpublished(self):
        title = 'This is recipe is not published'
        self.make_recipe(title=title, is_published=False)

        url = reverse('recipes:home')
        response = self.client.get(url)
        content = response.content.decode('utf-8')

        self.assertNotIn(title, content)

    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=12A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )
            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                3
            )
