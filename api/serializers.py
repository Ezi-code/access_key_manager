from rest_framework import serializers
from main.models import AccessKey


class AccessKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessKey
        fields = ["user", "key", "status", "expiry_date", "created_at"]
