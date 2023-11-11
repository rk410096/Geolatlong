Project setup
1.install python
2.install OSGeo4W
3.Create Python Virtual Environment
4.Activate virtual Environvent
5.Install Django
6.Install GDAL for Python
	pip install GDAL‑3.X.X‑cp3X‑cp3X‑win_amd64.whl
	or
	pip install C:\Users\Rajesh\Downloads\GDAL-3.4.3-pp38-pypy38_pp73-win_amd64.whl


# settings.py file
import os
Step 7:
# use this if setting up on Windows 10 with GDAL installed from OSGeo4W using defaults
if os.name == 'nt':
    VIRTUAL_ENV_BASE = os.environ['VIRTUAL_ENV']
    os.environ['PATH'] = os.path.join(VIRTUAL_ENV_BASE, r'.\Lib\site-packages\osgeo') + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(VIRTUAL_ENV_BASE, r'.\Lib\site-packages\osgeo\data\proj') + ';' + os.environ['PATH']

INSTALLED_APPS = [
    'django.contrib.gis',
    'leaflet',
    'rest_framework',
    'gis_app',
    
]

## Leaftet setting for admin panel
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-.023,36.87),
    'DEFAULT_ZOOM': 5,
    'MAX_ZOOM':20,
    'MIN_ZOOM':3,
    'SCALE':'both',
    'ATTRIBUTION_PREFIX':'RAJESH'
}



#####Setup for postgis database

1.Install postgresql with sapital data driver
2.Run command "CREATE EXTENSION postgis;"
3.Configure in settings.py file 
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geo_db',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

POST API
http://127.0.0.1:9000/gis_app/location/
# POINT(longitude latitude)

{
    "coordinates": "POINT(38.93285677254418 -77.07015970830255)"
}

PATCH API
http://127.0.0.1:9000/gis_app/location/?location_id=2
{
    "coordinates": "POINT(38.93285677254418 -77.07015970830255)"
}

DELTE API
http://127.0.0.1:9000/gis_app/location/?location_id=2
