from django.contrib.auth import get_user_model
from rest_framework import serializers

from authors.validators import AuthorRecipeValidator
from recipes.models import Recipe
from tag.models import Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_step', 'cover', 'public', 'preparation',
            'category_name', 'author_name', 'tag_objects', 'tag_links',
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True
    )
    preparation = serializers.SerializerMethodField(
        read_only=True
    )
    category_name = serializers.StringRelatedField(
        source='category',
        read_only=True
    )  # type: ignore
    author_name = serializers.StringRelatedField(
        source='author',
        read_only=True
    )  # type: ignore

    tag_objects = TagSerializer(
        many=True,
        source='tags',
        read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True
    )  # type: ignore

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        super_validate = super().validate(attrs)

        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError
        )

        return super_validate
