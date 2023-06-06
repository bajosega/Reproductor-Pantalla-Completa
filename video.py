import tkinter as tk
from tkinter import filedialog
import cv2
import ctypes
import configparser

# Archivo de configuración
CONFIG_FILE = "config.ini"

# Sección del archivo de configuración
CONFIG_SECTION = "AppConfig"

def save_config(video_path):
    config = configparser.ConfigParser()
    config[CONFIG_SECTION] = {"last_video_path": video_path}

    with open(CONFIG_FILE, "w") as config_file:
        config.write(config_file)

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    if config.has_section(CONFIG_SECTION):
        return config[CONFIG_SECTION].get("last_video_path", "")

    return ""

def select_video():
    # Abrir el cuadro de diálogo para seleccionar el archivo de video
    video_path = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4")])

    if video_path:
        global video_path_var
        video_path_var.set(video_path)

def play_video():
    video_path = video_path_var.get()

    if video_path:
        save_config(video_path)
        global stop_key_var 
        stop_key = stop_key_var.get()

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error al abrir el archivo de video.")
            return

        cv2.namedWindow("Reproduciendo video", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Reproduciendo video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty("Reproduciendo video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Ocultar el cursor del mouse
        ctypes.windll.user32.ShowCursor(False)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Reproduciendo video", frame)
            key = cv2.waitKey(30)
            if key == ord(stop_key):
                break

        cap.release()
        cv2.destroyAllWindows()

        # Restaurar el cursor del mouse
        ctypes.windll.user32.ShowCursor(True)

def create_gui():
    def load_last_video_path():
        last_video_path = load_config()
        video_path_var.set(last_video_path)

    root = tk.Tk()
    root.title("Reproductor de video")

    # Obtener el ancho y la altura de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Establecer el tamaño y la posición del formulario
    form_width = 800
    form_height = 300
    form_x = (screen_width - form_width) // 2
    form_y = (screen_height - form_height) // 2
    root.geometry(f"{form_width}x{form_height}+{form_x}+{form_y}")

    # Etiqueta para mostrar la ruta del video seleccionado
    video_path_label = tk.Label(root, text="Ruta del video:")
    video_path_label.pack(pady=10)

    # Variable para almacenar la ruta del video seleccionado
    global video_path_var
    video_path_var = tk.StringVar(root)
    video_path_entry = tk.Entry(root, textvariable=video_path_var, state=tk.DISABLED,width=100)
    video_path_entry.pack()

    # Botón para seleccionar el video
    select_button = tk.Button(root, text="Seleccionar video", command=select_video)
    select_button.pack(pady=10)

    # Cargar la última ruta de video al abrir la aplicación
    load_last_video_path()

    # Selector de tecla para detener el video
    global stop_key_var
    stop_key_var = tk.StringVar(root, value="*")
    stop_key_label = tk.Label(root, text="PARAR video con")
    stop_key_label.pack(pady=10)
    stop_key_selector = tk.Entry(root, textvariable=stop_key_var)
    stop_key_selector.pack()

    # Botón para iniciar el video
    start_button = tk.Button(root, text="Iniciar video", command=play_video)
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
