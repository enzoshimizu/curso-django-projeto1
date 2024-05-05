from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 1


class RecipeAPIV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={
            'request': request,
        }
    )

    return Response(serializer.data)
