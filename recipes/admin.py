from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from recipes.models import Category, Recipe
from tag.models import Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


class TagInLine(GenericStackedInline):
    model = Tag
    fields = ['name',]
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_at',
        'author',
        'is_published',
        'preparation_step_is_html',
    )

    list_display_links = (
        'title',
        'created_at',
    )

    search_fields = (
        'id',
        'title',
        'description',
        'slug',
        'preparation_step',
    )

    list_filter = (
        'category',
        'author',
        'is_published',
        'preparation_step_is_html',
    )

    list_per_page = 10

    list_editable = (
        'is_published',
    )

    ordering = (
        '-id',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    inlines = [
        TagInLine,
    ]
