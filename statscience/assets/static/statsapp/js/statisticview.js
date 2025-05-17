let statGraph = null; // higher-scope variable to retain a chart instance

async function create_graph(stat_name) {
    const ctx = document.getElementById('myChart').getContext('2d');

    // Destroy the existing chart if it exists
    if (statGraph) {
        statGraph.destroy();
    }

    let stat_data = await get_data(stat_name);
    let labels = stat_data.data.labels;
    let label_data = stat_data.data.values;
    let stat_type = stat_data.type;

    if (stat_type === 'daily') {
        // Use the data as-is
    }
    else if (stat_type === 'weekly') {
        const grouped_data = [];
        for (let i = 0; i < label_data.length; i += 7) {
            const week_sum = label_data.slice(i, i + 7).reduce((a, b) => a + b, 0);
            grouped_data.push(week_sum);
        }

        // Pad to ensure at least 5 weeks of data
        const min_weeks = 5;
        const missing_weeks = Math.max(0, min_weeks - grouped_data.length);
        label_data = Array(missing_weeks).fill(0).concat(grouped_data);

        // Generate labels like ["4 Weeks Ago", ..., "This Week"]
        labels = label_data.map((_, index, arr) => {
            const week_diff = arr.length - index - 1;
            return week_diff === 0 ? "This Week" :
                week_diff === 1 ? "1 Week Ago" :
                    `${week_diff} Weeks Ago`;
        });
    }
    else if (stat_type === 'accumulative') {
        for (let i = 1; i < label_data.length; i++) {
            label_data[i] += label_data[i - 1];
        }
    }

    // Create a new chart
    // noinspection JSUnresolvedReference
    statGraph = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${stat_name}`,
                data: label_data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
