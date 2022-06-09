from rest_framework import serializers
from . import models


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = ("id", "name", "category")
