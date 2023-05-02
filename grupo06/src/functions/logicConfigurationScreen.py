from config import *
import json
import PySimpleGUI as sg
from src.screens import configurationScreen as config_layout
from src.screens import menuScreen as menu_layout

"""Módulo que implementa las funciones utiizadas en la pantalla de
configuración y modifican su respectivo archivo JSON"""

def agregar_settings_excepcion():
    """Crea un nuevo archivo JSON en caso de que se borre"""

    configuracion ={"facil": {
        "tiempo_x_ronda": 60.0,
        "rondas_x_juego": 10.0,
        "suma_puntaje": 50.0,
        "resta_puntaje": 10.0,
        "car_a_mostrar": 5.0,
        "select": False
    },
    "normal": {
        "tiempo_x_ronda": 40.0,
        "rondas_x_juego": 10.0,
        "suma_puntaje": 30.0,
        "resta_puntaje": 20.0,
        "car_a_mostrar": 3.0,
        "select": False
    },
    "dificil": {
        "tiempo_x_ronda": 20.0,
        "rondas_x_juego": 10.0,
        "suma_puntaje": 20.0,
        "resta_puntaje": 30.0,
        "car_a_mostrar": 2.0,
        "select": False
    },
    "personalizado": {
        "tiempo_x_ronda": 40.0,
        "rondas_x_juego": 10.0,
        "suma_puntaje": 30.0,
        "resta_puntaje": 20.0,
        "car_a_mostrar": 3.0,
        "select": False
    }
    }
    with open(SETTINGS_FILE_PATH, "x") as archivo_settings:
        json.dump(configuracion, archivo_settings, indent=4)

def cargar_personalizado (nombre_perfil):
    """Carga en el archivo JSON que contiene los datos de la 
    configuración los valores de la configuración personalizada del
    perfil elegido"""

    with open(SETTINGS_FILE_PATH, "r") as archivo_config:
        datos_config= json.load(archivo_config)
    with open(DATA_FILE_PATH, "r") as archivo_perfiles:
        datos_perfiles= json.load(archivo_perfiles)
    for perfil, datos in datos_perfiles.items():  #perfil tomará las claves y datos el diccinario con los valores
        if perfil == nombre_perfil:
            datos_config["personalizado"]["tiempo_x_ronda"]= datos["tiempo_x_ronda"]
            datos_config["personalizado"]["rondas_x_juego"]= datos["rondas_x_juego"]
            datos_config["personalizado"]["suma_puntaje"]= datos["suma_puntaje"]
            datos_config["personalizado"]["resta_puntaje"]= datos["resta_puntaje"]
            datos_config["personalizado"]["car_a_mostrar"]= datos["car_a_mostrar"]
    with open (SETTINGS_FILE_PATH, "w") as archivo_config:
        json.dump(datos_config, archivo_config, indent= 4)


def cambiar_dificultad(dificultad_seleccionada):
    """Recibe como parámetro la dificultad elegida por el usuario y 
    la marca como seleccionada en el archivo JSON de configuración."""

    with open (SETTINGS_FILE_PATH, "r") as settings_file:
        datos_config= json.load(settings_file)
    for dificultad, valores in datos_config.items():
        if dificultad == dificultad_seleccionada:
            valores["select"]= True
        else:
            valores["select"]= False
    with open (SETTINGS_FILE_PATH, "w") as settings_file:
        json.dump(datos_config, settings_file, indent=4)


