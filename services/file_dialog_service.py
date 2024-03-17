from tkinter import filedialog

def select_csv_file(parent):
    file_path = filedialog.askopenfilename(
        parent=parent,
        title="Select CSV File",
        filetypes=(("CSV files", "*.csv"),
        ("All files", "*.*"))
    )
    return file_path
