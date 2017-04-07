from rest_framework import serializers

from .models import ParkingSpace


class ParkingSpaceSerializer(serializers.ModelSerializer):
    booked_till = serializers.DateTimeField()

    class Meta:
        model = ParkingSpace
        fields = "__all__"