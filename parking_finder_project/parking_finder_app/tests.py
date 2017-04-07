from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse

from parking_finder_app.models import ParkingSpace


class ParkingSpaceTestCase(APITestCase):
    def test_available_list(self):
        url = reverse('avalable_parkings')
        response = self.client.get(url)
        self.assertEqual(len(response.data), ParkingSpace.objects.filter(available=True).count())

    def test_reserved_list(self):
        url = reverse('reserved_parking')
        response = self.client.get(url)
        self.assertEqual(len(response.data), ParkingSpace.objects.filter(available=False).count())
