from datetime import timedelta
from django.db.models.expressions import F
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.base import TemplateView
from rest_framework import status
import random
from .serializers import ParkingSpaceSerializer
from .models import ParkingSpace
from .helper import check_parking_in_given_area
import datetime


class ListAvailableParkingSpaces(APIView):
    """
    API to view all available parkings within the circular area defined  a center (latitude, longitude) and a radius

    URL : /api/parkings/'

    """

    def get(self, request, format=None):
        '''
        Returns all the currently available parking spots
        :param request:
        :param format:
        :return: Serialized Queryset
        '''
        queryset = ParkingSpace.objects.filter(available=True)
        serializer = ParkingSpaceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        '''
        Returns all the parking spots within the circular area
        :param request: lat <INT>, lng <INT>, radius <INT> posted as part of request
        :param format:
        :return: Serialized Queryset
        '''
        remove_ids = []

        # Fetch parameters from request
        try:
            lat = int(request.POST.get("lat"))
            lon = int(request.POST.get("lng"))
            radius = int(request.POST.get("radius"))
        except:
            return Response("Input parameters Invalid", status=status.HTTP_400_BAD_REQUEST)

        # Apply check only on available parking spots
        list_parking_spaces = ParkingSpace.objects.filter(available=True)
        for parking in list_parking_spaces:
            if not check_parking_in_given_area(lat, lon, radius, parking.latitude, parking.longitude):
                remove_ids.append(parking.id)
        list_parking_spaces.filter(id__in=remove_ids).delete()
        serializer = ParkingSpaceSerializer(list_parking_spaces, many=True)
        return Response(serializer.data)


class HandleReservationParkingSpace(APIView):
    """
    Handle blocking, extending and cancelling of a parking reservation

    URL : 'api/handle_parking/
    """

    def post(self, request, format=None):
        '''
        Booking and Extending a parking spot
        :param request: parking_spot <ID>, time_range <INT>
        :param format:
        :return: Serialized ParkingSpace Object
        '''
        try:
            parking_space_id = int(request.POST.get("parking_spot"))
            time_range = int(request.POST.get("time_range"))
        except:
            return Response("Input parameters Invalid", status=status.HTTP_400_BAD_REQUEST)
        if ParkingSpace.objects.filter(id=parking_space_id).exists():
            parking = ParkingSpace.objects.get(id=parking_space_id)
            if parking.available:
                # Booking a spot
                blocked_till = datetime.datetime.now() + timedelta(minutes=time_range)
                parking.available = False
                parking.booked_till = blocked_till
                parking.save()
            else:
                # Extending a spot
                ParkingSpace.objects.filter(id=parking_space_id).update(
                    booked_till=F('booked_till') + timedelta(minutes=time_range))
            serializer = ParkingSpaceSerializer(parking)
            return Response(serializer.data)
        return Response("Not a valid parking spot", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        '''
        cancel reservation of a parking spot
        :param request: parking_spot <ID>
        :param format:
        :return: Serialized ParkingSpace Object
        '''
        parking_space_id = int(request.POST.get("parking_spot"))
        if ParkingSpace.objects.filter(id=parking_space_id).exists():
            ParkingSpace.objects.filter(id=parking_space_id, available=False).update(booked_till=None, available=True)
            serializer = ParkingSpaceSerializer(ParkingSpace.objects.get(id=parking_space_id))
            return Response(serializer.data)
        return Response("Not a valid parking spot", status=status.HTTP_400_BAD_REQUEST)


class ListReservedSpots(APIView):
    """
    List all reserved parking spots.

    URL : 'api/view_booked_parkings/
    """

    def get(self, request, format=None):
        '''
        List all the reserved parking spots
        :param request:
        :param format:
        :return:
        '''
        list_booked_parking_spaces = ParkingSpace.objects.filter(available=False)
        serializer = ParkingSpaceSerializer(list_booked_parking_spaces, many=True)
        return Response(serializer.data)


class CreateDummyData(TemplateView):
    """
    Add dummy data to database
    """
    template_name = "App.html"

    def get(self, request, *args, **kwargs):
        i = 0
        n = 50
        max_lat = max_lon = 100
        while i < n:
            lat = random.randint(0, max_lat)
            lon = random.randint(0, max_lon)
            created, _ = ParkingSpace.objects.get_or_create(latitude=lat, longitude=lon, available=True)
            if created:
                i += 1
            else:
                continue
        return HttpResponse()


###################################### GUI Version 2.0 ##########################################
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import TemplateHTMLRenderer
import json
from django import http
# class Home(TemplateView):
#     template_name = "App.html"
#
#     def get(self, request, *args, **kwargs):
#         return render_to_response(template_name=self.template_name)
#
# @method_decorator(csrf_exempt, name="dispatch")
# class ListAvailableParkingSpaces(TemplateView):
#     template_name = "App.html"
#
#     def get(self, request, *args, **kwargs):
#
#         return HttpResponse()
#
#     def post(self, request, *args, **kwargs):
#         import pdb; pdb.set_trace()
#         return_list = []
#         lat = int(request.POST.get("lat"))
#         lon = int(request.POST.get("lon"))
#         radius = int(request.POST.get("radius"))
#         list_parking_spaces = ParkingSpace.objects.filter(available=True).values("id", "latitude", "longitude")
#         for parking in list_parking_spaces:
#             if check_parking_in_given_area(lat, lon, radius, parking["latitude"], parking["longitude"]):
#                 return_list.append(parking)
#         return Response({'parkings': return_list}, template_name='App.html')
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class BlockParkingSpace(generics.ListCreateAPIView):
#     queryset = ParkingSpace.objects.filter(available=True)
#     serializer_class = ParkingSpaceSerializer
#
#     def post(self, request, *args, **kwargs):
#         parking_space_id = int(request.POST.get("parking_spot"))
#         time_range = int(request.POST.get("time_range"))
#         parking = ParkingSpace.objects.get(id=parking_space_id)
#         if parking.available:
#             blocked_till = datetime.datetime.now() + timedelta(minutes=time_range)
#             parking.available = False
#             parking.booked_till = blocked_till
#             parking.save()
#         else:
#             ParkingSpace.objects.filter(id=parking_space_id).update(
#                 booked_till=F('booked_till') + timedelta(minutes=time_range))
#
#         return HttpResponse(parking)
