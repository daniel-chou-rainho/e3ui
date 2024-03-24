import tkinter as tk
from tkinter import ttk
from services.data.select_csv_file import select_csv_file
from services.data.get_app_ids import get_app_ids
from services.data.load_data import load_data
from services.plot.plot_overview import plot_overview
from services.plot.plot_breakdown import plot_breakdown
from services.plot.plot_timeline import plot_timeline
from services.plot.plot_carbon import plot_carbon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from services.e3.clear_database import clear_database
from services.e3.get_csv import get_csv

class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.data = None
        self.canvas = None
        self.configure(background='#F0F7EE')  # A light green/white background
        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self, bg='#DAE5D0')  # Light green background
        control_frame.pack(side=tk.LEFT, fill='y', padx=10, pady=10)

        button_frame = tk.Frame(control_frame, bg='#DAE5D0')
        button_frame.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        # Use a more natural, subdued green for buttons
        style = ttk.Style()
        style.configure('TButton', background='#88A09E', foreground='dark gray')
        style.map('TButton', background=[('active', '#8ABF9B')])
        # Configure the style for the dropdown
        style.configure('TCombobox', fieldbackground='white', foreground='dark gray', selectbackground='white', selectforeground='dark gray')


        self.start_button = ttk.Button(
            button_frame,
            text="Start Data Collection",
            command=self.start_data_collection
        )
        self.start_button.pack(side=tk.LEFT, fill='x', expand=True, padx=2.5, pady=5)

        self.stop_button = ttk.Button(
            button_frame,
            text="Stop Data Collection",
            command=self.stop_data_collection
        )
        self.stop_button.pack(side=tk.LEFT, fill='x', expand=True, padx=2.5, pady=5)

        self.select_file_button = ttk.Button(
            control_frame,
            text="Select CSV File",
            command=self.select_file
        )
        self.select_file_button.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        self.filename_label = tk.Label(
            control_frame,
            text="No file selected",
            foreground="gray",
            bg='#DAE5D0'
        )
        self.filename_label.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        self.graph_type_dropdown = ttk.Combobox(
            control_frame,
            state="readonly",
            values=[
                "Total Power Consumption by App",
                "Power Consumption Breakdown for a Selected App",
                "Cumulative Power Consumption Over Time",
                "Power Consumption Over Time",
                "Cummulative CO2 emmision"
            ]
        )
        self.graph_type_dropdown.pack(side=tk.TOP, fill='x', padx=5, pady=5)
        self.graph_type_dropdown.bind("<<ComboboxSelected>>", self.update_graph)

        self.app_id_dropdown = ttk.Combobox(control_frame, state="readonly", values=[])
        self.app_id_dropdown.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        self.graph_frame = tk.Frame(self, background="white")
        self.graph_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)


    def start_data_collection(self):
        # Clear the database
        clear_database()
        print("Database cleared. Data collection can start.")

    def stop_data_collection(self):
        # Call get_csv to generate the CSV file and load the data
        file_path = get_csv()
        if file_path:
            # Load the data from the CSV file
            self.update_data_and_ui(file_path)
        else:
            print("Failed to generate or load CSV file.")

    def select_file(self):
        file_path = select_csv_file(self)
        if file_path:
            self.update_data_and_ui(file_path)

    def update_data_and_ui(self, file_path):
        self.data = load_data(file_path)
        app_ids = get_app_ids(self.data)
        self.app_id_dropdown['values'] = app_ids
        # Ensure that UI updates happen in the main thread
        self.after(0, self.app_id_dropdown.bind, "<<ComboboxSelected>>", self.update_graph)
        filename = file_path.split('/')[-1]
        # Ensure that UI updates happen in the main thread
        self.after(0, self.filename_label.config, {'text': filename, 'foreground': "black"})
        # Automatically trigger graph update
        self.after(0, self.update_graph, None)

    def update_graph(self, event):
        selected_graph_type = self.graph_type_dropdown.get()

        # Automatically select the first App ID if none is selected
        if not self.app_id_dropdown.get() and self.app_id_dropdown['values']:
            self.app_id_dropdown.set(self.app_id_dropdown['values'][0])

        selected_app_id = self.app_id_dropdown.get()

        # Check if canvas exists; if not, initialize it
        if not self.canvas:
            fig, ax = plt.subplots()
            self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(fill="both", expand=True)
        else:
            # Clear the figure (or axes) for the new plot
            self.canvas.figure.clf()

        # Depending on the type of graph, call the respective function
        if selected_graph_type == "Total Power Consumption by App":
            plot_overview(self.data, self.canvas.figure)
        elif selected_graph_type == "Power Consumption Breakdown for a Selected App":
            plot_breakdown(self.data, self.canvas.figure, selected_app_id)
        elif selected_graph_type == "Cumulative Power Consumption Over Time":
            plot_timeline(self.data, self.canvas.figure, cumulative=True, selected_app_id=selected_app_id)
        elif selected_graph_type == "Power Consumption Over Time":
            plot_timeline(self.data, self.canvas.figure, cumulative=False, selected_app_id=selected_app_id)
        elif selected_graph_type == "Cummulative CO2 emmision":
            plot_carbon(self.data, self.canvas.figure, selected_app_id=selected_app_id)

        self.canvas.draw()
