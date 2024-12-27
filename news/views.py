from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
# Biến global để lưu thời gian cập nhật cuối cùng
last_update_time = None
# Lưu giá trị trong memory
latest_sensor_data = {
    'temperature': 0,
    'humidity': 0
}

@csrf_exempt
def check_esp32_status(request):
    global last_update_time
    
    if last_update_time is None:
        return JsonResponse({'status': 'offline'})
        
    # Kiểm tra xem lần cập nhật cuối cùng có trong vòng 10 giây không
    time_difference = datetime.now() - last_update_time
    if time_difference <= timedelta(seconds=10):
        return JsonResponse({'status': 'online'})
    return JsonResponse({'status': 'offline'})
@csrf_exempt
def update_sensor(request):
    global last_update_time
    if request.method == 'GET':
        return JsonResponse(latest_sensor_data)  # Trả về dữ liệu hiện tại nếu là GET
    elif request.method == 'POST':
        last_update_time = datetime.now()  # Cập nhật thời gian
        latest_sensor_data['temperature'] = float(request.POST.get('temperature', 0))
        latest_sensor_data['humidity'] = float(request.POST.get('humidity', 0))
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
@csrf_exempt
def get_sensor_data(request):
    return JsonResponse({'status': 'success', **latest_sensor_data})

# Tạo một dictionary để lưu trạng thái thiết bị (giả lập)
device_states = {}
@csrf_exempt
def update_device_state(request):
    try:
        if request.method == 'GET':
            device_id = request.GET.get('device')
            if not device_id:
                return JsonResponse({'status': 'error', 'message': 'Device ID is required'}, status=400)

            # Lấy trạng thái từ device_states, mặc định là False nếu không tìm thấy
            state = device_states.get(device_id, False)
            return JsonResponse({'status': 'success', 'device': device_id, 'state': state})

        elif request.method == 'POST':
            data = json.loads(request.body)
            device_id = data.get('device')
            action = data.get('action')

            if not device_id or action not in ['on', 'off']:
                return JsonResponse({'status': 'error', 'message': 'Invalid parameters'}, status=400)

            state = action == 'on'
            device_states[device_id] = state
            return JsonResponse({'status': 'success', 'device': device_id, 'state': state})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def get_all_device_states(request):
    return JsonResponse({'status': 'success', 'device_states': device_states})

def index(request):
    return render(request, 'index.html')

def check_number(request,number):
    if number>0:
        res=f'{number} là số dương'
    else:
        res=f'{number} là số âm'

    return HttpResponse(res)
