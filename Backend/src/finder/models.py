# from django.db import models
from djongo import models


class Address(models.Model):
    country = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.country + ' ' + self.city


class OrganizationProfile(models.Model):
    pic = models.IntegerField(unique=True)
    legalName = models.CharField(max_length=200)
    businessName = models.CharField(max_length=200)
    classificationType = models.CharField(max_length=50, blank=True, null=True)
    # numberOfProjects = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    address = models.OneToOneField(
        Address, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pic)


class Tag(models.Model):
    tag = models.CharField(max_length=200, blank=True, null=True)
    organizations = models.ManyToManyField(
        OrganizationProfile, blank=True, related_name='tagsAndKeywords')

    def __str__(self):
        return self.tag
