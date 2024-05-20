from rest_framework import serializers
from main.models import AccessKey


class AccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        fields = "__all__"
