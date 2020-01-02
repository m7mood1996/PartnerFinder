from django.db import models

# Create your models here.


class OrganizationProfile(models.Model):
    pic = models.IntegerField(unique=True)
    legalName = models.CharField(max_length=200)
    businessName = models.CharField(max_length=200)
    classificationType = models.CharField(max_length=50)
    # numberOfProjects = models.IntegerField()
    description = models.TextField()
    address = models.TextField()
    # collaborations = models.TextField()
    tagsAndKeywords = models.TextField()

    def getAddress(self):
        return json.loads(self.address)

    def setAddress(self, address):
        self.address = json.dumps(address)

    # def getCollaborations(self):
    #     return json.loads(self.collaborations)

    # def setCollaborations(self, collaborations):
    #     self.collaborations = json.dumps(collaborations)

    def getTagsAndKeywords(self):
        return json.loads(self.tagsAndKeywords)

    def setTagsAndKeywords(self, tagsAndKeywords):
        self.tagsAndKeywords = json.dumps(tagsAndKeywords)
