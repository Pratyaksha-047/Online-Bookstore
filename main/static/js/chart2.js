var line = document.getElementById('line');
// line.height = 100
var lineConfig = new Chart(line, {
    type: 'line',
    data: {
        labels: ['January',
            'February',
            'March',
            'April',
            'May',
            'June',],
        datasets: [{
            label: 'No of books sold',
            data: [10, 15, 20, 10, 25, 45],
            fill: false,
            borderColor: '#70442d',
            backgroundColor: '#70442d',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
    }
})