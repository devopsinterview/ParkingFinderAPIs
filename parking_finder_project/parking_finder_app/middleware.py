from parking_finder_app.models import ParkingSpace
import datetime
from django.utils.deprecation import MiddlewareMixin

class ParkingSpaceUpdateMiddleware(MiddlewareMixin):
    """
    Custom Middleware to update the expired bookings
    """

    def process_request(self, request):
        '''
        Based on the current time if the booked till time has expired make the spot available
        :param request:
        :return:
        '''

        current_time = datetime.datetime.now()
        ParkingSpace.objects.filter(booked_till__lte=current_time).update(available=True, booked_till=None)
        return