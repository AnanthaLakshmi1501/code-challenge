from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Weather, WeatherStats
from .serializers import WeatherSerializer, WeatherStatsSerializer


class Weather(generics.ListAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["date", "station_id"]


class WeatherStats(generics.ListAPIView):
    queryset = WeatherStats.objects.all()
    serializer_class = WeatherStatsSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["year", "station_id"]
