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

        ax.plot(data['TimeStamp'], y_data, marker='o', linestyle='-', color='b')
    else:
        # Setup for an empty graph
        ax.plot([], [])  # No data to plot

    ax.set_title(f'{plot_title} for Selected AppId' if selected_app_id else plot_title)
    ax.set_xlabel('TimeStamp')
    ax.set_ylabel('Energy Consumption (mJ)')
    ax.tick_params(axis='x', rotation=45)

    # Add grid lines for both x and y axes
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='grey')
    # Setting minor grid lines
    ax.minorticks_on()
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    
    figure.tight_layout()
