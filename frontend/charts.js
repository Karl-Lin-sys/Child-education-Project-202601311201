/**
 * Chart.js設定 - 教育研究プラットフォーム
 */
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255,255,255,0.1)';

let subjectChart = null;
let ageGroupChart = null;

function renderSubjectChart(data) {
    const ctx = document.getElementById('subjectChart');
    if (!ctx) return;
    if (subjectChart) subjectChart.destroy();

    const colors = ['#4ecdc4', '#f9a61c', '#9b59b6', '#2ecc71', '#e91e63', '#3498db', '#f1c40f', '#e74c3c'];

    subjectChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: '平均スコア',
                data: Object.values(data),
                backgroundColor: colors.slice(0, Object.keys(data).length),
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, max: 100 } }
        }
    });
}

function renderAgeGroupChart(stats) {
    const ctx = document.getElementById('ageGroupChart');
    if (!ctx) return;
    if (ageGroupChart) ageGroupChart.destroy();

    const labels = Object.keys(stats);
    const counts = labels.map(k => stats[k].count);

    ageGroupChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: ['#4ecdc4', '#9b59b6', '#e91e63'],
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: { legend: { position: 'bottom' } }
        }
    });
}
