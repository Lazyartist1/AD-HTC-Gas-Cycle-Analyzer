document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const etaGasVal = document.getElementById('eta-gas-val');
    const etaSteamVal = document.getElementById('eta-steam-val');
    const powerVal = document.getElementById('power-val');
    const co2Val = document.getElementById('co2-val');

    analyzeBtn.addEventListener('click', async () => {
        const payload = {
            gt_temp: parseFloat(document.getElementById('gt-temp').value),
            comp_ratio: parseFloat(document.getElementById('comp-ratio').value),
            htc_press: parseFloat(document.getElementById('htc-press').value),
            biomass_flow: parseFloat(document.getElementById('biomass-flow').value)
        };

        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'ANALYZING...';

        try {
            const response = await fetch('http://localhost:8000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.statusText}`);
            }

            const data = await response.json();
            updateDashboard(data);

        } catch (error) {
            console.error('Analysis failed:', error);
            alert('Failed to connect to the server. Ensure main.py is running.');
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'ANALYZE CYCLE';
        }
    });

    function updateDashboard(data) {
        // Update Metrics
        etaGasVal.textContent = `${(data.metrics.efficiency_gas * 100).toFixed(1)}%`;
        etaSteamVal.textContent = `${(data.metrics.efficiency_steam * 100).toFixed(1)}%`;
        powerVal.textContent = `${data.metrics.power.toFixed(1)} MW`;
        co2Val.textContent = `${data.metrics.co2.toFixed(1)}%`;

        // Plot h-s Chart
        const hsData = [{
            x: data.charts.hs.s,
            y: data.charts.hs.h,
            mode: 'lines+markers',
            name: 'Steam Cycle',
            line: { color: '#2563eb', width: 2 },
            marker: { size: 6 }
        }];
        const hsLayout = {
            title: { text: 'h-s Diagram (Steam Cycle)', font: { color: '#f1f5f9' } },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            xaxis: {
                title: { text: 'Entropy (s) [kJ/kg·K]', font: { color: '#94a3b8' } },
                tickfont: { color: '#94a3b8' },
                gridcolor: '#334155'
            },
            yaxis: {
                title: { text: 'Enthalpy (h) [kJ/kg]', font: { color: '#94a3b8' } },
                tickfont: { color: '#94a3b8' },
                gridcolor: '#334155'
            },
            margin: { t: 60, r: 20, l: 60, b: 40 }
        };
        Plotly.newPlot('hs-chart', hsData, hsLayout);

        // Plot T-H Chart
        const thData = [
            {
                x: data.charts.th.gas_H,
                y: data.charts.th.gas_T,
                mode: 'lines',
                name: 'GT Exhaust',
                line: { color: '#ef4444', width: 3 }
            },
            {
                x: data.charts.th.steam_H,
                y: data.charts.th.steam_T,
                mode: 'lines',
                name: 'Water/Steam Path',
                line: { color: '#3b82f6', width: 3 }
            }
        ];
        const thLayout = {
            title: { text: 'T-Ḣ Diagram Heat Integration', font: { color: '#f1f5f9' } },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            xaxis: {
                title: { text: 'Heat Transfer [kW]', font: { color: '#94a3b8' } },
                tickfont: { color: '#94a3b8' },
                gridcolor: '#334155'
            },
            yaxis: {
                title: { text: 'Temperature (T) [°C]', font: { color: '#94a3b8' } },
                tickfont: { color: '#94a3b8' },
                gridcolor: '#334155'
            },
            legend: {
                orientation: 'h',
                y: -0.2,
                font: { color: '#f1f5f9' }
            },
            margin: { t: 60, r: 20, l: 60, b: 40 }
        };
        Plotly.newPlot('th-chart', thData, thLayout);
    }
});
