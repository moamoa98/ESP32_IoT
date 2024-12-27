from django.db import models

# Create your models here.
from django.db import models

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temp: {self.temperature}, Humidity: {self.humidity}, Time: {self.timestamp}"


class DeviceState(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    state = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

