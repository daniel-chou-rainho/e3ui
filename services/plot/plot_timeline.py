import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_timeline(data=None, parent_frame=None, canvas=None, cumulative=False, selected_app_id=None):
    # Initialize plot_title to ensure it's always defined
    plot_title = 'Energy Consumption Over Time'

    # Clear the existing canvas if any
    if canvas:
        try:
            canvas.get_tk_widget().destroy()
        except AttributeError:
            print("Invalid canvas passed to plot_timeline.")

    fig, ax = plt.subplots()
    
    if data is not None and not data.empty and selected_app_id:
        # Filter data for the selected app ID if specified
        if selected_app_id:
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
    plt.xticks(rotation=45)

    # Add grid lines for both x and y axes
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='grey')
    # Setting minor grid lines
    ax.minorticks_on()
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()

    return canvas
