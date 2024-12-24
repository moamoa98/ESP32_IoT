// Cấu hình và hằng số
const API_ENDPOINTS = {
    LED_CONTROL: '/api/led_control/',
 
};

// Hàm chính để điều khiển thiết bị
async function controlHome(action, device) {
    try {
        const response = await fetch(API_ENDPOINTS.LED_CONTROL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action, device })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Success:', data);
        return data;

    } catch (error) {
        console.error('Error controlling device:', error);
        // Có thể thêm xử lý UI để hiển thị lỗi cho người dùng
        throw error;
    }
}

// Hàm helper để thiết lập event listener cho các thiết bị
function setupDeviceControl(deviceId) {
    const element = document.getElementById(deviceId);
    if (!element) {
        console.warn(`Element with id ${deviceId} not found`);
        return;
    }

    element.addEventListener('change', async function() {
        try {
            const action = this.checked ? 'on' : 'off';
            console.log(`${deviceId} state: ${action.toUpperCase()}`);
            
            const result = await controlHome(action, deviceId);
            console.log('Control result:', result);

            // Có thể thêm phản hồi trực quan cho người dùng
            if (result.status === 'success') {
                // Thêm phản hồi thành công (có thể là toast notification)
            }
        } catch (error) {
            console.error(`Failed to control ${deviceId}:`, error);
            // Hiển thị lỗi cho người dùng
            this.checked = !this.checked; // Revert trạng thái switch
        }
    });
}

// Danh sách các thiết bị cần điều khiển
const devices = [
    'tog-light-lee',
    'tog-light-micheal',
    'tog-light-larry',
    'tog-light-jack',
    'tog-fan-micheal',
    'tog-fan-jack',
    'tog-gate'
];

// Khởi tạo các controls khi DOM đã sẵn sàng
document.addEventListener('DOMContentLoaded', function() {
    // Thiết lập điều khiển cho tất cả các thiết bị
    devices.forEach(deviceId => setupDeviceControl(deviceId));
    
    // Có thể thêm code khởi tạo khác ở đây
    console.log('Smart home control system initialized');
});

// Test function để log request
// async function testControl() {
//     try {
//         const response = await fetch('/api/led_control/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 action: 'on',
//                 device: 'test-device'
//             })
//         });
        
//         console.log('Response status:', response.status);
//         const data = await response.json();
//         console.log('Response data:', data);
        
//     } catch (error) {
//         console.error('Error details:', {
//             name: error.name,
//             message: error.message,
//             stack: error.stack
//         });
//     }
// }

// // Basic event listener
// document.addEventListener('DOMContentLoaded', function() {
//     // Test với một nút đơn giản
//     const button = document.createElement('button');
//     button.textContent = 'Test LED Control';
//     button.onclick = testControl;
//     document.body.appendChild(button);
    
//     console.log('Test system initialized');
// });

// console.log('123')