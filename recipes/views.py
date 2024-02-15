# from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q

from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {'recipes': recipes}

    return render(request, 'recipes/pages/home.html', context=context)


def search(request):
    search_term = request.GET.get('q', '').strip()

    if search_term == '':
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True).order_by('-id')

    context = {'page_title': f'Search for "{search_term}"',
               'recipes': recipes}

    return render(request, 'recipes/pages/search.html', context=context)


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
