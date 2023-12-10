document.addEventListener('DOMContentLoaded', function() {
    const dataSelector = document.getElementById('dataSelector');
    const mothYearSelector = document.getElementById('month-year-selector-id');

    // Function to trigger API call and update chart
    function triggerAPICallAndUpdateChart() {
        const selectedLocationId = dataSelector.value;
        const selectedMonth = `${mothYearSelector.value}-01`;
        console.log(selectedMonth);
        // Call the function to update chart with new data
       updateChart(selectedLocationId, selectedMonth);
    }
    // Event listeners for the selection change in dataSelector and the date input change
    dataSelector.addEventListener('change', triggerAPICallAndUpdateChart);
    mothYearSelector.addEventListener('change', triggerAPICallAndUpdateChart);

    // Call the API function to initialize the chart on initial page load
    triggerAPICallAndUpdateChart();
});

function updateChart(locationId, date) {
    fetchData(locationId, date);
}

function fetchData(locationId, date) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const apiUrl = '/api/location-montly-history-comparison/';
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
        createComparisonChart(data[0]);
    })
    .catch(error => {
        console.log(error);
    });
}

function createComparisonChart(data) {
    console.log(data);
    const locationId = data.location_id;
    const energyConsumption = data.energy_consumption;
    const similarAvg = data.similar_avg;
    const bigNumberDiv = document.getElementById('consumption-percentage');
    if (bigNumberDiv) {
        bigNumberDiv.textContent = data.energy_as_percentage.toFixed(2) + '%'; // Displaying the percentage with two decimal places
    }
    console.log(locationId, energyConsumption, similarAvg);
    const ctx = document.getElementById('comparison-chart').getContext('2d');
    if (window.comparisonChart) {
        window.comparisonChart.destroy();
    }
    window.comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [``],
            datasets: [
                {
                    label: 'Energy Consumption',
                    data: [energyConsumption],
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderWidth: 1
                },
                {
                    label: 'Similar Locations\' Average',
                    data: [similarAvg],
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderWidth: 1
                }
            ]
        },
        options: {
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
                        text: 'Location Selected and Similar Locations',
                        font: {
                            size: 20, // Set font size for x-axis title
                        },
                    }
                }
            }
        }
    });
}