def guardar_personalizado (tiempo_x_ronda, rondas_x_juego, 
    suma_puntaje, resta_puntaje, car_a_mostrar, nombre_selecto):
    """ Guarda los valores de la pantalla de configuración como la 
    configuración personalizada del perfil elegido"""

    with open (SETTINGS_FILE_PATH, "r") as settings_file:
        datos_config= json.load(settings_file)
    datos_config["personalizado"]["tiempo_x_ronda"]= tiempo_x_ronda
    datos_config["personalizado"]["rondas_x_juego"]= rondas_x_juego
    datos_config["personalizado"]["suma_puntaje"]= suma_puntaje
    datos_config["personalizado"]["resta_puntaje"]= resta_puntaje
    datos_config["personalizado"]["car_a_mostrar"]= car_a_mostrar
    
    
    # Si los valores ingresados coinciden con otra dificultad, se marca 
    # esta dificultad como true y no personalizado, ademas de no guardar 
    # los valores como personalizados del usuario
    
    valores_personalizado= [valores for valores in datos_config["personalizado"].values()]
    for dificultad, valores in datos_config.items():        #Busco si los valores ingresados, equivalen a una dificultad existente
        aux=[datos for datos in valores.values()]
        if  aux[:5] == valores_personalizado[:5]:
            difi_aux = dificultad
            break

    if difi_aux == "personalizado":         #Si solo equivale a "personalizado", se guarda como la config personal del user
        with open(DATA_FILE_PATH, "r") as archivo_perfiles:
            datos_perfiles= json.load(archivo_perfiles)
        datos_perfiles [nombre_selecto]["tiempo_x_ronda"]= tiempo_x_ronda
        datos_perfiles [nombre_selecto]["rondas_x_juego"]= rondas_x_juego
        datos_perfiles [nombre_selecto]["suma_puntaje"]= suma_puntaje
        datos_perfiles [nombre_selecto]["resta_puntaje"]= resta_puntaje
        datos_perfiles [nombre_selecto]["car_a_mostrar"]= car_a_mostrar
        with open(DATA_FILE_PATH, "w") as archivo_perfiles:       
            json.dump(datos_perfiles, archivo_perfiles, indent= 4)
    else:
        sg.popup (f"Ingresaste los valores de la dificultad {difi_aux}. \nNo se guardara como tu dificultad personalizada",
                            button_color=("white","grey"),
                            keep_on_top=True)


    with open (SETTINGS_FILE_PATH, "w") as settings_file:
        json.dump(datos_config, settings_file, indent=4)
    
    cambiar_dificultad(difi_aux)        #Se marca como True la dificultad ingresada(personalizado) o la dificultad ya existente
    

def buscar_dificultad ():
    """Busca en el archivo JSON de la configuración la dificultad
    elegida por el usuario y la retorna (valores)"""

    with open (SETTINGS_FILE_PATH, "r") as settings_file:
        datos_config= json.load(settings_file)
    for dificultad in datos_config.values():
        if dificultad["select"]:
            return dificultad

def buscar_dificultad_por_nombre ():
    """Busca en el archivo JSON de la configuración la dificultad
    elegida por el usuario y la retorna"""
    try:
        with open (SETTINGS_FILE_PATH, "r") as settings_file:
            datos_config= json.load(settings_file)
        for dificultad in datos_config:
            if datos_config[dificultad]["select"]:
                return dificultad
    except FileNotFoundError:
        agregar_settings_excepcion()

def procesar_ventana_config(current_window, nombre_selecto):
    """Función que cierra la ventana de menú y abre la ventana de 
       configuración manteniéndola abierta hasta que se toque la cruz
       (WIN_CLOSED) o el botón 'Volver': en el primer caso 
       el juego se cerrará por completo y en el segundo se volverá a 
       abrir la ventana del menú principal. Además se abre el archivo
       JSON con los datos de configuración de las distintas 
       dificultades para guardar los valores que el usuario hay 
       modificado por su cuenta """
       
    current_window.close()
    config_layout.abrir_config(nombre_selecto)
    while True:
        current_window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED:
            current_window.close()
            break
        elif event == "-GUARDAR-": 
            guardar_personalizado(
                values["-TIEMPO_X_RONDA-"], 
                values["-RONDAS_X_JUEGO-"], values["-SUMA_PUNTAJE-"],
                values["-RESTA_PUNTAJE-"], values["-CAR_A_MOSTRAR-"],
            nombre_selecto)
            current_window.close()
            return menu_layout.abrir_menu(nombre_selecto)
        elif event == "-CONFIG_VOLVER-":
            current_window.close()
            return menu_layout.abrir_menu(nombre_selecto)


