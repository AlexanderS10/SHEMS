let myChart;
function updateChart(locationId, date) {
    fetchData(locationId, date);
}
function fetchData(locationId, date) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const apiUrl = '/api/device-energy-usage-date/';
    // Construct the API payload
    const apiPayload = {
        location_id: locationId,
        date: date
    };
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(apiPayload)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        createPolarAreaChart(data)
    })
    .catch(error => {
        console.log(error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const dataSelector = document.getElementById('dataSelector');
    const calendarSelector = document.getElementById('calendar-selector');

    // Function to trigger API call and update chart
    function triggerAPICallAndUpdateChart() {
        const selectedLocationId = dataSelector.value;
        const selectedDate = calendarSelector.value;

        // Call the function to update chart with new data
        updateChart(selectedLocationId, selectedDate);
    }

    // Event listeners for the selection change in dataSelector and the date input change
    dataSelector.addEventListener('change', triggerAPICallAndUpdateChart);
    calendarSelector.addEventListener('change', triggerAPICallAndUpdateChart);

    // Call the API function to initialize the chart on initial page load
    triggerAPICallAndUpdateChart();
});

function createPolarAreaChart(data) {
    // Process the data to extract labels and dataset values
    const labels = data.map(entry => entry.device_name);
    const values = data.map(entry => entry.total_energy_consumption); // Values for the chart

    const ctx = document.getElementById('location-chart').getContext('2d');
    if (window.polarAreaChart) {
        // If chart exists, destroy it before re-rendering
        window.polarAreaChart.destroy();
    }
    window.polarAreaChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                label: 'Energy Consumption',
                data: values,
                backgroundColor: data.map(entry => getRandomColor()),
                borderWidth: 1
            }]
        },
        options: {

        }
    });
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}