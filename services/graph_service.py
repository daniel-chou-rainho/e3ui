import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_graph(data=None, parent_frame=None, canvas=None):
    if canvas:
        canvas.get_tk_widget().destroy()  # Clear the existing canvas if any

    fig, ax = plt.subplots()
    
    if data is not None and not data.empty:
        # Plot the data if it's provided and not empty
        ax.plot(data['TimeStamp'], data['TotalEnergyConsumption'], marker='o', linestyle='-', color='b')
    else:
        # Setup for an empty graph
        ax.plot([], [])  # No data to plot

    ax.set_title('Total Energy Consumption Over Time for Selected AppId')
    ax.set_xlabel('TimeStamp')
    ax.set_ylabel('Total Energy Consumption')
    plt.xticks(rotation=45)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()

    return canvas
