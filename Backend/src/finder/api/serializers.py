from rest_framework import serializers

from ..models import OrganizationProfile, Address, Tag, Event, Participants, Location, TagP


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


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['_id', 'event_name', 'event_url']

class TagPSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagP
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ParticipantsSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)
    tags = TagPSerializer(many=True)
    class Meta:
        model = Participants
        fields = '__all__'
