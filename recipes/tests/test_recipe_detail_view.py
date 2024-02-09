from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_recipe_view_function_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'id': 1, })
        view = resolve(url)
        self.assertIs(view.func, views.recipe)

    def test_recipe_recipe_view_returns_status_code_404_OK(self):
        url = reverse('recipes:recipe', kwargs={'id': 9999, })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        title = 'This is a detail test'
        self.make_recipe(title=title)

        url = reverse('recipes:recipe', kwargs={'id': 1, })
        response = self.client.get(url)
        content = response.content.decode('utf-8')

        self.assertIn(title, content)

    def test_recipe_detail_template_do_not_load_unpublished(self):
        title = 'This is recipe is not published'
        recipe = self.make_recipe(title=title, is_published=False)

        url = reverse('recipes:recipe', kwargs={'id': recipe.id, })
        response = self.client.get(url)
        content = response.content.decode('utf-8')

        self.assertNotIn(title, content)
