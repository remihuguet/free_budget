from rest_framework import viewsets, permissions
from . import models, serializers


class IsComptaPermission(permissions.BasePermission):

    message = "You must be a compta to access this resource."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Compta").exists()


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = models.SubCategory.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsComptaPermission,
    ]
    serializer_class = serializers.SubCategorySerializer
