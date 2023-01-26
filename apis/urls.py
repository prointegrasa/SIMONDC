from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import SmartlinkViewSet


smartlink_router = DefaultRouter()
smartlink_router.register(r"/smartlink", SmartlinkViewSet, "smartlink")

urlpatterns = [
    url('', include(smartlink_router.urls)),
]
