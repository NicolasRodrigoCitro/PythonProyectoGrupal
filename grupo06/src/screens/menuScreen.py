import PySimpleGUI as sg
import json
from config import *
from src.functions import logicProfileScreen as prof_logic


def abrir_menu(nombre_selecto):
    """Procedimiento que recibe el nombre de perfil elegido y especifica 
    las caracteristicas de la ventana menu (layout y perfiles que se muestan
    arriba a la derecha) y la devuelve como ventana"""

    with open(SETTINGS_FILE_PATH, "r") as archivo_settings:
        configuracion = json.load(archivo_settings)
        
    try:       
        with open(DATA_FILE_PATH, "r") as archivo_perfiles:
            jugadores = json.load(archivo_perfiles)  
    except FileNotFoundError:
        prof_logic.crear_data_perfil_excepcion()      
        with open(DATA_FILE_PATH, "r") as archivo_perfiles:
            jugadores = json.load(archivo_perfiles)
    finally:
        lista_perfiles = [nombre for nombre, claves in jugadores.items()] #creo lista con perfiles

        
    options_frame_layout= [
        [sg.Text("FiguRace", 
                font=TITULO3, 
                text_color="black", 
                background_color=("white"))],
        [sg.Push("white"), sg.Button(("Jugar"), 
                                    button_color=("black", "white"), 
                                    font=OPCIONES3, size=(13,1), 
                                    border_width=(5), 
                                    pad=((0,0),(30,0))), sg.Push("white")],
        [sg.Push("white"), sg.Button(("Configuracion"), 
                                    button_color=("black", "white"), 
                                    font=OPCIONES3, size=(13,1), 
                                    border_width=(5), 
                                    pad=((0,0),(0,0))), sg.Push("white")],
        [sg.Push("white"), sg.Button(("Puntajes"), 
                                    button_color=("black", "white"), 
                                    font=OPCIONES3, 
                                    size=(13,1), 
                                    border_width=(5), 
                                    pad=((0,0),(0,0))), sg.Push("white")],
        [sg.Push("white"), sg.Button(("Perfil"), 
                                    button_color=("black", "white"), 
                                    font=OPCIONES3, 
                                    size=(13,1), 
                                    border_width=(5), 
                                    pad=((0,0),(0,0))), sg.Push("white")],
        [sg.Push("white"), sg.Button(("Salir"), 
                                    button_color=("black", "white"), 
                                    font=OPCIONES3, 
                                    size=(13,1), 
                                    border_width=(5), 
                                    pad=((0,0),(0,0))), sg.Push("white")]
        ]

    difficulty_users_frame_layout= [
        [sg.Text("Usuario", 
                font=OPCIONES3, 
                text_color=("black"), 
                background_color=("white")), sg.Push("white")],
        [sg.Combo(lista_perfiles, 
                size=(15), 
                readonly=True, 
                font=OPCIONES, 
                text_color=("black"), 
                button_arrow_color="black", 
                button_background_color= ("white"), 
                background_color= ("white"), 
                pad=((0,0),(0,130)), 
                enable_events=True, 
                key='-PERFIL_SELECTO-', 
                default_value=nombre_selecto)],
        [sg.Text(("Dificultad"), 
                font=OPCIONES3, 
                text_color=("black"), 
                background_color=("white"))],
        [sg.Radio(("Facil"), 
                    ("dificultad"), 
                    circle_color=("light blue"), 
                    background_color=("white"), 
                    text_color=("green"), 
                    default= configuracion["facil"]["select"], 
                    font=OPCIONES2, 
                    enable_events=True, 
                    key="-FACIL-")],
        [sg.Radio(("Normal"), 
                    ("dificultad"), 
                    circle_color=("light blue"), 
                    background_color=("white"), 
                    text_color=("orange"), 
                    default= configuracion["normal"]["select"], 
                    font=OPCIONES2, 
                    enable_events=True, 
                    key="-NORMAL-"), sg.Push("white")],
        [sg.Radio(("Dificil"), 
                    ("dificultad"), 
                    circle_color=("light blue"), 
                    background_color=("white"), 
                    text_color=("red"), 
                    default= configuracion["dificil"]["select"], 
                    font=OPCIONES2, 
                    enable_events=True, 
                    key="-DIFICIL-"), sg.Push("white")],
        [sg.Radio(("Personalizado"), 
                    ("dificultad"), 
                    circle_color=("light blue"), 
                    background_color=("white"), 
                    text_color=("brown"), 
                    default= configuracion["personalizado"]["select"], 
                    font=OPCIONES2, 
                    enable_events=True, 
                    key="-PERSONALIZADO-"), sg.Push("white")]
    ]

    invisible_frame_layout=[
        [sg.Text("          ", 
                font=OPCIONES3, 
                text_color=("black"), 
                background_color=("white"))]
    ]

    layout= [
        [sg.Frame(None, 
                    invisible_frame_layout, 
                    background_color=("white"), 
                    border_width=0, 
                    pad=((0,50),(0,0))), 
        sg.Frame(None, 
                    options_frame_layout, 
                    background_color=("white"), 
                    border_width=0), 
        sg.Frame(None, 
                    difficulty_users_frame_layout, 
                    background_color=("white"), 
                    border_width=0, 
                    pad=(50,0))]
        ]
    return sg.Window("Figurace (Menú Principal)", 
                        layout,
                        size=(1500,1500), 
                        border_depth=(1),
                        location=(-10,0),
                        margins=(60,60), 
                        background_color=("white"), 
                        finalize=True)

