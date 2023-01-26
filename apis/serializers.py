from rest_framework import serializers
from smartlink import models


class SmartlinkSerializer(serializers.ModelSerializer):

    class Meta:
        model= models.Smartlink
        fields= ('title','base64','slug','tabela')
