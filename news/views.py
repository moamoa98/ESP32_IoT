from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData, DeviceState
import json

@csrf_exempt
def get_temp_humidity(request):
    try:
        latest_data = SensorData.objects.latest('timestamp')
        return JsonResponse({
            'status': 'success',
            'temperature': latest_data.temperature,
            'humidity': latest_data.humidity,
            'timestamp': latest_data.timestamp
        })
    except SensorData.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No data available'}, status=404)

@csrf_exempt
def update_device_state(request):
    try:
        data = json.loads(request.body)
        device_id = data.get('device')
        action = data.get('action')
        
        if not device_id or action not in ['on', 'off']:
            return JsonResponse({'status': 'error', 'message': 'Invalid parameters'}, status=400)
        
        state = action == 'on'
        device, created = DeviceState.objects.update_or_create(
            device_id=device_id,
            defaults={'state': state}
        )
        return JsonResponse({'status': 'success', 'device': device_id, 'state': state})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def index(request):
    return render(request, 'index.html')