import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_timeline(data=None, figure=None, cumulative=False, selected_app_id=None):
    # Clear the figure for the new plot
    figure.clf()  # Clears the figure to prepare for a new plot
    ax = figure.add_subplot(111)  # Adds a new subplot to the cleared figure

    # Initialize plot_title to ensure it's always defined
    plot_title = 'Energy Consumption Over Time'
    
    if data is not None and not data.empty and selected_app_id:
        # Filter data for the selected app ID if specified
        data = data[data['AppId'] == selected_app_id]

        if cumulative:
            data = data.sort_values('TimeStamp')
            data['CumulativeEnergy'] = data['TotalEnergyConsumption'].cumsum()
            y_data = data['CumulativeEnergy']
            plot_title = 'Cumulative Energy Consumption Over Time'
        else:
            y_data = data['TotalEnergyConsumption']
            plot_title = 'Total Energy Consumption Over Time'

        ax.plot(data['TimeStamp'], y_data, marker='o', linestyle='-', color='#4CAF50')  # Use a green color for the line
    else:
        # Setup for an empty graph
        ax.plot([], [])  # No data to plot

    ax.set_title(f'{plot_title} for Selected AppId' if selected_app_id else plot_title, fontname='Arial')
    ax.set_xlabel('TimeStamp', fontname='Arial')
    ax.set_ylabel('Energy Consumption (mJ)', fontname='Arial')
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y')

    # Add grid lines for both x and y axes, using a lighter shade of green for eco-friendly vibes
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#A5D6A7')
    ax.minorticks_on()
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='#C8E6C9')
    
    # Set background color to a lighter shade of green for an eco-friendly vibe
    ax.set_facecolor('#E8F5E9')  # Light green background
    figure.patch.set_facecolor('#E8F5E9')  # Matching figure background

    figure.tight_layout()
