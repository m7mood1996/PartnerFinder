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
        response = {'Message': 'Organization Created Successfully!'}

        data = json.loads(request.data['data'])
        try:
            OrganizationProfile.objects.get(pic=data['pic'])
            response = {
                'Message': 'Organization with the same PIC is already exists!'}
        except:
            if 'address' in data:
                if 'country' in data['address'] and 'city' in data['address']:
                    newAddress = Address(
                        country=data['address']['country'], city=data['address']['city'])
                    newAddress.save()
            org = OrganizationProfile(pic=data['pic'], legalName=data['legalName'], businessName=data['businessName'], classificationType=data['classificationType'], description=data['description'],
                                      address=newAddress)
            org.save()
            for tag in data['tagsAndKeywords']:
                try:
                    currTag = Tag.objects.get(tag=tag)
                    currTag.organizations.add(org)
                except:
                    currTag = Tag(tag=tag)
                    currTag.save()
                    currTag.organizations.add(org)

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def getOrganizationsByTags(self, request):
        data = json.loads(request.data['data'])
        tags = data['tags']
        res = []
        allTags = Tag.objects.all()
        for tag in allTags:
            if tag.tag in tags:
                res.extend(tag.organizations.all())
        response = []
        for val in res:
            response.append({'pic': val.pic, 'legalName': val.legalName, 'businessName': val.businessName,
                             'address': {'country': val.address.country, 'city': val.address.city}})

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def getOrganizationsByCountries(self, request):
        data = json.loads(request.data['data'])
        countries = data['countries']
        res = []
        allOrgs = OrganizationProfile.objects.all()
        for org in allOrgs:
            if org.address.country in countries:
                res.append(org)
        response = []
        for val in res:
            response.append({'pic': val.pic, 'legalName': val.legalName, 'businessName': val.businessName,
                             'address': {'country': val.address.country, 'city': val.address.city}, 'discreption': val.description})

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
