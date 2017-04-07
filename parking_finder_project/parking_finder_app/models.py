from django.db import models


class ParkingSpace(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    available = models.BooleanField(default=True)
    booked_till = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (("latitude", "longitude"),)
        ordering = ["latitude", "longitude"]


    def __str__(self):
        return "Parking Space {0} at {1},{2} {3} blocked till {4}".format(self.id, self.latitude, self.longitude, self.available, self.booked_till)