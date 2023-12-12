// Access the global variables defined in graph.html
var ctx = document.getElementById('lineCharts').getContext('2d');
var linCharts = new Chart(ctx, {
    type: 'line',
    data: {
        labels: JSON.parse(labels),
        datasets: [{
            label: 'Abscence',
            data: JSON.parse(values),
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: 'rgba(255, 0, 0, 1)',
            borderWidth: 1
        }]
    },
});
