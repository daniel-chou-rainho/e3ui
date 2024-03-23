import tkinter as tk
from ttkthemes import ThemedTk
from windows.graph_window import GraphWindow

def main():
    #root = tk.Tk()
    root = ThemedTk(theme="arc")
    root.title('E3UI')
    root.geometry('800x600')
    root.minsize(800, 600)
    app = GraphWindow(root)
    app.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
