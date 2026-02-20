 AD-HTC Fuel-Enhanced Gas Cycle Analyzer

Visualization and Analysis platform for integrated AD-HTC Gas/Steam cycles.

Features

- Thermodynamic Engine: Python implementation using `iapws` for steam properties and Brayton cycle models for gas turbines.
- REST API: FastAPI backend providing calculation endpoints for thermal efficiency, power output, and CO2 reduction metrics.
- Interactive Dashboard: Modern UI/UX with Chart.js/Plotly visualizations for:
  - $h-s$ (Enthalpy-Entropy) diagram for the steam cycle.
  - $T-\dot{H}$ (Temperature-Heat Rate) diagram for gas processes.
- Real-time Parametric Analysis: Modify temperatures, pressures, and flow rates to see immediate impacts.

## Installation

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn iapws scipy numpy
   ```

2. Run the API server:
   ```bash
   python main.py
   ```

3. Open `index.html` in your browser to view the dashboard.

## Architecture
- `cycle_engine.py`: Core thermodynamic logic.
- `main.py`: FastAPI server and request routing.
- `index.html`, `styles.css`, `script.js`: Frontend implementation.
