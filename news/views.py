# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from datetime import datetime
import json

# ESP32 và ThingSpeak configuration
ESP32_IP = '118.69.234.7'
THINGSPEAK_API_KEY = '850L5YHIZ5AIC93F'
THINGSPEAK_CHANNEL_ID = '2790754'  # Thay bằng channel ID của bạn
THINGSPEAK_READ_API = 'https://api.thingspeak.com/channels/2790754/feeds.json'

def get_thingspeak_data(field=None, results=1):
    """
    Lấy dữ liệu từ ThingSpeak
    field: số field cần lấy (1=temperature, 2=humidity)
    results: số lượng kết quả muốn lấy
    """
    try:
        params = {
            'api_key': THINGSPEAK_API_KEY,
            'results': results
        }
        if field:
            params['field'] = field
            
        response = requests.get(
            f'{THINGSPEAK_BASE_URL}/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json',
            params=params,
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException as e:
        print(f"ThingSpeak API error: {str(e)}")
        return None

@csrf_exempt
def get_temp_humidity(request):
    try:
        # Lấy dữ liệu từ cả ESP32 và ThingSpeak
        esp32_response = requests.get(f'http://{ESP32_IP}/temp-humidity', timeout=5)
        thingspeak_data = get_thingspeak_data(results=1)
        
        response_data = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'sources': {}
        }

        # Dữ liệu từ ESP32
        if esp32_response.status_code == 200:
            esp32_data = esp32_response.json()
            response_data['sources']['esp32'] = {
                'temperature': round(float(esp32_data['temperature']), 2),
                'humidity': round(float(esp32_data['humidity']), 2)
            }
        
        # Dữ liệu từ ThingSpeak
        if thingspeak_data and 'feeds' in thingspeak_data and thingspeak_data['feeds']:
            latest_feed = thingspeak_data['feeds'][-1]
            response_data['sources']['thingspeak'] = {
                'temperature': round(float(latest_feed['field1']), 2) if 'field1' in latest_feed else None,
                'humidity': round(float(latest_feed['field2']), 2) if 'field2' in latest_feed else None,
                'timestamp': latest_feed['created_at']
            }

        return JsonResponse(response_data)
        
    except requests.RequestException as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def get_historical_data(request):
    """Lấy dữ liệu lịch sử từ ThingSpeak"""
    try:
        # Số lượng điểm dữ liệu muốn lấy (mặc định 24 giờ - 96 điểm với interval 15 phút)
        results = request.GET.get('results', '96')
        
        thingspeak_data = get_thingspeak_data(results=results)
        
        if thingspeak_data and 'feeds' in thingspeak_data:
            historical_data = []
            for feed in thingspeak_data['feeds']:
                historical_data.append({
                    'timestamp': feed['created_at'],
                    'temperature': round(float(feed['field1']), 2) if 'field1' in feed else None,
                    'humidity': round(float(feed['field2']), 2) if 'field2' in feed else None
                })
            
            return JsonResponse({
                'status': 'success',
                'data': historical_data
            })
        
        return JsonResponse({
            'status': 'error',
            'message': 'No data available'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def led_control(request):
    """Điều khiển thiết bị và lưu trạng thái vào ThingSpeak"""
    if request.method == 'POST':
        action = request.POST.get('action')
        device = request.POST.get('device')
        
        try:
            # Gửi lệnh đến ESP32
            url = f'http://{ESP32_IP}/led/{action}'
            response = requests.get(url, params={'device': device})
            
            if response.status_code == 200:
                # Cập nhật trạng thái lên ThingSpeak (Field 3 cho device status)
                device_status = 1 if action == 'on' else 0
                thingspeak_update_url = f'{THINGSPEAK_BASE_URL}/update'
                requests.get(thingspeak_update_url, params={
                    'api_key': THINGSPEAK_API_KEY,
                    'field3': f"{device}:{device_status}"
                })
                
                return JsonResponse({
                    'status': 'success',
                    'message': f'Device {device} turned {action}'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to control device'
                }, status=400)
                
        except requests.RequestException as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST requests are allowed'
    }, status=405)

def index(request):
    return render(request, 'index.html')