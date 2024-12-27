
from django.urls import path
from .views import index
from django.urls import path
from .views import update_device_state,update_sensor,get_sensor_data,check_number,check_esp32_status




# urlpatterns = [
#     path('', index, name='index'),
#     # path('led_control/',led_control, name='led_control'),
#     # path('get_temp_humidity/',get_temp_humidity, name='get_temp_humidity'),
#     # path('api/temp-humidity/', get_temp_humidity),
#     # path('api/get_thingspeak_data/', get_thingspeak_data),
#     # path('api/led_control/', led_control),
# ]

urlpatterns = [
    path('update_sensor/',update_sensor,name='update_sensor'),
    path('check_esp32_status/', check_esp32_status, name='check_esp32_status'),
    path('get_sensor_data/',get_sensor_data,name='get_sensor_data'),
    path('update_device_state/', update_device_state, name='update_device_state'),
    path('', index, name='index'),
    path('check_number/<int:number>/', check_number),

]




