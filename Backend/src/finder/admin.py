from django.contrib import admin

# Register your models here.
# from .models import Finder

# admin.site.register(Finder)

from .models import OrganizationProfile, Address, Tag

admin.site.register(OrganizationProfile)
admin.site.register(Address)
admin.site.register(Tag)

