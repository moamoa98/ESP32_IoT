
from django.urls import path
from .views import index,get_temp_humidity
from django.urls import path
from .views import get_temp_humidity, update_device_state



# urlpatterns = [
#     path('', index, name='index'),
#     # path('led_control/',led_control, name='led_control'),
#     # path('get_temp_humidity/',get_temp_humidity, name='get_temp_humidity'),
#     # path('api/temp-humidity/', get_temp_humidity),
#     # path('api/get_thingspeak_data/', get_thingspeak_data),
#     # path('api/led_control/', led_control),
# ]

urlpatterns = [
    path('get_temp_humidity/', get_temp_humidity, name='get_temp_humidity'),
    path('update_device_state/', update_device_state, name='update_device_state'),
    path('', index, name='index'),
]




