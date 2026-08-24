/*
 * K.A.R.M.A Cloud SIEM Analytics & Real-Time Multi-Plot Chart Handler
 * Real-Time Per-Second Line Plot with Auto-Compression & Interactive Zooming
 */

let timeSeriesChartInstance = null;
let productsBarChartInstance = null;
let logTypesDoughnutChartInstance = null;
let eventActionsHorizontalChartInstance = null;

// Zoom state for Time Series Line Plot
let linePlotZoomLimit = 15; // default visible ticks
let cachedSecondBuckets = {};

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

// 1. Real-Time Per-Second Event Volume Trend Line Chart (with auto-skip & label clamping)
function initTimeSeriesChart() {
    const ctx = document.getElementById('timeSeriesChart');
    if (!ctx) return;
    const c = getChartColors();

    timeSeriesChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Attack Event Count',
                data: [],
                borderColor: c.green,
                backgroundColor: 'rgba(16, 185, 129, 0.12)',
                borderWidth: 2,
                tension: 0.25,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: c.green
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        title: function(items) {
                            return `Timestamp: ${items[0].label}`;
                        },
                        label: function(item) {
                            return ` Attacks: ${item.raw} events`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: c.textColor,
                        font: { size: 9 },
                        maxRotation: 0,
                        minRotation: 0,
                        autoSkip: true,
                        autoSkipPadding: 14
                    },
                    grid: { color: c.gridColor }
                },
                y: {
                    ticks: { color: c.textColor, font: { size: 10 }, stepSize: 1 },
                    grid: { color: c.gridColor },
                    beginAtZero: true
                }
            }
        }
    });
}

// 2. Products / Decoy Services Bar Chart
function initProductsBarChart() {
    const ctx = document.getElementById('productsBarChart');
    if (!ctx) return;
    const c = getChartColors();

    productsBarChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Event Hits',
                data: [],
                backgroundColor: [c.blue, c.purple, c.cyan, c.amber, c.red],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: c.textColor, font: { size: 9 }, maxRotation: 0, autoSkip: true }, grid: { display: false } },
                y: { ticks: { color: c.textColor, font: { size: 10 }, stepSize: 1 }, grid: { color: c.gridColor }, beginAtZero: true }
            }
        }
    });
}

// 3. Log Types Volume Doughnut Chart
function initLogTypesDoughnutChart() {
    const ctx = document.getElementById('logTypesDoughnutChart');
    if (!ctx) return;
    const c = getChartColors();

    logTypesDoughnutChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Critical (Honeytoken)', 'High (SQLi/XSS)', 'Medium (BruteForce)', 'Info (Scan Probe)'],
            datasets: [{
                data: [0, 0, 0, 0],
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

// 4. Event Actions Horizontal Bar Chart
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
                data: [0, 0, 0, 0],
                backgroundColor: [c.red, c.amber, c.green, c.purple],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: c.textColor, font: { size: 10 }, stepSize: 1 }, grid: { color: c.gridColor }, beginAtZero: true },
                y: { ticks: { color: c.textColor, font: { size: 10 } }, grid: { display: false } }
            }
        }
    });
}

// Zoom Controls for Line Plot (Zoom In, Zoom Out, Fit All)
function zoomTimeSeriesChart(action) {
    const timeKeys = Object.keys(cachedSecondBuckets).sort();
    if (timeKeys.length === 0) return;

    if (action === 'in') {
        linePlotZoomLimit = Math.max(5, Math.floor(linePlotZoomLimit / 1.6));
    } else if (action === 'out') {
        linePlotZoomLimit = Math.min(timeKeys.length, Math.ceil(linePlotZoomLimit * 1.6));
    } else if (action === 'reset') {
        linePlotZoomLimit = timeKeys.length;
    }

    renderTimeSeriesPlot();
}

