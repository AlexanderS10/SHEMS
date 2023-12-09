const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent the click event from propagating to document
        const dropdownMenu = this.nextElementSibling;
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });
});

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdownMenus = document.querySelectorAll('.dropdown-menu-home');
    dropdownMenus.forEach(menu => {
        if (!menu.contains(event.target)) {
            menu.style.display = 'none';
        }
    });
});
let ctx = document.getElementById("chart").getContext("2d");

let myChart;
function fetchDataForDevices() {
    fetch('/api/energy-usage-device-24/')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            createOrUpdateChart(data); // Create or update chart with device data
            // Update the chart when the data type is changed (devices/locations)
            document.getElementById('dataSelector').addEventListener('change', function () {
                const selectedValue = this.value; // Get the selected value (devices/locations)
                if (selectedValue === 'locations') {
                    fetchDataForUserLocation(); // Fetch data for the user's location
                } else {
                    fetchDataForDevices(); // Fetch data for devices
                }
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function fetchDataForUserLocation() {
    fetch('/api/energy-usage-location-24/')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            createOrUpdateChart(data); // Create or update chart with location data
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}
function createOrUpdateChart(data) {
    const labels = data.map(item => item.device_name || item.streetName); // Choose the label based on the data structure
    const values = data.map(item => item.energy_use || item.total_energy_consumption);

    if (!myChart) {
        const ctx = document.getElementById('chart').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'kwh',
                    data: values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Energy Use In The Last 24 Hours For ALL Devices or Locations',
                        font: {
                            size: 30, // Set font size for the chart title
                        },
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            font: {
                                size: 15, // Set font size for y-axis labels
                            },
                        },
                        title: {
                            display: true,
                            text: 'Energy Consumption in kwh',
                            font: {
                                size: 20, // Set font size for y-axis title
                            },
                        }
                    },
                    x: {
                        ticks: {
                            font: {
                                size: 20, // Set font size for x-axis labels
                            },
                        },
                        title: {
                            display: true,
                            text: 'Item Name',
                            font: {
                                size: 25, // Set font size for x-axis title
                            },
                        }
                    }
                }
            }
        });
    } else {
        myChart.data.labels = labels;
        myChart.data.datasets[0].data = values;
        myChart.update();
    }
}
function updateChart(chart, newData) {
    chart.data.labels = newData.map(item => item.device_name);
    chart.data.datasets[0].data = newData.map(item => item.energy_use);
    chart.update();
}
fetchDataForDevices(); // Fetch data for devices or initial load data

