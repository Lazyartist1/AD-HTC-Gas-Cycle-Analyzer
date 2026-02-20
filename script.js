document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');

    analyzeBtn.addEventListener('click', () => {
        runRemoteAnalysis();
    });

    // Initial run
    runRemoteAnalysis();
});

async function runRemoteAnalysis() {
    const payload = {
        gt_temp: parseFloat(document.getElementById('gt-temp').value),
        comp_ratio: parseFloat(document.getElementById('comp-ratio').value),
        htc_press: parseFloat(document.getElementById('htc-press').value),
        biomass_flow: parseFloat(document.getElementById('biomass-flow').value)
    };

    try {
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        updateUI(data);

    } catch (error) {
        console.error('API Error:', error);
        alert("API not reachable. Ensure the Python server (main.py) is running on port 8000.");
    }
}

function updateUI(data) {
    document.getElementById('eta-val').innerText = (data.metrics.efficiency * 1).toFixed(1) + '%';
    document.getElementById('power-val').innerText = data.metrics.power.toFixed(1) + ' MW';
    document.getElementById('co2-val').innerText = data.metrics.co2.toFixed(1) + '%';

    drawHSChart(data.charts.hs);
    drawTHChart(data.charts.th);
}

function drawHSChart(hsData) {
    const trace = {
        x: hsData.s,
        y: hsData.h,
        mode: 'lines+markers',
        name: 'HTC Steam Cycle',
        line: { color: '#2563eb', width: 3, shape: 'spline' },
        marker: { size: 6 }
    };

    const layout = {
        title: 'h-s Diagram (Steam Cycle)',
        xaxis: { title: 'Entropy (s) [kJ/kg·K]', gridcolor: '#f1f5f9' },
        yaxis: { title: 'Enthalpy (h) [kJ/kg]', gridcolor: '#f1f5f9' },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: { t: 40, b: 40, l: 60, r: 20 }
    };

    Plotly.newPlot('hs-chart', [trace], layout);
}

function drawTHChart(thData) {
    const traceGas = {
        x: thData.gas_H,
        y: thData.gas_T,
        mode: 'lines',
        name: 'GT Exhaust',
        line: { color: '#ef4444', width: 3 }
    };

    const traceSteam = {
        x: thData.steam_H,
        y: thData.steam_T,
        mode: 'lines',
        name: 'Water/Steam Path',
        line: { color: '#3b82f6', width: 3 }
    };

    const layout = {
        title: 'T-Ḣ Diagram Heat Integration',
        xaxis: { title: 'Heat Transfer [kW]', gridcolor: '#f1f5f9' },
        yaxis: { title: 'Temperature (T) [°C]', gridcolor: '#f1f5f9' },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: { t: 40, b: 40, l: 60, r: 20 },
        legend: { orientation: 'h', y: -0.2 }
    };

    Plotly.newPlot('th-chart', [traceGas, traceSteam], layout);
}
