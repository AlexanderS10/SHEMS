let energyUsageData = [];
let myChart;

function createOrUpdateChart(data) {
    preprocessDate(data); // Convert all dates to day format
    const uniqueDates = getUniqueDayDates(data); // Get unique day dates
    const labels = uniqueDates.map(date => date);

    const uniqueDeviceIds = [...new Set(data.map(item => item.device_id))];

    // Create a mapping of device IDs to device names
    const deviceNames = {};
    data.forEach(item => {
        if (!deviceNames[item.device_id]) {
            deviceNames[item.device_id] = item.device_name;
        }
    });

    const datasets = uniqueDeviceIds.map(deviceId => {
        const filteredData = data.filter(item => item.device_id === deviceId);
        const values = labels.map(label => {
            const dataForDate = filteredData.find(item => item.day_date === label);
            return dataForDate ? dataForDate.avg_daily_energy : null;
        });
        const color = getRandomColor(); // Generate a single random color for each device

        return {
            label: deviceNames[deviceId], // Use device name from the mapping
            data: values,
            backgroundColor: color, // Set the background color for the area under the line
            borderColor: color, // Set the line color
            pointBackgroundColor: color, // Set the point (dot) color
            borderWidth: 2, // Increase line width
            pointRadius: 5, // Increase point size
            fill: false,
        };
    });

    const ctx = document.getElementById('history-chart').getContext('2d');
    if (window.myChart instanceof Chart) {
        window.myChart.data.labels = labels;
        window.myChart.data.datasets = datasets;
        window.myChart.update();
    } else {
        window.myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets,
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Energy Consumption', 
                        font: {
                            size: 18,
                        },
                    },
                },
                scales: {
                    x: {
                        type: 'category',
                        title: {
                            display: true,
                            text: 'Date', // X-axis title
                            font: {
                                size: 14,
                            },
                        },
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Energy (kWh)', // Y-axis title
                            font: {
                                size: 14,
                            },
                        },
                    },
                },
            },
        });
    }
}

// Function to convert all dates to day format
function preprocessDate(data) {
    data.forEach(item => {
        const date = new Date(item.day_date);
        item.day_date = date.toLocaleDateString('en-US', { day: 'numeric' });
    });
}
// Function to get unique day dates
function getUniqueDayDates(data) {
    const uniqueDates = [...new Set(data.map(item => item.day_date))];
    return uniqueDates;
}

// Function to generate random colors for each dataset
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}


let selectedLocation = ''; // Global variable to store the selected location ID
let debounceTimer;
function debounce(func, delay) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(func, delay);
}
function fetchDataAndInitializeChart(locationId, days) {
    // Check if 'days' is empty or undefined, then set it to the default value (7)
    days = days || 7;
    const url = locationId !== 'all' ? `/api/history-energy-usage/${locationId}/` : '/api/history-energy-usage/';
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ location_id: locationId, days: days }),
    })
    .then(response => response.json())
    .then(data => {
        energyUsageData = data;
        createOrUpdateChart(energyUsageData);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}
function fetchAndUpdateChartDelayed() {
    const delayDuration = 500; //Set the delay duration in milliseconds
    const inputValue = parseInt(document.getElementById('numberOfDays').value, 10);
    const minValue = 3;
    const maxValue = 20;

    // Check if the inputValue is within the specified range (3 to 20)
    if (!isNaN(inputValue) && inputValue >= minValue && inputValue <= maxValue) {
        debounce(function () {
            fetchAndUpdateChart();
        }, delayDuration);
    } else {
        window.alert('Please enter a value between 3 and 20.');
    }
}
const defaultSelection = document.getElementById('dataSelector').value;
fetchDataAndInitializeChart(defaultSelection);

// Function to fetch data based on the current selection
function fetchAndUpdateChart() {
    const selectedValue = document.getElementById('dataSelector').value;
    const selectedDays = document.getElementById('numberOfDays').value; // Get the selected days
    fetchDataAndInitializeChart(selectedValue, selectedDays);
}
// Add event listeners to the dropdown and input elements
document.getElementById('dataSelector').addEventListener('change', fetchAndUpdateChart);
document.getElementById('numberOfDays').addEventListener('input', fetchAndUpdateChartDelayed);





