from rest_framework.serializers import ModelSerializer
from app01 import models


class User_ser(ModelSerializer):
    class Meta:
        model = models.Wxuser
        fields = "__all__"
