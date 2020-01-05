from ..models import OrganizationProfile
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import OrganizationProfile, Address, Tag
from .serializers import OrganizationProfileSerializer, AddressSerializer, TagSerializer
import json


class OrganizationProfileViewSet(viewsets.ModelViewSet):
    queryset = OrganizationProfile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = OrganizationProfileSerializer

    @action(detail=False, methods=['POST'])
    def createOrganization(self, request):
        response = {'Message': 'Organization added successfully!'}

        data = json.loads(request.data['data'])
        try:
            OrganizationProfile.objects.get(pic=data['pic'])
            response = {
                'Message': 'Organization with the same PIC is already exists!'}
        except:
            print(data)
            newAddress = Address(
                country=data['address']['country'], city=data['address']['city'])
            newAddress.save()
            org = OrganizationProfile(pic=data['pic'], legalName=data['legalName'], businessName=data['businessName'], classificationType=data['classificationType'], description=data['description'],
                                      address=newAddress)
            org.save()
            print(data['tagsAndKeywords'])
            for tag in data['tagsAndKeywords']:
                currTag = Tag(tag=tag, organization=org)
                currTag.save()

        return Response(response, status=status.HTTP_200_OK)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AddressSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TagSerializer
