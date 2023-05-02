"""Archivo con constantes (Fuentes, colores, valores y rutas de carpetas y archivos)"""
import os

#fuentes
TEXTO = ("Courier New", "10")
OPCIONES = ("Courier new", "14")
OPCIONES2= ("Courier New", "18")
OPCIONES3 = ("Courier New", "22")
OPCIONES4 = ("Courier new", "12")

TITULO = ("Courier New", "30")
TITULO2 = ("Courier New", "48")
TITULO3 = ("Courier New", "68")

#colores
COLOR1="LightSkyBlue4"
COLOR2="olive drab"
COLOR3="light coral"

#Cantidad de puntajes a mostrar en la pantalla de puntajes 
CANT_PTS_MOSTRAR= 20

#rutas carpetas
MAIN_PATH = os.path.dirname((__file__))
SRC_PATH = os.path.join(MAIN_PATH, "src")

SCREENS_PATH = os.path.join(SRC_PATH, "screens")
FUNCTIONS_PATH = os.path.join(SRC_PATH, "functions")
DATAFILES_PATH = os.path.join(SRC_PATH, "datafiles")
IMAGES_PATH = os.path.join(SRC_PATH, "images")
PRIMITIVES_PATH = os.path.join(DATAFILES_PATH, "primitives")
PROCESSED_PATH = os.path.join(DATAFILES_PATH, "processed")

#rutas archivos
SETTINGS_FILE_PATH = os.path.join(DATAFILES_PATH, "settings.json")
DATA_FILE_PATH = os.path.join(DATAFILES_PATH, "data.json")
DATA_FILE_EVENTO_PATH = os.path.join(DATAFILES_PATH, "data_eventos.csv")

FIFA_IMG_FILE = os.path.join(IMAGES_PATH, "fifa_img.png")
LAGO_IMG_FILE = os.path.join(IMAGES_PATH, "lagos_img.png")
SPOTIFY_IMG_FILE = os.path.join(IMAGES_PATH, "spotify_img.png")



