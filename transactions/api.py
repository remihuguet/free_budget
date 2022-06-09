from rest_framework import viewsets
from . import models, serializers


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = models.SubCategory.objects.all()
    serializer_class = serializers.SubCategorySerializer
