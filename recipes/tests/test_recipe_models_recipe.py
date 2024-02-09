from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_has_more_than_65_chars(self):
        self.recipe.title = 'a' * 66

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = Recipe(category=self.make_category('Test default category'),
                        author=self.make_author(username='newuser'),
                        title='Recipe Title',
                        description='Description',
                        slug='recipe-slug-1',
                        preparation_time=10,
                        preparation_time_unit='Minutos',
                        servings=5,
                        servings_unit='Porções',
                        preparation_step='Recipe Preparations Steps',)
        recipe.full_clean()
        recipe.save()

        self.assertFalse(recipe.preparation_step_is_html,
                         msg='preparation_step_is_html is not false')
        self.assertFalse(recipe.is_published,
                         msg='is_published is not false')

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation')
