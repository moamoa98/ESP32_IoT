# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from datetime import datetime
import json
import logging
logger = logging.getLogger(__name__)

# ESP32 và ThingSpeak configuration
ESP32_IP = '118.69.234.7'
THINGSPEAK_API_KEY = '850L5YHIZ5AIC93F'
THINGSPEAK_CHANNEL_ID = '2790754'  # Thay bằng channel ID của bạn
THINGSPEAK_READ_API = 'https://api.thingspeak.com/channels/2790754/feeds.json'
THINGSPEAK_BASE_URL = 'https://api.thingspeak.com'

def get_thingspeak_data(field=None, results=1):
    """
    Lấy dữ liệu từ ThingSpeak với xử lý lỗi tốt hơn
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
            timeout=10  # Tăng timeout
        )
        
        response.raise_for_status()  # Raise exception for bad status codes
        
        data = response.json()
        
        if not data.get('feeds'):
            logger.warning("No data received from ThingSpeak")
            return None
            
        return data
        
    except requests.Timeout:
        logger.error("ThingSpeak API timeout")
        return None
    except requests.RequestException as e:
        logger.error(f"ThingSpeak API error: {str(e)}")
        return None
    except (ValueError, KeyError) as e:
        logger.error(f"Error parsing ThingSpeak data: {str(e)}")
        return None
@csrf_exempt
def get_temp_humidity(request):
    """Lấy dữ liệu nhiệt độ và độ ẩm mới nhất"""
    try:
        thingspeak_data = get_thingspeak_data(results=1)
        
        if not thingspeak_data or not thingspeak_data.get('feeds'):
            return JsonResponse({
                'status': 'error',
                'message': 'No data available from ThingSpeak'
            }, status=404)
        
        latest_feed = thingspeak_data['feeds'][-1]
        
        # Validate data
        temperature = latest_feed.get('field1')
        humidity = latest_feed.get('field2')
        
        if temperature is None or humidity is None:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid data format from ThingSpeak'
            }, status=500)
            
        try:
            temperature = round(float(temperature), 2)
            humidity = round(float(humidity), 2)
        except (ValueError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid numeric data from ThingSpeak'
            }, status=500)
        
        return JsonResponse({
            'status': 'success',
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': latest_feed['created_at']
        })
        
    except Exception as e:
        logger.error(f"Error in get_temp_humidity: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error'
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