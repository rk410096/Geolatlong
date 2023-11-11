from django.contrib.gis.db import models

class Location(models.Model):
    coordinates = models.PointField()