function renderTimeSeriesPlot() {
    if (!timeSeriesChartInstance) return;

    const timeKeys = Object.keys(cachedSecondBuckets).sort();
    if (timeKeys.length === 0) {
        timeSeriesChartInstance.data.labels = [];
        timeSeriesChartInstance.data.datasets[0].data = [];
    } else {
        const sliceCount = Math.min(linePlotZoomLimit, timeKeys.length);
        const visibleKeys = timeKeys.slice(-sliceCount);

        timeSeriesChartInstance.data.labels = visibleKeys;
        timeSeriesChartInstance.data.datasets[0].data = visibleKeys.map(k => cachedSecondBuckets[k]);
    }
    timeSeriesChartInstance.update();
}

// Update Charts Real-Time from Telemetry Stream
function updateSiemCharts(logs) {
    if (!logs || logs.length === 0) {
        resetCharts();
        return;
    }

    // Update Severity & Service Breakdown
    let counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 };
    let services = {};
    let actions = { Quarantined: 0, Alerted: 0, Monitored: 0, Blocked: 0 };
    cachedSecondBuckets = {};

    logs.forEach(l => {
        const sev = l.severity || 'LOW';
        if (counts[sev] !== undefined) counts[sev]++;

        const s = l.decoy_service || 'UNKNOWN';
        services[s] = (services[s] || 0) + 1;

        if (l.quarantined) {
            actions.Quarantined++;
            actions.Blocked++;
        } else if (sev === 'CRITICAL' || sev === 'HIGH') {
            actions.Alerted++;
        } else {
            actions.Monitored++;
        }

        // Group by Real Time Second (HH:MM:SS)
        if (l.timestamp) {
            let timeStr = "";
            if (l.timestamp.includes("T")) {
                timeStr = l.timestamp.split("T")[1].substring(0, 8);
            } else if (l.timestamp.includes(" ")) {
                timeStr = l.timestamp.split(" ")[1].substring(0, 8);
            } else {
                timeStr = l.timestamp.substring(0, 8);
            }
            if (timeStr) {
                cachedSecondBuckets[timeStr] = (cachedSecondBuckets[timeStr] || 0) + 1;
            }
        }
    });

    // 1. Update Doughnut Chart
    if (logTypesDoughnutChartInstance) {
        logTypesDoughnutChartInstance.data.datasets[0].data = [
            counts.CRITICAL,
            counts.HIGH,
            counts.MEDIUM,
            counts.LOW
        ];
        logTypesDoughnutChartInstance.update();
    }

    // 2. Update Products / Services Bar Chart
    if (productsBarChartInstance) {
        productsBarChartInstance.data.labels = Object.keys(services);
        productsBarChartInstance.data.datasets[0].data = Object.values(services);
        productsBarChartInstance.update();
    }

    // 3. Update Event Actions Horizontal Bar Chart
    if (eventActionsHorizontalChartInstance) {
        eventActionsHorizontalChartInstance.data.datasets[0].data = [
            actions.Quarantined,
            actions.Alerted,
            actions.Monitored,
            actions.Blocked
        ];
        eventActionsHorizontalChartInstance.update();
    }

    // 4. Update Line Plot with Zoom Clamping
    renderTimeSeriesPlot();
}

// Reset All Charts Back to Zero / Empty State
function resetCharts() {
    cachedSecondBuckets = {};
    linePlotZoomLimit = 15;

    if (timeSeriesChartInstance) {
        timeSeriesChartInstance.data.labels = [];
        timeSeriesChartInstance.data.datasets[0].data = [];
        timeSeriesChartInstance.update();
    }
    if (productsBarChartInstance) {
        productsBarChartInstance.data.labels = [];
        productsBarChartInstance.data.datasets[0].data = [];
        productsBarChartInstance.update();
    }
    if (logTypesDoughnutChartInstance) {
        logTypesDoughnutChartInstance.data.datasets[0].data = [0, 0, 0, 0];
        logTypesDoughnutChartInstance.update();
    }
    if (eventActionsHorizontalChartInstance) {
        eventActionsHorizontalChartInstance.data.datasets[0].data = [0, 0, 0, 0];
        eventActionsHorizontalChartInstance.update();
    }
}
