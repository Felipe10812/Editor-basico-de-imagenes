# -*- coding: utf-8 -*-
"""
Editor Básico de Imágenes
Desarrollado por: Felipe Acosta
"""

# -----------------------------------------------------------------------------
# Copyright (c) 2025, Felipe Acosta.
#
# Licenciado bajo la Licencia MIT.
# Ver el archivo LICENSE para más detalles.
# -----------------------------------------------------------------------------

import sys
import os
import tkinter as tk
from gui.app import ImageEditorApp

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")

    app = ImageEditorApp(root, resource_path)  # Pasamos la función a la app

    root.mainloop()