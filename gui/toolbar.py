import tkinter as tk

class Toolbars:
    def __init__(self, root, app):
        """
        root = ventana principal
        app = referencia a la app principal (ImageEditorApp)
        """
        self.root = root
        self.app = app
        self._setup_top_toolbar()

    def _setup_top_toolbar(self):
        """Opciones de rotación arriba"""
        toolbar_top = tk.Frame(self.root, bg="#444444")
        toolbar_top.pack(fill=tk.X, side=tk.TOP)

        # Botones principales
        tk.Button(toolbar_top, text="Abrir", command=self.app.open_image).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar_top, text="Recortar", command=self.app.crop_image).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar_top, text="Redimensionar", command=self.app.resize_image).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar_top, text="Guardar como...", command=self.app.save_image).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar_top, text="Restablecer", command=self.app.reset_image).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar_top, text="Cerrar", command=self.root.quit).pack(side=tk.RIGHT, padx=2, pady=2)

        # Botones de rotación
        tk.Button(toolbar_top, text="Rotar ↺", command=self.app.rotate_left).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar_top, text="Rotar ↻", command=self.app.rotate_right).pack(side=tk.LEFT, padx=2, pady=2)