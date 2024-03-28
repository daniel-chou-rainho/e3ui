import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.ticker as ticker

def abbreviate_label(label, max_length=30):
    if len(label) <= max_length:
        return label
    else:
        # Ensure to keep the portion of the end of the label
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
        
        # Plot with eco-friendly aesthetics
        ax.barh(abbreviated_labels, total_consumption_by_app_sorted['TotalEnergyConsumption']/3600, color='#4CAF50')  # A green color
        ax.set_title('Top 20 Apps by Total Energy Consumption', fontname='Arial')  # Darker green color for the title
        ax.set_ylabel('AppId', fontname='Arial')
        ax.set_xlabel('Total Energy Consumption (Wh)', fontname='Arial')

        # Add grid lines behind bars
        ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5, color='#A5D6A7')  # Light green for grid lines
        # Move grid lines to background
        ax.set_axisbelow(True)

        # Increase the density of grid lines
        ax.xaxis.set_major_locator(ticker.AutoLocator())  # Automatic placement of major ticks
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))  # Places a specific number of minor ticks between major ticks
        
        # Set background color to a lighter shade of green for an eco-friendly vibe
        ax.set_facecolor('#E8F5E9')  # Light green background
        figure.patch.set_facecolor('#E8F5E9')  # Matching figure background
    else:
        # Setup for an empty graph
        ax.bar([], [])  # No data to plot

    figure.tight_layout()
