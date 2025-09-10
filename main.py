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

import tkinter as tk
from gui.app import ImageEditorApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")

    app = ImageEditorApp(root)  # ya crea el toolbar internamente

    root.mainloop()