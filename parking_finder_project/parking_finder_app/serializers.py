from rest_framework import serializers

from .models import ParkingSpace


class ParkingSpaceSerializer(serializers.ModelSerializer):
    booked_till = serializers.DateTimeField()
    pricing_details = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSpace
        fields = "__all__"

    def get_pricing_details(self, obj):
        return {'pricing_per_hour': '$3.00',
                'pricing_per_day': '$30.00'}
