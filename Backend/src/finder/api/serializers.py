from rest_framework import serializers

from ..models import OrganizationProfile, Address, Tag


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'city']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag', 'organizations']


class OrganizationProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    tagsAndKeywords = TagSerializer(many=True)

    class Meta:
        model = OrganizationProfile
        fields = '__all__'
