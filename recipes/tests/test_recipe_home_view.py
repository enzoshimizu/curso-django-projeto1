from django.urls import reverse, resolve

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
