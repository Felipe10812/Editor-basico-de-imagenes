import tkinter as tk
from tkinter import Toplevel, Label, messagebox
import webbrowser
from PIL import ImageTk
from core.image_manager import ImageManager
from core.operations import ImageOperations
from utils.dialogs import ask_image_path, ask_save_path, ask_resize_dimensions, show_info, show_error
from gui.toolbar import Toolbars  # 👈 importamos las toolbars

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes")

        # 🔹 Ventana adaptable a pantalla completa
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        default_w = screen_w // 2  # ancho por defecto: la mitad de la pantalla
        default_h = screen_h // 2  # alto por defecto: la mitad de la pantalla
        root.geometry(f"{default_w}x{default_h}")  # ventana redimensionable
        root.minsize(400, 300)  # tamaño mínimo

        self.image_manager = ImageManager()
        self.photo = None
        self.display_image = None
        self.scale = 1.0
        self.has_unsaved_changes = False
        
        # toolbar de rotación
        self.toolbar = Toolbars(self.root, self)

        
        self.canvas = tk.Canvas(root, cursor="cross", bg="#333333")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Eventos de selección
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Atajo de teclado para mostrar la información del autor
        self.root.bind("<Control-l>", self.show_about_info)

        # Interceptar el evento de cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.rect = None
        self.start_x = self.start_y = self.cur_x = self.cur_y = None


    def open_image(self):
        path = ask_image_path("Abrir imagen")
        if not path:
            return
        try:
            self.image_manager.load_image(path)
        except Exception as e:
            show_error(f"No se pudo abrir la imagen:\n{e}")
            return
        self.reset_image()

    def reset_image(self):
        self.image_manager.reset()
        self.display_image = self.image_manager.current_image
        self.has_unsaved_changes = False
        self._render_to_canvas()
        self.clear_rectangle()

    def _render_to_canvas(self):
        if self.display_image is None:
            return
        w, h = self.display_image.size
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 600
        scale = min((cw-10)/w, (ch-10)/h, 1.0)
        self.scale = scale
        disp_w, disp_h = int(w*scale), int(h*scale)
        resized = self.display_image.resize((disp_w, disp_h))
        self.photo = ImageTk.PhotoImage(resized)
        self.canvas.delete("all")
        self.canvas.config(width=disp_w, height=disp_h)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self._disp_size = (disp_w, disp_h)

    def on_button_press(self, event):
        if self.display_image is None:
            return
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_move_press(self, event):
        if not self.rect:
            return
        self.cur_x, self.cur_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.cur_x, self.cur_y)

    def on_button_release(self, event):
        if not self.rect:
            return
        self.cur_x, self.cur_y = event.x, event.y
        disp_w, disp_h = self._disp_size
        self.start_x = max(0, min(self.start_x, disp_w))
        self.start_y = max(0, min(self.start_y, disp_h))
        self.cur_x = max(0, min(self.cur_x, disp_w))
        self.cur_y = max(0, min(self.cur_y, disp_h))
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.cur_x, self.cur_y)

    def clear_rectangle(self):
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None

    def _coords_display_to_image(self, x, y):
        return int(x / self.scale), int(y / self.scale)

    def crop_image(self):
        if self.image_manager.current_image is None:
            show_info("Primero abre una imagen.")
            return
        if self.rect is None:
            show_info("Dibuja un rectángulo para recortar.")
            return
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        il, it = self._coords_display_to_image(min(x1, x2), min(y1, y2))
        ir, ib = self._coords_display_to_image(max(x1, x2), max(y1, y2))
        w, h = self.image_manager.current_image.size
        il, it = max(0, il), max(0, it)
        ir, ib = min(ir, w), min(ib, h)
        if ir - il < 1 or ib - it < 1:
            show_info("El área seleccionada es demasiado pequeña.")
            return
        cropped = ImageOperations.crop(self.image_manager.current_image, (il, it, ir, ib))
        self.image_manager.current_image = cropped
        self.display_image = cropped
        self._render_to_canvas()
        self.clear_rectangle()
        self.has_unsaved_changes = True
        show_info(f"Imagen recortada a {cropped.size[0]} x {cropped.size[1]} píxeles")

    def resize_image(self):
        if self.image_manager.current_image is None:
            show_info("Primero abre una imagen.")
            return
        w, h = self.image_manager.current_image.size
        answer = ask_resize_dimensions(w, h, self.root)
        if not answer:
            return
        try:
            if "x" in answer:
                parts = answer.lower().split("x")
                new_w = int(parts[0].strip())
                new_h = int(parts[1].strip())
            else:
                new_w = int(answer.strip())
                new_h = int(round((new_w / w) * h))
        except:
            show_error("Formato de tamaño inválido. Usa ancho x alto, por ejemplo: 800x600 o solo 800.")
            return
        if new_w <= 0 or new_h <= 0:
            show_error("Las dimensiones deben ser números positivos.")
            return
        resized = ImageOperations.resize(self.image_manager.current_image, new_w, new_h)
        self.image_manager.current_image = resized
        self.display_image = resized
        self._render_to_canvas()
        self.has_unsaved_changes = True
        show_info(f"Imagen redimensionada a {new_w} x {new_h} píxeles")
        
    def rotate_left(self):
        if self.image_manager.current_image:
           self.image_manager.current_image = self.image_manager.current_image.rotate(90, expand=True)
           self.display_image = self.image_manager.current_image
           self.has_unsaved_changes = True
           self._render_to_canvas()

    def rotate_right(self):
        if self.image_manager.current_image:
            self.image_manager.current_image = self.image_manager.current_image.rotate(-90, expand=True)
            self.display_image = self.image_manager.current_image
            self.has_unsaved_changes = True
            self._render_to_canvas()
    
    def save_image(self):
        if self.image_manager.current_image is None:
            show_info("Primero abre una imagen.")
            return
        path = ask_save_path()
        if not path:
            return
        try:
            self.image_manager.save(path)
            self.has_unsaved_changes = False
            show_info(f"Imagen guardada en: {path}")
        except Exception as e:
            show_error(f"No se pudo guardar la imagen:\n{e}")

    def on_closing(self):
        """Maneja el evento de cierre de la ventana."""
        if self.has_unsaved_changes:
            response = messagebox.askyesnocancel(
                "Salir sin guardar",
                "Tienes cambios sin guardar. ¿Deseas guardarlos antes de salir?"
            )
            if response is True:  # Sí, guardar
                self.save_image()
                # Si el usuario no canceló el guardado, cerramos.
                if not self.has_unsaved_changes:
                    self.root.destroy()
            elif response is False:  # No, salir sin guardar
                self.root.destroy()
            # Si es None (Cancelar), no hacemos nada.
        else:
            self.root.destroy()

    def show_about_info(self, event=None):
        """Muestra una ventana personalizada con información del autor y enlace a GitHub."""
        about_window = Toplevel(self.root)
        about_window.title("Acerca de Image Editor")
        about_window.geometry("400x220")
        about_window.resizable(False, False)
        about_window.transient(self.root) # Mantener la ventana por encima de la principal

        # Centrar la ventana de "Acerca de" relativa a la ventana principal
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()
        win_w = 400
        win_h = 220
        x = root_x + (root_w // 2) - (win_w // 2)
        y = root_y + (root_h // 2) - (win_h // 2)
        about_window.geometry(f'+{x}+{y}')

        main_message = (
            "Editor Básico de Imágenes v1.0\n\n"
            "Desarrollado por: Felipe Acosta\n"
            "Copyright © 2025, Felipe Acosta."
        )
        Label(about_window, text=main_message, justify=tk.CENTER, padx=10, pady=10).pack()

        github_url = "https://github.com/Felipe10812" # 👈 ¡RECUERDA CAMBIAR ESTO!
        link_label = Label(about_window, text="Perfil de GitHub", fg="blue", cursor="hand2")
        link_label.pack(pady=5)
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new(github_url))

        license_message = "Este programa está licenciado bajo la Licencia MIT."
        Label(about_window, text=license_message, justify=tk.CENTER, padx=10, pady=10).pack()

        about_window.grab_set() # Bloquear interacción con la ventana principal
        self.root.wait_window(about_window) # Esperar a que se cierre la ventana de "Acerca de"