from django.db import models

# Create your models here.
from django.db import models

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

SensorData.objects.create(temperature=25.5, humidity=60.0)

class DeviceState(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    state = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

