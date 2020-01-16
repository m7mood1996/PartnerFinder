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



class Location(models.Model):
    location = models.CharField(max_length=200, blank=True)
    #participant = models.(Participants, blank=True, null=True, on_delete=models.CASCADE, related_name='locationA')


class Participants(models.Model):
    participant_name = models.CharField(max_length=200)
    organization_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    location = models.OneToOneField(Location,on_delete=models.CASCADE)
    participant_img_url = models.CharField(max_length=200,blank=True,null=True)
    org_type = models.CharField(max_length=200,blank=True,null=True)
    org_icon_url = models.CharField(max_length=200,blank=True,null=True)
    org_url = models.CharField(max_length=200,blank=True,null=True)
    #tags = models.ManyToManyField(TagP,related_name='participants_tags')

class TagP(models.Model):
    tag = models.CharField(max_length=200, blank=True, null=True)
    participant = models.ManyToManyField(Participants, blank=True, related_name='tagsAndKeywordsP')


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_url = models.CharField(max_length=200)

    def __str__(self):
        return self.event_name




