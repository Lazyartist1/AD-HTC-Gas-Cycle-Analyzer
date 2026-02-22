import urllib.request
import json
import matplotlib.pyplot as plt
import sys

def run_remote_analysis():
    url = "http://localhost:8000/analyze"
    payload = {
        "gt_temp": 1200.0,
        "comp_ratio": 15.0,
        "htc_press": 20.0,
        "biomass_flow": 10.0
    }

    print(f"Calling API at {url}...")
    headers = {'Content-Type': 'application/json'}
    data_json = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(url, data=data_json, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            data = json.loads(res_body)
            
            display_results(data)
            plot_diagrams(data)
            
    except Exception as e:
        print(f"Error connecting to API: {e}")
        print("Ensure the FastAPI server (main.py) is running on port 8000.")
        sys.exit(1)

def display_results(data):
    metrics = data["metrics"]
    print("\n--- Cycle Analysis Results ---")
    print(f"Thermal Efficiency: {metrics['efficiency']:.1f}%")
    print(f"Net Power Output:   {metrics['power']:.1f} MW")
    print(f"CO2 Reduction:      {metrics['co2']:.1f}%")
    print("------------------------------\n")

def plot_diagrams(data):
    charts = data["charts"]
    hs_data = charts["hs"]
    th_data = charts["th"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # h-s Chart
    ax1.plot(hs_data["s"], hs_data["h"], 'o-', color='#2563eb', linewidth=2, markersize=6)
    ax1.set_title('h-s Diagram (Steam Cycle)')
    ax1.set_xlabel('Entropy (s) [kJ/kg·K]')
    ax1.set_ylabel('Enthalpy (h) [kJ/kg]')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # T-H Chart
    ax2.plot(th_data["gas_H"], th_data["gas_T"], '-', color='#ef4444', linewidth=3, label='GT Exhaust')
    ax2.plot(th_data["steam_H"], th_data["steam_T"], '-', color='#3b82f6', linewidth=3, label='Water/Steam Path')
    ax2.set_title('T-Ḣ Diagram Heat Integration')
    ax2.set_xlabel('Heat Transfer [kW]')
    ax2.set_ylabel('Temperature (T) [°C]')
    ax2.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2)
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    print("Displaying diagrams. Close the window to exit.")
    plt.show()

if __name__ == "__main__":
    run_remote_analysis()
