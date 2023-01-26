from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from smartlink import models
from .serializers import SmartlinkSerializer

class SmartlinkViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    lookup_field = 'slug'
    queryset = models.Smartlink.objects.all()
    serializer_class = SmartlinkSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



