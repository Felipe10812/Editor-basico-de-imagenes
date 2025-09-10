import tkinter as tk
from gui.app import ImageEditorApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")

    app = ImageEditorApp(root)  # ya crea el toolbar internamente

    root.mainloop()