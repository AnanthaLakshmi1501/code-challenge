from django.db import models


# Create your models here.
class Weather(models.Model):
    date = models.CharField(max_length=20)
    maximum_temperature = models.IntegerField()
    minimum_temperature = models.IntegerField()
    precipitation = models.IntegerField()
    station_id = models.CharField(max_length=20)

    class Meta:
        unique_together = ("date", "station_id")


class WeatherStats(models.Model):
    station_id = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    avg_max_temp = models.IntegerField()
    avg_min_temp = models.IntegerField()
    total_acc_precipitation = models.IntegerField()

    class Meta:
        unique_together = ("year", "station_id")
