import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.ticker as ticker

def plot_breakdown(data=None, figure=None, selected_app_id=None):
    # Clear the figure for the new plot
    figure.clf()
    ax = figure.subplots()

    if data is not None and not data.empty and selected_app_id:
        # Filter data for the selected App ID
        app_data = data[data['AppId'] == selected_app_id]

        # Aggregate total energy consumption by type
        energy_types = [
            "CPUEnergyConsumption", "SocEnergyConsumption", "DisplayEnergyConsumption",
            "DiskEnergyConsumption", "NetworkEnergyConsumption", "MBBEnergyConsumption",
            "OtherEnergyConsumption", "EmiEnergyConsumption", "CPUEnergyConsumptionWorkOnBehalf",
            "CPUEnergyConsumptionAttributed"
        ]
        consumption_totals = {}
        for energy_type in energy_types:
            trimmed_type = energy_type.strip()
            consumption_totals[trimmed_type] = app_data[trimmed_type].sum()

        # Convert to DataFrame for easy sorting and plotting
        consumption_df = pd.DataFrame(list(consumption_totals.items()), columns=['EnergyType', 'TotalConsumption'])
        consumption_df_sorted = consumption_df.sort_values(by='TotalConsumption', ascending=False)

        # Plot with eco-friendly aesthetics
        ax.barh(consumption_df_sorted['EnergyType'], consumption_df_sorted['TotalConsumption']/3600, color='#4CAF50')  # A green color for bars
        ax.set_title(f'Energy Consumption Breakdown for {selected_app_id}', fontname='Arial')  # Darker green color for the title
        ax.set_ylabel('Energy Type', fontname='Arial')
        ax.set_xlabel('Total Energy Consumption (Wh)', fontname='Arial')

        # Add grid lines behind bars, using a lighter shade of green
        ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5, color='#A5D6A7')  # Light green for grid lines
        # Move grid lines to background
        ax.set_axisbelow(True)

        # Increase the density of grid lines
        ax.xaxis.set_major_locator(ticker.AutoLocator())  # Automatic placement of major ticks
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))  # Places a specific number of minor ticks between major ticks
        
        # Set background color to a lighter shade of green for an eco-friendly vibe
        ax.set_facecolor('#E8F5E9')  # Light green background
        figure.patch.set_facecolor('#E8F5E9')  # Matching figure background

        # Make the plot layout tight
        figure.tight_layout()
