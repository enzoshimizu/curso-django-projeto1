from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(name='Category Test')
        return super().setUp()

    def test_recipe_category_model_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_recipe_category_raises_error_if_has_more_than_65_chars(self):
        self.category.name = 'a' * 66

        with self.assertRaises(ValidationError):
            self.category.full_clean()
