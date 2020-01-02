from rest_framework import serializers

from ..models import OrganizationProfile


class OrganizationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationProfile
        fields = '__all__'
