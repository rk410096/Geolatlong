from django.urls import path
from .import views
urlpatterns = [
    path('location/', views.LocationView.as_view(),name='location'),
    path('', views.mapview,name='mapview'),
]