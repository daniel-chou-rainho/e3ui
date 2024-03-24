import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import datetime

def get_co2_intensity() -> float:
    co2_intensity_types = {
        "Biomass": 52,
        "Solar": 43,
        "Fossil oil": 840,
        "Fossil brown coal / lignite": 1001,
        "Fossil hard coal": 1001,
        "Fossil gas": 486,
        "Geothermal": 37,
        "Hydro water reservoir": 21,
        "Hydro Run-of-River": 21,
        "Wind offshore": 13,
        "Wind onshore": 13,
        "Nuclear": 13,
    }


    # Current location
    requests_loc= requests.get(f'https://ipinfo.io/json')
    requests_loc = requests_loc.json()
    country = requests_loc["country"].lower()
    #Get current date and time like 2023-01-01T00%3A00%2B01%3A00
    now = datetime.datetime.now()

    start = now - datetime.timedelta(hours=3)
    start = start.strftime('%Y-%m-%dT%H%%3A%M%%2B01%%3A00')
    end = now.strftime('%Y-%m-%dT%H%%3A%M%%2B01%%3A00')

    request_energy = requests.get(f'https://api.energy-charts.info/public_power?country={country}&start={start}&end={end}', headers={'accept': 'application/json'})
    response = request_energy.json()

    #Get current c02 intensity
    production = response['production_types']

    total_production = 0
    co2_intensity = 0
    for type in production:
        if type['name'] in co2_intensity_types:
            co2_intensity += type['data'][-1] * co2_intensity_types[type['name']]
            total_production += type['data'][-1]
    co2_intensity = co2_intensity / total_production
    return co2_intensity

def plot_carbon(data=None, figure=None, selected_app_id=None):
    # Clear the figure for the new plot
    figure.clf()  # Clears the figure to prepare for a new plot
    ax = figure.add_subplot(111)  # Adds a new subplot to the cleared figure

    # Initialize plot_title to ensure it's always defined
    plot_title = 'Energy Consumption Over Time'

    co2_intensity = get_co2_intensity()
    
    if data is not None and not data.empty and selected_app_id:
        # Filter data for the selected app ID if specified
        data = data[data['AppId'] == selected_app_id]


        data = data.sort_values('TimeStamp')
        data['CummulativeCO2'] = data['TotalEnergyConsumption'].cumsum()/1000/3600*co2_intensity
        y_data = data['CummulativeCO2']
        plot_title = 'Cumulative CO2 emision Over Time'


        ax.plot(data['TimeStamp'], y_data, marker='o', linestyle='-', color='b')
    else:
        # Setup for an empty graph
        ax.plot([], [])  # No data to plot

    ax.set_title(f'{plot_title} for Selected AppId' if selected_app_id else plot_title)
    ax.set_xlabel('TimeStamp')
    ax.set_ylabel('CO2 emisions (mg)')
    ax.tick_params(axis='x', rotation=45)

    # Add grid lines for both x and y axes
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='grey')
    # Setting minor grid lines
    ax.minorticks_on()
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    
    figure.tight_layout()
