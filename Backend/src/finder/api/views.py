from ..models import OrganizationProfile
from rest_framework import viewsets, permissions

from .serializers import OrganizationProfileSerializer


class OrganizationProfileViewSet(viewsets.ModelViewSet):
    queryset = OrganizationProfile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = OrganizationProfileSerializer
