import datetime as dt
import json
import time

import grequests
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from drf_yasg.utils import swagger_auto_schema
from more_itertools import chunked
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from .models import WeatherData
from .swagger_schemas import get_response, post_request, post_response
from drf_yasg import openapi
API_KEY = settings.OPEN_WEATHER_API_KEY
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&id={{}}"
CITIES_IDS = settings.CITIES_IDS

def kelvin_to_celsius(temp_kelvin):
    """Converts Kelvin to Celsius with rounding to 2 decimal places."""
    return round(temp_kelvin - 273.15, 2)

class WeatherDataView(APIView):
    def build_payload(self, weather_data):
        """Creates the JSON payload from the weather data."""
        return {
            "city_id": weather_data["id"],
            "temperature": kelvin_to_celsius(weather_data["main"]["temp"]),
            "humidity": weather_data["main"]["humidity"],
        }

    def call_weather_api(self, user_defined_id, request_time, urls):
        """Generates weather data for the specified cities."""
        yield f'{{"user_defined_id": {json.dumps(user_defined_id)}, "request_time": {json.dumps(request_time.isoformat())}, "city_info": ['
        first_entry = True
        for city_group in chunked(urls, 10):
            if not first_entry:
                yield ","
            first_entry = False
            start_time = time.time()
            responses = grequests.map((grequests.get(url) for url in city_group))
            processed_data = [self.build_payload(resp.json()) for resp in responses if resp and resp.ok]
            weather_entry, _ = WeatherData.objects.get_or_create(
                user_defined_id=user_defined_id,
                defaults={'request_datetime': request_time, 'city_info': {"cities_info": []}}
            )
            weather_entry.city_info["cities_info"].extend(processed_data)
            weather_entry.save()
            yield from (json.dumps(data) for data in processed_data)
            time.sleep(max(0, 11 - (time.time() - start_time)))
        yield "]}"


    @swagger_auto_schema(request_body=post_request(), responses={200: post_response()})
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_defined_id = data.get("user_defined_id")
            if not user_defined_id:
                raise ValueError("User ID is required.")
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except ValueError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

        if WeatherData.objects.filter(user_defined_id=user_defined_id).exists():
            return JsonResponse({"Error": "This user ID is already in use."}, status=400)

        response_stream = StreamingHttpResponse(
            self.call_weather_api(user_defined_id, timezone.now(), (WEATHER_URL.format(id) for id in CITIES_IDS)),
            content_type="text/event-stream"
        )
        response_stream["Cache-Control"] = "no-cache"
        return response_stream


class ProgressView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user_defined_id',
                openapi.IN_PATH,
                description="ID defined by the user.",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: get_response()}
    )
    def get(self, request, user_defined_id):
        weather_data = WeatherData.objects.filter(user_defined_id=user_defined_id).first()
        if not weather_data:
            return JsonResponse({"user_defined_id": user_defined_id, "Status": "User ID not found"}, status=status.HTTP_404_NOT_FOUND)
        progress_percentage = 100 * len(weather_data.city_info["cities_info"]) / len(CITIES_IDS)
        return JsonResponse({"user_defined_id": user_defined_id, "Status": f"{progress_percentage:.2f}%"})
