from rest_framework.test import APIClient,APITestCase
from gis_app.models import Location
from  gis_app.serializers import LocationSerializer
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from rest_framework import status
from django.test import TestCase
from django.contrib.gis.geos import Point

class LocationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_location(self):
        url = reverse('location')

        # Send a POST request to create a new location
        data = {"coordinates": "POINT(38.93285677254418 -77.07015970830255)"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        # Convert Point object to string for comparison
        # actual_coordinates_str = str(Location.objects.first().coordinates)

        # Parse the string representation of the Point to ensure consistent formatting
        expected_coordinates_str = Point(38.93285677254418, -77.07015970830255).wkt

        self.assertEqual(Location.objects.first().coordinates.wkt, expected_coordinates_str)

    def test_patch_location(self):
        # Create a location to update
        url = reverse('location') 
        location = Location.objects.create(coordinates="POINT(0.0 0.0)")

        # Send a PATCH request to update the location
        new_coordinates = "POINT(38.93285677254418 -77.07015970830255)"
        data = {"coordinates": new_coordinates}
        url = f'{url}?location_id={location.id}'
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        location.refresh_from_db()
        expected_coordinates = Point(38.93285677254418, -77.07015970830255)
        self.assertEqual(location.coordinates.wkt, expected_coordinates)


    def test_delete_location(self):
        # Create a location to delete
        url = reverse('location') 
        location = Location.objects.create(coordinates="POINT(38.93285677254418 -77.07015970830255)")
        # Send a DELETE request to delete the location
        url = f'{url}?location_id={location.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Location.objects.count(), 0)