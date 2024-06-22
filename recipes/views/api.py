from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from recipes.permissions import IsOwner
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 3


class RecipeAPIV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    def get_object(self):
        pk = self.kwargs.get('pk', '')

        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()


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
