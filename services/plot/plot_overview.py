import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.ticker as ticker

def abbreviate_label(label, max_length=30):
    if len(label) <= max_length:
        return label
    else:
        # Ensure to keep the portion of the end of the label
        # Calculate how many characters to keep from the end
        end_chars_count = max_length - 3  # Subtracting the length of '...'
        abbreviated = '...' + label[-end_chars_count:]
        return abbreviated

def plot_overview(data, figure):
    # Clear the current axes and create a new one
    figure.clf()
    ax = figure.add_subplot(111)  # Adds a subplot with a single axis

    if data is not None and not data.empty:
        # Aggregate total energy consumption by AppId
        total_consumption_by_app = data.groupby('AppId')['TotalEnergyConsumption'].sum().reset_index()
        
        # Sort the results in descending order and limit to top 20
        total_consumption_by_app_sorted = total_consumption_by_app.sort_values(by='TotalEnergyConsumption', ascending=False).head(20)
        
        # Abbreviate labels
        abbreviated_labels = [abbreviate_label(app_id) for app_id in total_consumption_by_app_sorted['AppId']]
        
        # Plot
        ax.barh(abbreviated_labels, total_consumption_by_app_sorted['TotalEnergyConsumption'], color='b')
        ax.set_title('Top 20 Apps by Total Energy Consumption')
        ax.set_xlabel('AppId')
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

    figure.tight_layout()
