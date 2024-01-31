# from django.http import HttpResponse
from django.shortcuts import render
from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {'recipes': recipes}
    return render(request, 'recipes/pages/home.html', context=context)


def recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    context = {'recipe': recipe,
               'is_detail_page': True}
    return render(request, 'recipes/pages/recipe-view.html', context=context)


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id')
    context = {'recipes': recipes}
    return render(request, 'recipes/pages/home.html', context=context)
