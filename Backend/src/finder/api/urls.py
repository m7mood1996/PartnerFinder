from rest_framework import routers

from django.urls import path
from .views import OrganizationProfileViewSet

router = routers.DefaultRouter()

router.register('api/OrganizationProfile',
                OrganizationProfileViewSet, 'finder')

urlpatterns = router.urls
# urlpatterns = [
#     path('',OrganizationProfileViewSet.as_view())
# ]
