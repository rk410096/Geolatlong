from django.test import TestCase
from gis_app.models import Location
from django.contrib.gis.geos import Point

class LocationModelTest(TestCase):
    def test_location_create(self):
        expected_coordinates = Point(38.93285677254418, -77.07015970830255)
        location = Location.objects.create(coordinates=expected_coordinates)
        self.assertEqual(location.coordinates, expected_coordinates)