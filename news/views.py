# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from urllib.request import urlopen
import urllib.parse
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
def led_control(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            action = data.get('action')  # 'on' hoặc 'off'
            device = data.get('device')  # Tên thiết bị

            logger.info(f"Received action: {action} for device: {device}")

            # Chuyển đổi action thành giá trị số
            value = 1 if action == 'on' else 0
            device_encoded=urllib.parse.quote(device)
            # Xây dựng URL với các tham số cần thiết
            url = f'{THINGSPEAK_BASE_URL}/update?api_key={THINGSPEAK_API_KEY}&field3={value}&field4={device}'

            # Gửi request đến ThingSpeak bằng urlopen
            try:
                with urlopen(url, timeout=30) as response:
                    result = response.read().decode('utf-8')  # Đọc và giải mã phản hồi
                    logger.info(f"ThingSpeak response: {result}")

                    if result.strip():  # Đảm bảo phản hồi không rỗng
                        return JsonResponse({
                            'status': 'success',
                            'message': f'Device {device} turned {action}',
                            'response': result
                        })
                    else:
                        logger.warning("ThingSpeak returned an empty response")
                        return JsonResponse({
                            'status': 'error',
                            'message': 'ThingSpeak returned an empty response'
                        }, status=500)
            except Exception as e:
                logger.error(f"Error sending request to ThingSpeak: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'Failed to update ThingSpeak: {str(e)}'
                }, status=500)

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({
                'status': 'error', 
                'message': 'Invalid JSON data'
            }, status=400)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Only POST requests are allowed'
    }, status=405)


def index(request):
    return render(request, 'index.html')