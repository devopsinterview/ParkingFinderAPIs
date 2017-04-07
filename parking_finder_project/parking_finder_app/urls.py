"""ParkingFinderApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/parkings/', ListAvailableParkingSpaces.as_view(), name='avalable_parkings'),
    url(r'^api/handle_parking/', HandleReservationParkingSpace.as_view(), name="handle_parking"),
    url(r'^api/view_booked_parkings/', ListReservedSpots.as_view(), name="reserved_parking"),
    url(r'^home/$', CreateDummyData.as_view(), name="dummy_data")
]
