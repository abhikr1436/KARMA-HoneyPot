/*
 * Enterprise SIEM Analytics & Multi-Plot Chart Handler
 * Handles Line, Bar, Doughnut, and Horizontal Bar Charts (Logz.io & Logsign Style)
 */

let timeSeriesChartInstance = null;
let productsBarChartInstance = null;
let logTypesDoughnutChartInstance = null;
let eventActionsHorizontalChartInstance = null;

function getChartColors() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    return {
        textColor: isDark ? '#94a3b8' : '#64748b',
        gridColor: isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.05)',
        blue: isDark ? '#3b82f6' : '#0070f3',
        green: '#10b981',
        purple: isDark ? '#a855f7' : '#7c3aed',
        amber: '#f59e0b',
        red: '#ef4444',
        cyan: '#00f2fe'
    };
}

function initSiemCharts() {
    initTimeSeriesChart();
    initProductsBarChart();
    initLogTypesDoughnutChart();
    initEventActionsHorizontalChart();
}

function generateISTTimeBuckets() {
    const now = new Date();
    const labels = [];
    const bucketStartTimes = [];
    
    // Generate 8 time slots for the last 24 hours (3-hour steps) ending at current IST time
    for (let i = 7; i >= 0; i--) {
        const d = new Date(now.getTime() - i * 3 * 3600 * 1000);
        const hh = String(d.getHours()).padStart(2, '0');
        const mm = String(d.getMinutes()).padStart(2, '0');
        
        if (i === 0) {
            labels.push(`${hh}:${mm} IST`);
        } else {
            labels.push(`${hh}:00`);
        }
        bucketStartTimes.push(d.getTime());
    }
    
    return { labels, bucketStartTimes };
}

// 1. Time Series Line Chart (Logz.io Image 1)
function initTimeSeriesChart() {
    const ctx = document.getElementById('timeSeriesChart');
    if (!ctx) return;
    const c = getChartColors();
    const { labels } = generateISTTimeBuckets();

    timeSeriesChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: [0, 0, 0, 0, 0, 0, 0, 0],
                borderColor: c.green,
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: c.green
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    ticks: { color: c.textColor, font: { size: 10 } },
                    grid: { color: c.gridColor }
                },
                y: {
                    ticks: { color: c.textColor, font: { size: 10 } },
                    grid: { color: c.gridColor },
                    beginAtZero: true
                }
            }
        }
    });
}

// 2. Products / Decoy Services Bar Chart (Logsign Image 2)
function initProductsBarChart() {
    const ctx = document.getElementById('productsBarChart');
    if (!ctx) return;
    const c = getChartColors();

    productsBarChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['SSH Decoy', 'Web Admin', 'FTP Probe', 'Telnet Probe', 'RDP Probe'],
            datasets: [{
                label: 'Event Hits',
                data: [4, 6, 2, 1, 3],
                backgroundColor: [c.blue, c.purple, c.cyan, c.amber, c.red],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: c.textColor, font: { size: 9 } }, grid: { display: false } },
                y: { ticks: { color: c.textColor, font: { size: 10 } }, grid: { color: c.gridColor }, beginAtZero: true }
            }
        }
    });
}

// 3. Log Types Volume Doughnut Chart (Logsign Image 2)
function initLogTypesDoughnutChart() {
    const ctx = document.getElementById('logTypesDoughnutChart');
    if (!ctx) return;
    const c = getChartColors();

    logTypesDoughnutChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Critical (Honeytoken)', 'High (SQLi/XSS)', 'Medium (BruteForce)', 'Info (Scan Probe)'],
            datasets: [{
                data: [1, 3, 5, 7],
                backgroundColor: [c.red, c.amber, c.blue, c.green],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: c.textColor, font: { size: 10 }, usePointStyle: true, boxWidth: 6 }
                }
            }
        }
    });
}

// 4. Event Actions Horizontal Bar Chart (Logsign Image 2)
function initEventActionsHorizontalChart() {
    const ctx = document.getElementById('eventActionsHorizontalChart');
    if (!ctx) return;
    const c = getChartColors();

    eventActionsHorizontalChartInstance = new Chart(ctx, {
        type: 'bar',
        indexAxis: 'y',
        data: {
            labels: ['Quarantined', 'Alerted', 'Monitored', 'Blocked'],
            datasets: [{
                label: 'Count',
                data: [3, 8, 12, 5],
                backgroundColor: [c.red, c.amber, c.green, c.purple],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: c.textColor, font: { size: 10 } }, grid: { color: c.gridColor }, beginAtZero: true },
                y: { ticks: { color: c.textColor, font: { size: 10 } }, grid: { display: false } }
            }
        }
    });
}

function updateSiemCharts(logs) {
    if (!logs) return;

    // Update Log Types Doughnut
    let counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 };
    let services = {};

    logs.forEach(l => {
        const sev = l.severity || 'LOW';
        if (counts[sev] !== undefined) counts[sev]++;
        const s = l.decoy_service || 'UNKNOWN';
        services[s] = (services[s] || 0) + 1;
    });

    if (logTypesDoughnutChartInstance) {
        logTypesDoughnutChartInstance.data.datasets[0].data = [
            counts.CRITICAL,
            counts.HIGH,
            counts.MEDIUM,
            counts.LOW
        ];
        logTypesDoughnutChartInstance.update();
    }

    if (productsBarChartInstance && Object.keys(services).length > 0) {
        productsBarChartInstance.data.labels = Object.keys(services);
        productsBarChartInstance.data.datasets[0].data = Object.values(services);
        productsBarChartInstance.update();
    }

    if (timeSeriesChartInstance) {
        const { labels } = generateISTTimeBuckets();
        const counts = new Array(8).fill(0);
        const nowMs = new Date().getTime();

        if (logs && logs.length > 0) {
            logs.forEach(l => {
                if (!l.timestamp) return;
                const logTime = new Date(l.timestamp.replace(" ", "T")).getTime();
                if (isNaN(logTime)) return;

                const ageMs = nowMs - logTime;
                if (ageMs >= 0 && ageMs <= 24 * 3600 * 1000) {
                    const hoursAgo = ageMs / (3600 * 1000);
                    let idx = 7 - Math.floor(hoursAgo / 3);
                    if (idx < 0) idx = 0;
                    if (idx > 7) idx = 7;
                    counts[idx]++;
                }
            });
        }

        timeSeriesChartInstance.data.labels = labels;
        timeSeriesChartInstance.data.datasets[0].data = counts;
        timeSeriesChartInstance.update();
    }
}
