from rest_framework import serializers
from .models import RequesterData


class RequesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequesterData
        fields = "__all__"