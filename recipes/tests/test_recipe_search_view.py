from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?q=teste'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=teste'
        response = self.client.get(url)
        content = response.content.decode('utf-8')

        self.assertIn('Search for &quot;teste&quot;', content)

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one',
            title=title1,
            author_data={'username': 'one'}
        )

        recipe2 = self.make_recipe(
            slug='two',
            title=title2,
            author_data={'username': 'two'}
        )

        url1 = reverse('recipes:search') + '?q=' + title1
        response1 = self.client.get(url1)

        url2 = reverse('recipes:search') + '?q=' + title2
        response2 = self.client.get(url2)

        url3 = reverse('recipes:search') + '?q=this'
        response3 = self.client.get(url3)

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertNotIn(recipe1, response2.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])

        self.assertIn(recipe1, response3.context['recipes'])
        self.assertIn(recipe2, response3.context['recipes'])
