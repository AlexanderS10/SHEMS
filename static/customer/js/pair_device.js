function filterModels(selectedDeviceType) {//Iterator for the device models
    let deviceModels = document.getElementById('device_model').getElementsByTagName('option');

    for (let i = 0; i < deviceModels.length; i++) {
        let model = deviceModels[i];
        if (model.getAttribute('data-device-type') === selectedDeviceType || selectedDeviceType === '') {
            model.style.display = '';
        } else {
            model.style.display = 'none';
        }
    }

    // Automatically select the first model for the new device type
    let firstModel = document.querySelector('#device_model [data-device-type="' + selectedDeviceType + '"]');
    if (firstModel) {
        document.getElementById('device_model').value = firstModel.value;
    }
}
    // Event listener for device type change
document.getElementById('device_type').addEventListener('change', function() {
    let selectedDeviceType = this.value;
    filterModels(selectedDeviceType);
});

// Filter models based on initially selected device type (on page load)
window.onload = function() {
    let selectedDeviceType = document.getElementById('device_type').value;
    filterModels(selectedDeviceType);
};

function confirmDelete() {
    return confirm('Are you sure you want to deactivate this device?');
}

function confirmActivate(){
    return confirm('Are you sure you want to activate this device?');
}