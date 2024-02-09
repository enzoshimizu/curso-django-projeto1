from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1, })
        view = resolve(url)
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_code_404_OK(self):
        url = reverse('recipes:category', kwargs={'category_id': 9999, })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        title = 'This is a category test'
        self.make_recipe(title=title)

        url = reverse('recipes:category', kwargs={'category_id': 1, })
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        context_recipes = response.context['recipes']

        self.assertIn(title, content)
        self.assertGreaterEqual(len(context_recipes), 1)

    def test_recipe_category_template_do_not_load_unpublished(self):
        title = 'This is recipe is not published'
        recipe = self.make_recipe(title=title, is_published=False)

        url = reverse('recipes:category', kwargs={
                      'category_id': recipe.category.id, })
        response = self.client.get(url)
        content = response.content.decode('utf-8')

        self.assertNotIn(title, content)
