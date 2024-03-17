import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from services.file_dialog_service import select_csv_file
from services.graph_service import plot_graph
from services.data_service import load_data, get_app_ids

class GraphWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.data = None
        self.canvas = None
        self.create_widgets()
        self.canvas = plot_graph(parent_frame=self.graph_frame)

    def create_widgets(self):
        # Create a frame to contain the buttons and dropdown, this time aligning it to the left
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.LEFT, fill='y', padx=10, pady=10)  # Align the frame itself to the left

        # Pack each control inside the control_frame to stack them on top of each other
        self.start_stop_button = ttk.Button(control_frame, text="Start/Stop Data Collection", command=self.toggle_data_collection)
        self.start_stop_button.pack(side=tk.TOP, fill='x', padx=5, pady=5)  # Fill the frame horizontally

        self.select_file_button = ttk.Button(control_frame, text="Select CSV File", command=self.select_file)
        self.select_file_button.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        self.app_id_dropdown = ttk.Combobox(control_frame, state="readonly", values=[])
        self.app_id_dropdown.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        # The graph_frame will now take the rest of the space to the right
        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

    def toggle_data_collection(self):
        # Placeholder for actual start/stop functionality
        pass

    def select_file(self):
        file_path = select_csv_file(self)
        if file_path:
            self.data = load_data(file_path)
            app_ids = get_app_ids(self.data)
            self.app_id_dropdown['values'] = app_ids
            self.app_id_dropdown.bind("<<ComboboxSelected>>", self.update_graph)

    def update_graph(self, event):
        selected_app_id = self.app_id_dropdown.get()
        if self.data is not None:
            filtered_data = self.data[self.data['AppId'] == selected_app_id].copy()
            self.canvas = plot_graph(filtered_data, self.graph_frame, self.canvas)
