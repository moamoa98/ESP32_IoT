

document.addEventListener("DOMContentLoaded", function () {
    const devices = [
        'tog-light-lee',
        'tog-light-micheal',
        'tog-light-larry',
        'tog-light-jack',
        'tog-fan-micheal',
        'tog-fan-jack',
        'tog-gate'
    ];

    devices.forEach((deviceId) => {
        const toggleButton = document.getElementById(deviceId);

        if (toggleButton) {
            toggleButton.addEventListener("click", function () {
                // Sử dụng setTimeout để đảm bảo trạng thái đã được cập nhật
                setTimeout(() => {
                    const isPressed = toggleButton.getAttribute("aria-pressed") === "true";
                    console.log(`Trạng thái nút ${deviceId}:`, isPressed ? "Bật" : "Tắt");
                    const action=isPressed ? "on" : "off";

                    fetch('/update_device_state/',{
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            device: deviceId,
                            action: action
                            
                        })
                        
                    })                        
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                console.log(`Thiết bị ${deviceId} đã được đặt thành ${action}`);
                            } else {
                                console.error('Lỗi khi gửi trạng thái:', data.message);
                            }
                        })
                        .catch(error => console.error('Lỗi kết nối:', error));



                }, 0);
            });
        } else {
            console.error(`Không tìm thấy nút #${deviceId}`);
        }
    });
});

document.addEventListener('DOMContentLoaded', function(e) {

    function updateStatus() {
        const statusDiv = document.getElementById('status');
        const statusText = document.getElementById('status-text');
        const deviceStatus = document.getElementById('device-status');

        if (navigator.onLine) {
            statusDiv.className = 'status border border-success online';
            statusText.textContent = 'Online';
            deviceStatus.textContent = 'ESP32 đang hoạt động';
        } else {
            statusDiv.className = 'status border border-danger offline';
            statusText.textContent = 'Offline';
            deviceStatus.textContent = 'ESP32 đang offline';
        }
    }

    // Update status on load
    window.addEventListener('load', updateStatus);

    // Update status when online/offline events are triggered
    window.addEventListener('online', updateStatus);
    window.addEventListener('offline', updateStatus);

});


function checkCSSFiles() {
    // Lấy tất cả các thẻ link trong document
    const links = document.getElementsByTagName('link');
    
    // Mảng chứa các file CSS
    const cssFiles = [];
    
    // Kiểm tra từng thẻ link
    for(let link of links) {
        // Kiểm tra rel="stylesheet"
        if(link.rel === 'stylesheet' && link.href) {
            cssFiles.push(link.href);
        }
    }
    
    // Kiểm tra cả style tag
    const styles = document.getElementsByTagName('style');
    
    // Kết quả
    if(cssFiles.length > 0 || styles.length > 0) {
        console.log('Website có sử dụng CSS');
        console.log('Số file CSS:', cssFiles.length);
        console.log('Số internal style tags:', styles.length);
        console.log('Danh sách file CSS:', cssFiles);
    } else {
        console.log('Website không sử dụng CSS');
    }
}

// Gọi hàm kiểm tra
checkCSSFiles();



// async function updateDeviceState(action,deviceId) {
//     try {
//         const response = await fetch(API_ENDPOINTS.DEVICE_STATE, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ device: deviceId, action }),
//         });

//         if (response.ok) {
//             const data = await response.json();
//             console.log(`Device ${deviceId} set to ${action}:`, data);
//         } else {
//             console.error('Failed to update device state:', response.status);
//         }
//     } catch (error) {
//         console.error('Error:', error);
//     }
// }

// // Hàm helper để thiết lập event listener cho các thiết bị
// function setupDeviceControl(deviceId) {
//     const element = document.getElementById(deviceId);
//     if (!element) {
//         console.warn(`Element with id ${deviceId} not found`);
//         return;
//     }

//     element.addEventListener('change', async function() {
//         try {
//             const action = this.checked ? 'on' : 'off';
//             console.log(`${deviceId} state: ${action.toUpperCase()}`);
            
//             // const result = await controlHome(action, deviceId);
//             console.log('Control result:', result);

//             // Có thể thêm phản hồi trực quan cho người dùng
//             if (result.status === 'success') {
//                 // Thêm phản hồi thành công (có thể là toast notification)
//             }
//         } catch (error) {
//             console.error(`Failed to control ${deviceId}:`, error);
//             // Hiển thị lỗi cho người dùng
//             this.checked = !this.checked; // Revert trạng thái switch
//         }
//     });
// }

// // Danh sách các thiết bị cần điều khiển


// // Khởi tạo các controls khi DOM đã sẵn sàng
// document.addEventListener('DOMContentLoaded', function() {
//     // Thiết lập điều khiển cho tất cả các thiết bị
//     devices.forEach(deviceId => setupDeviceControl(deviceId));
    
//     // Có thể thêm code khởi tạo khác ở đây
//     console.log('Smart home control system initialized');
// });

