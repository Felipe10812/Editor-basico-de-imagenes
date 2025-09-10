from PIL import Image

class ImageManager:
    """Gestiona la imagen cargada y su versión actual en memoria"""
    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.path = None

    def load_image(self, path: str):
        img = Image.open(path).convert("RGBA")
        self.original_image = img.copy()
        self.current_image = img
        self.path = path

    def reset(self):
        if self.original_image:
            self.current_image = self.original_image.copy()

    def save(self, path: str):
        ext = path.lower().split('.')[-1]
        if ext in ("jpg", "jpeg"):
            self.current_image.convert("RGB").save(path, "JPEG", quality=95, optimize=True)
        else:
            self.current_image.save(path)
            