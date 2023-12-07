 document.getElementById('device_type').addEventListener('change', function() {
        let selectedDeviceType = this.value;
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
    });

function confirmDelete() {
    return confirm('Are you sure you want to delete this device? All associated data will be removed.');
}