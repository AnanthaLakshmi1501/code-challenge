from rest_framework import serializers
from .models import Weather, WeatherStats


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = [
            "date",
            "maximum_temperature",
            "minimum_temperature",
            "precipitation",
            "station_id",
        ]


class WeatherStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStats
        fields = [
            "year",
            "total_acc_precipitation",
            "avg_min_temp",
            "avg_max_temp",
            "station_id",
        ]
