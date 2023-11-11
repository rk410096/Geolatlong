from rest_framework.test import APITestCase
from gis_app.models import Location
from gis_app.serializers import LocationSerializer

class LocationSerializerTestCase(APITestCase):
    def test_location(self):
        data = {"coordinates": "POINT(38.93285677254418 -77.07015970830255)"}
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors,{})