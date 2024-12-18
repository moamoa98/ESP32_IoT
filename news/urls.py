
from django.urls import path
from .views import index,led_control,get_temp_humidity




urlpatterns = [
    path('', index, name='index'),
    path('led_control/',led_control, name='led_control'),
    path('get_temp_humidity/',get_temp_humidity, name='get_temp_humidity'),
]


