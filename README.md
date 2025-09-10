# Proyecto de Editor de Imágenes

Este proyecto es un editor de imágenes básico que permite realizar operaciones como recortar, redimensionar y guardar imágenes. Está diseñado siguiendo los principios de la arquitectura SOLID, lo que facilita su mantenimiento y expansión en el futuro.

## Estructura del Proyecto

```
image_editor/
├── main.py                 # Punto de entrada
|
├── gui/
│   ├── app.py              # Clase principal de la GUI
│   └── toolbar.py          # Barra de botones
|
├── core/
│   ├── image_manager.py    # Carga, guarda, resetea y manipula imágenes
│   └── operations.py       # Crop, resize, etc.
|
├── utils/
│   └── dialogs.py          # Funciones para cuadros de diálogo
|
├── requirements.txt        # Dependencias del proyecto
└── README.md               
```

## Requisitos
Los requisitos se encuentran en el archivo [requirements.txt](requirements.txt).


## Instalación

1. Clona el repositorio en tu máquina local.
2. Navega al directorio del proyecto.
3. Instala las dependencias necesarias ejecutando:

```
pip install -r requirements.txt
```

## Uso

Para iniciar el editor de imágenes, ejecuta el archivo `main.py`:

```
python main.py

```

## Funcionalidades

- **Abrir Imágenes**: Permite seleccionar imágenes desde el sistema de archivos.
- **Recortar Imágenes**: Selecciona un área de la imagen para recortarla.
- **Redimensionar Imágenes**: Cambia el tamaño de la imagen manteniendo la relación de aspecto.
- **Guardar Imágenes**: Guarda la imagen editada en el formato deseado.
- **Rotar Imágenes**: Gira la imagen 90 grados a la izquierda o derecha.

## Creación del Ejecutable

Para crear un archivo ejecutable independiente, puedes usar `PyInstaller`. Esta herramienta ya está incluida en el archivo `requirements.txt`, por lo que se instalará junto con las demás dependencias al seguir los pasos de la sección 

**Instalación**.

1. Instala `PyInstaller`:
   ```
   pip install pyinstaller
   ```
2. Genera el ejecutable desde el directorio raíz del proyecto:
   ```
   python -m PyInstaller --onefile --windowed --name="ImageEditor" main.py
   ```
   El archivo ejecutable se encontrará en la carpeta `dist`.


El archivo ejecutable se encontrará en la carpeta `dist`.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia [MIT](LICENSE).