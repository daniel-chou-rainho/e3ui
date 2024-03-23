import tkinter as tk
from ttkthemes import ThemedTk
from windows.main_window import MainWindow

def main():
    root = ThemedTk(theme="arc")
    root.title('E3UI')
    root.geometry('1000x600')
    root.minsize(1000, 600)
    app = MainWindow(root)
    app.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
