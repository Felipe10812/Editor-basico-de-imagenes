from PIL import Image

class ImageOperations:
    """Contiene operaciones de edición de imagen"""

    @staticmethod
    def crop(image: Image.Image, box: tuple):
        """Recibe la imagen y el cuadro (left, top, right, bottom) en pixeles"""
        return image.crop(box)

    @staticmethod
    def resize(image: Image.Image, width: int, height: int):
        return image.resize((width, height), resample=Image.LANCZOS)
