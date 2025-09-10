import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox

def ask_image_path(title="Abrir imagen"):
    return filedialog.askopenfilename(
        title=title,
        filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.webp"), ("Todos los archivos", "*.*")]
    )

def ask_save_path(default_ext=".png"):
    return filedialog.asksaveasfilename(
        defaultextension=default_ext,
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("Todos los archivos", "*.*")]
    )

def ask_resize_dimensions(current_w, current_h, root):
    answer = simpledialog.askstring(
        "Redimensionar",
        f"Ingrese el nuevo ancho x alto (o solo ancho para mantener la proporción). Actual: {current_w}x{current_h}",
        parent=root
    )
    return answer

def show_info(msg):
    messagebox.showinfo("Información", msg)

def show_error(msg):
    messagebox.showerror("Error", msg)