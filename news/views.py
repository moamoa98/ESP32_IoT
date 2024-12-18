from django.shortcuts import render
from django.http import request
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

ESP32_IP='192.168.1'
@csrf_exempt

def get_temp_humidity(request):
    try:
        # Gửi request đến endpoint của ESP32
        response = requests.get(f'http://{ESP32_IP}/temp-humidity', timeout=5)
        
        if response.status_code == 200:
            # Trả về dữ liệu JSON từ ESP32
            return JsonResponse(response.json())
        else:
            # Trả về lỗi nếu không lấy được dữ liệu
            return JsonResponse({
                'status': 'error', 
                'message': 'Failed to fetch temperature and humidity'
            }, status=400)
    
    except requests.RequestException as e:
        # Xử lý lỗi kết nối
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)

@csrf_exempt
def led_control(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        device = request.POST.get('device')
        
        try:
            url = f'http://{ESP32_IP}/led/{action}'
            response = requests.get(url, params={'device': device})
            
            if response.status_code == 200:
                return JsonResponse({'status': 'success', 'message': f'Device {device} turned {action}'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to control device'}, status=400)
        
        except requests.RequestException as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)
# Create your views here.
def index(request):
    return render(request, 'index.html')