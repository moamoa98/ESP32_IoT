
from django.urls import path
from .views import index,led_control,get_temp_humidity,get_thingspeak_data




urlpatterns = [
    path('', index, name='index'),
    path('led_control/',led_control, name='led_control'),
    path('get_temp_humidity/',get_temp_humidity, name='get_temp_humidity'),
    path('api/temp-humidity/', get_temp_humidity),
    path('api/get_thingspeak_data/', get_thingspeak_data),
    path('api/led_control/', led_control),
]


