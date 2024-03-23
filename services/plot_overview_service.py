import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def abbreviate_label(label, max_length=30):
    if len(label) <= max_length:
        return label
    else:
        # Ensure to keep the portion of the end of the label
        # Calculate how many characters to keep from the end
        end_chars_count = max_length - 3  # Subtracting the length of '...'
        abbreviated = '...' + label[-end_chars_count:]
        return abbreviated

def plot_overview(data=None, parent_frame=None, canvas=None):
    if canvas:
        canvas.get_tk_widget().destroy()  # Clear the existing canvas if any

    fig, ax = plt.subplots()

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
    else:
        # Setup for an empty graph
        ax.bar([], [])  # No data to plot

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()

    return canvas
