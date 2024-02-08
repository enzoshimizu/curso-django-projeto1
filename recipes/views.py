# from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {'recipes': recipes}

    return render(request, 'recipes/pages/home.html', context=context)


def search(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {'recipes': recipes}

    return render(request, 'recipes/pages/home.html', context=context)


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    context = {'recipe': recipe,
               'is_detail_page': True}

    return render(request, 'recipes/pages/recipe-view.html', context=context)


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id')
    recipes = get_list_or_404(recipes)

    title = f'Categoria - {recipes[0].category.name}'
    context = {'recipes': recipes, 'title': title}

    return render(request, 'recipes/pages/category.html', context=context)
