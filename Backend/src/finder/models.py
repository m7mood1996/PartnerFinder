from django.db import models

# Create your models here.


class Finder(models.Model):
    legalName = models.TextField()

    def __str__(self):
        return self.legalName
