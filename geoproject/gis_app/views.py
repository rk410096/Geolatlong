from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import LocationSerializer
from . models import Location
from django.contrib.gis.geos import GEOSGeometry
import json
# Create your views here.

import requests

def get_weather_data(coordinates):
    url = f"https://api.weather.gov/points/{coordinates[1]},{coordinates[0]}"
    headers = {"User-Agent": "gis_app"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        forecast_url = data['properties']['forecast']
        response2 = requests.get(forecast_url, headers=headers)
        data2 = response2.json()
        temperature = data2['properties']['periods'][0]['temperature']
        humidity = data2['properties']['periods'][0]['relativeHumidity']['value']
        return temperature, humidity
    else:
        return 'NA', 'NA'

def mapview(request):
    locations = Location.objects.all()

    weather_data = []
    for location in locations:
        coordinates = GEOSGeometry(location.coordinates, srid=4326)  # Assuming the SRID is 4326
        temperature, humidity = get_weather_data((coordinates.x, coordinates.y))
        weather_data.append({
            'latitude': coordinates.y,
            'longitude': coordinates.x,
            'temperature': temperature,
            'humidity': humidity,
        })
    print("Weather data", weather_data)
    serialized_weather_data = json.dumps(weather_data)
    context = {'weather_data': serialized_weather_data}
    return render(request, 'index.html', context=context)

class LocationView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        params = request.data
        serializer = LocationSerializer(data=params)
        if serializer.is_valid():
            serializer.save()
            return Response({"flag": 1, "message": "Coordinates add successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"flag": 0, "message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, *args, **kwargs):
        params = request.data
        try:
            location_id = request.GET['location_id']
        except KeyError:
            return Response({"flag": 0, "message": "Please provide location id."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            queryset = Location.objects.get(id=location_id)
        except:
            return Response({"flag": 0, "message": "Location id does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = LocationSerializer(queryset,params)
            if serializer.is_valid():
                serializer.save()
                return Response({"flag": 1, "message": "Coordinates add successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"flag": 0, "message": f"Something went wrong-{e}."}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        try:
            location_id = request.GET['location_id']
        except KeyError:
            return Response({"flag": 0, "message": "Please provide location id."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            queryset = Location.objects.get(id=location_id)
        except:
            return Response({"flag": 0, "message": "Location id does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            queryset.delete()
            return Response({"flag": 1, "message": "Location deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"flag": 0, "message": f"Something went wrong-{e}."}, status=status.HTTP_400_BAD_REQUEST)