from rest_framework import serializers
from .models import RiderData


class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderData
        fields = "__all__"