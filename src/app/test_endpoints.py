from rest_framework import status
from django.urls import reverse
from .models import Weather, WeatherStats  # Import your Weather model
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "station_id, date, maximum_temperature, minimum_temperature, precipitation",
    [
        ("USC00113879", "20130707", 311, 178, 122),
        ("USC00250640", "20090611", 233, 128, 267),
    ],
)
def test_get_weather(
    client, station_id, date, maximum_temperature, minimum_temperature, precipitation
):
    Weather.objects.create(
        station_id=station_id,
        date=date,
        maximum_temperature=maximum_temperature,
        minimum_temperature=minimum_temperature,
        precipitation=precipitation,
    )
    response = client.get(reverse("weather"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get("results")) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "year, station_id, avg_max_temp, avg_min_temp, total_acc_precipitation",
    [
        ("2003", "USC00110072", 148, 28, 9117),
        ("1994", "USC00110072", 149, 37, 6688),
    ],
)
def test_get_stats(
    client, year, station_id, avg_max_temp, avg_min_temp, total_acc_precipitation
):
    WeatherStats.objects.create(
        year=year,
        station_id=station_id,
        avg_max_temp=avg_max_temp,
        avg_min_temp=avg_min_temp,
        total_acc_precipitation=total_acc_precipitation,
    )

    response = client.get(reverse("weather_stats"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get("results")) == 1
    assert response.json()["count"] == 1
