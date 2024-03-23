import tkinter as tk
from tkinter import ttk
from services.data.select_csv_file import select_csv_file
from services.data.get_app_ids import get_app_ids
from services.data.load_data import load_data
from services.plot.plot_overview import plot_overview
from services.plot.plot_breakdown import plot_breakdown
from services.plot.plot_timeline import plot_timeline

class GraphWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.data = None
        self.canvas = None
        self.create_widgets()
        self.canvas = plot_timeline(parent_frame=self.graph_frame)

    def create_widgets(self):
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.LEFT, fill='y', padx=10, pady=10)

        # Frame to hold Start and Stop buttons next to each other
        button_frame = tk.Frame(control_frame)
        button_frame.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        # Start Data Collection button
        self.start_button = ttk.Button(
            button_frame,
            text="Start Data Collection",
            command=self.start_data_collection
        )
        self.start_button.pack(side=tk.LEFT, fill='x', expand=True, padx=2.5, pady=5)

        # Stop Data Collection button
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop Data Collection",
            command=self.stop_data_collection
        )
        self.stop_button.pack(side=tk.LEFT, fill='x', expand=True, padx=2.5, pady=5)

        # File selection button
        self.select_file_button = ttk.Button(
            control_frame,
            text="Select CSV File",
            command=self.select_file
        )
        self.select_file_button.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        # File name label
        self.filename_label = tk.Label(
            control_frame,
            text="No file selected",
            foreground="gray"
        )
        self.filename_label.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        # Graph type dropdown
        self.graph_type_dropdown = ttk.Combobox(
            control_frame,
            state="readonly",
            values=[
                "Total Power Consumption by App",
                "Power Consumption Breakdown for a Selected App",
                "Cumulative Power Consumption Over Time",
                "Power Consumption Over Time"
            ]
        )
        self.graph_type_dropdown.pack(side=tk.TOP, fill='x', padx=5, pady=5)
        self.graph_type_dropdown.bind("<<ComboboxSelected>>", self.update_graph_type)

        # AppId dropdown
        self.app_id_dropdown = ttk.Combobox(control_frame, state="readonly", values=[])
        self.app_id_dropdown.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        # The graph_frame will now take the rest of the space to the right
        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

    def start_data_collection(self):
        pass

    def stop_data_collection(self):
        pass

    def select_file(self):
        file_path = select_csv_file(self)
        if file_path:
            self.data = load_data(file_path)
            app_ids = get_app_ids(self.data)
            self.app_id_dropdown['values'] = app_ids
            self.app_id_dropdown.bind("<<ComboboxSelected>>", self.update_graph_type)
            filename = file_path.split('/')[-1]
            self.filename_label.config(text=filename, foreground="black")
    
    def update_graph_type(self, event):
        selected_graph_type = self.graph_type_dropdown.get()

        # Clear existing graph before plotting a new one
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        # Automatically select the first App ID if none is selected
        if not self.app_id_dropdown.get() and self.app_id_dropdown['values']:
            self.app_id_dropdown.set(self.app_id_dropdown['values'][0])

        selected_app_id = self.app_id_dropdown.get()

        # Determine which function to call based on the selected graph type
        if selected_graph_type == "Total Power Consumption by App":
            self.canvas = plot_overview(self.data, self.graph_frame)
        elif selected_graph_type == "Power Consumption Breakdown for a Selected App":
            self.canvas = plot_breakdown(self.data, self.graph_frame, selected_app_id)
        elif selected_graph_type == "Cumulative Power Consumption Over Time":
            self.canvas = plot_timeline(self.data, self.graph_frame, cumulative=True, selected_app_id=selected_app_id)
        elif selected_graph_type == "Power Consumption Over Time":
            self.canvas = plot_timeline(self.data, self.graph_frame, cumulative=False, selected_app_id=selected_app_id)
