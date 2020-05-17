# from django.db import models
from djongo import models


class Address(models.Model):
    """
    class to define the data model of organization's address.
    """

    country = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.country + ' ' + self.city


class MapIds(models.Model):
    originalID = models.IntegerField(unique=True)
    indexID = models.IntegerField(unique=True)


class OrganizationProfile(models.Model):
    """
    class to define the data model of Organization profile which contains the necessary fields.
    """
    pic = models.IntegerField(unique=True)
    legalName = models.CharField(max_length=200)
    businessName = models.CharField(max_length=200)
    classificationType = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.OneToOneField(
        Address, blank=True, null=True, on_delete=models.CASCADE)
    dataStatus = models.CharField(max_length=200, default='')
    numberOfProjects = models.IntegerField(default=0)
    consorsiumRoles = models.BooleanField(default=False)
    collaborations = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pic)


class Tag(models.Model):
    """
    class to define the data model of the tags in the DB.
    """
    tag = models.CharField(max_length=200, blank=True, null=True)
    organizations = models.ManyToManyField(
        OrganizationProfile, blank=True, related_name='tagsAndKeywords')

    def __str__(self):
        return self.tag


class Location(models.Model):
    location = models.CharField(max_length=200, blank=True)

    # participant = models.(Participants, blank=True, null=True, on_delete=models.CASCADE, related_name='locationA')
    def __str__(self):
        return self.location


class MapIDsB2match(models.Model):
    originalID = models.IntegerField(unique=True)
    indexID = models.IntegerField(unique=True)


class MapIDsB2matchUpcoming(models.Model):
    originalID = models.IntegerField(unique=True)
    indexID = models.IntegerField(unique=True)


class Participants(models.Model):
    """
        Participants from B2MATCH events contains: name, organization name, location, organization url,
        org icon url and description
        NOTE: may contain empty fields
    """
    participant_name = models.CharField(max_length=200)
    organization_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    participant_img_url = models.CharField(
        max_length=200, blank=True, null=True)
    org_type = models.CharField(max_length=200, blank=True, null=True)
    org_icon_url = models.CharField(max_length=200, blank=True, null=True)
    org_url = models.CharField(max_length=200, blank=True, null=True)

    # tags = models.ManyToManyField(TagP,related_name='participants_tags')

    def __str__(self):
        return self.participant_name


class TagP(models.Model):
    tag = models.CharField(max_length=200, blank=True, null=True)
    participant = models.ManyToManyField( Participants, blank=True, related_name='tagsAndKeywordsP')

    def __str__(self):
        return self.tag


class Event(models.Model):
    """
        Event Object which contains Event name, url and if the event is up coming or from the past
    """
    event_name = models.CharField(max_length=200, unique=True)
    event_url = models.CharField(max_length=200)
    event_date = models.DateField(blank=True, null=True)
    is_upcoming = models.BooleanField(default=False, null=True)
    event_part = models.ManyToManyField(Participants, blank=True, related_name='Part_Event')

    def __str__(self):
        return self.event_name
