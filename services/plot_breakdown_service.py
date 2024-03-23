import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.ticker as ticker

def plot_breakdown(data=None, parent_frame=None, selected_app_id=None, canvas=None):
    if canvas:
        canvas.get_tk_widget().destroy()  # Clear the existing canvas if any

    fig, ax = plt.subplots()

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
            # Ensure column names are trimmed and consistent
            trimmed_type = energy_type.strip()
            consumption_totals[trimmed_type] = app_data[trimmed_type].sum()

        # Convert to DataFrame for easy sorting and plotting
        consumption_df = pd.DataFrame(list(consumption_totals.items()), columns=['EnergyType', 'TotalConsumption'])
        consumption_df_sorted = consumption_df.sort_values(by='TotalConsumption', ascending=False)

        # Plot
        ax.barh(consumption_df_sorted['EnergyType'], consumption_df_sorted['TotalConsumption'], color='b')
        ax.set_title(f'Energy Consumption Breakdown')
        ax.set_xlabel('Energy Type')
        ax.set_ylabel('Total Energy Consumption (mJ)')

        # Add grid lines behind bars
        ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
        # Move grid lines to background
        ax.set_axisbelow(True)

        # Increase the density of grid lines
        ax.xaxis.set_major_locator(ticker.AutoLocator())  # Automatic placement of major ticks
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))  # Places a specific number of minor ticks between major ticks
    else:
        # Setup for an empty graph
        ax.bar([], [])  # No data to plot

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()

    return canvas
