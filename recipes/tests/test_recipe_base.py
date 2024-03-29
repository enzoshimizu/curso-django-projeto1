from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(self,
                    first_name='user',
                    last_name='user',
                    username='username',
                    password='123456',
                    email='username@email.com'):
        return User.objects.create_user(first_name=first_name,
                                        last_name=last_name,
                                        username=username,
                                        password=password,
                                        email=email)

    def make_recipe(self,
                    category_data=None,
                    author_data=None,
                    title='Recipe Title',
                    description='Description',
                    slug='recipe-slug',
                    preparation_time=10,
                    preparation_time_unit='Minutos',
                    servings=5,
                    servings_unit='Porções',
                    preparation_step='Recipe Preparations Steps',
                    preparation_step_is_html=False,
                    is_published=True):

        if not category_data:
            category_data = {}

        if not author_data:
            author_data = {}

        return Recipe.objects.create(category=self.make_category(**category_data),  # noqa: E501
                                     author=self.make_author(**author_data),
                                     title=title,
                                     description=description,
                                     slug=slug,
                                     preparation_time=preparation_time,
                                     preparation_time_unit=preparation_time_unit,  # noqa: E501
                                     servings=servings,
                                     servings_unit=servings_unit,
                                     preparation_step=preparation_step,
                                     preparation_step_is_html=preparation_step_is_html,  # noqa: E501
                                     is_published=is_published)

    def make_recipe_in_batch(self, qtd=10):
        recipes = []

        for i in range(qtd):
            kwargs = {
                'title': f'Recipe Title {i}',
                'slug': f'{i}',
                'author_data': {'username': f'u{i}'},
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)

        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
