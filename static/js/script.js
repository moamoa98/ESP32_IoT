alert('hello')
function controlHome(action, device) {
    fetch('/led_control/', {
        method: 'POST',
        body: new URLSearchParams({
            'action': action,
            'device': device
        }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })

    .then(data => {
        console.log(data);
    })

}

document.addEventListener('DOMContentLoaded',function(){
    document.getElementById('tog-light-lee').addEventListener('change', function() {
        console.log('Toggle 1 state: ' + (this.checked ? 'ON' : 'OFF'));
        const action= this.checked? 'on' : 'off';
        const device='tog-light-lee';
        controlHome(action,device)
    });
    
    document.getElementById('tog-light-micheal').addEventListener('change', function() {
        console.log('Toggle 1 state: ' + (this.checked ? 'ON' : 'OFF'));
        const action= this.checked? 'on' : 'off';
        const device='tog-light-micheal';
        controlHome(action,device)
    });
    
    document.getElementById('tog-light-larry').addEventListener('change', function() {
        console.log('Toggle 1 state: ' + (this.checked ? 'ON' : 'OFF'));
        const action= this.checked? 'on' : 'off';
        const device='tog-light-larry';
        controlHome(action,device)
    });
    
    document.getElementById('tog-light-jack').addEventListener('change', function() {
        console.log('Toggle 1 state: ' + (this.checked ? 'ON' : 'OFF'));
        const action= this.checked? 'on' : 'off';
        const device='tog-light-jack';
        controlHome(action,device)
    });
    
    document.getElementById('tog-fan-micheal').addEventListener('change', function() {
        console.log('Toggle 1 state: ' + (this.checked ? 'ON' : 'OFF'));
        const action= this.checked? 'on' : 'off';
        const device='tog-fan-micheal';
        controlHome(action,device)
    });
    
    document.getElementById('tog-fan-jack').addEventListener('change', function() {
        console.log('Toggle 1 state: ' + (this.checked ? 'ON' : 'OFF'));
        const action= this.checked? 'on' : 'off';
        const device='tog-fan-jack';
        controlHome(action,device)
    });
    
    document.getElementById('tog-gate').addEventListener('change', function() {
        console.log('Toggle 1 state: ' + (this.checked ? 'ON' : 'OFF'));
        const action= this.checked? 'on' : 'off';
        const device='tog-gate';
        controlHome(action,device)
    });
    
    
    
});



