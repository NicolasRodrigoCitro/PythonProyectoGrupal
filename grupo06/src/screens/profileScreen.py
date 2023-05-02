import PySimpleGUI as sg
import json
from config import *
from ..functions import logicProfileScreen as prof_logic


def abrir_segunda_ventana(un_nombre):
    """Procedimiento que especifica las caracteristicas de la ventana de edicion de perfil"""

    with open(DATA_FILE_PATH, "r") as settings_file:
        jugadores = json.load(settings_file)
        edad_actual= jugadores[un_nombre]['edad']
        genero_actual= jugadores[un_nombre]['genero']

    layout = [[sg.Push('white'), sg.Text('Ventana edicion de perfil',
                                            font=TITULO2,
                                            background_color='White', 
                                            text_color='Black',), sg.Push('white')],
            [sg.Push('white'), sg.Text(f'Nombre: {un_nombre}', 
                                            font=OPCIONES3, 
                                            background_color='White', 
                                            text_color='Black',
                                            pad=((0,0),(10,0))), sg.Push('white')],
            [sg.Push('white'), sg.Text(f'Edad actual: {edad_actual}', 
                                            font=OPCIONES3, 
                                            background_color='White', 
                                            text_color='Black',
                                            pad=((0,0),(10,0))), sg.Push('white')],
            [sg.Push('white'), sg.Text(f'Genero actual: {genero_actual}', 
                                            font=OPCIONES3, 
                                            background_color='White', 
                                            text_color='Black',
                                            pad=((0,0),(0,10))), sg.Push('white')],
            [sg.Push('white'), sg.Text('Ingrese edad nueva',
                                            font=OPCIONES2,background_color='White', 
                                            text_color='Black'), sg.Push('white')],
            [sg.Push('white'), sg.Input(key='-EDAD-', 
                                            enable_events=True), sg.Push('white')],
            [sg.Push('white'), sg.Text('Ingrese genero nuevo', 
                                            font=OPCIONES2, 
                                            background_color='White', 
                                            text_color='Black'), sg.Push('white')],
            [sg.Push('White'), sg.Radio('Hombre', "Hombre", 
                                            key='-HOMBRE-', 
                                            font=OPCIONES, 
                                            background_color='White', 
                                            text_color="black",
                                            circle_color=("light blue")),
            sg.Radio('Mujer', 
                    "Hombre", 
                    key='-MUJER-', 
                    font=OPCIONES, 
                    background_color='White', 
                    text_color="black",
                    circle_color=("light blue")),
            sg.Radio('Sin genero', 
                    'Hombre', default=True, 
                    key='-SIN_GENERO-', 
                    font=OPCIONES, 
                    background_color='White',
                    text_color="black", 
                    circle_color=("light blue")), sg.Push('White')],
            [sg.Push('white'), sg.Button('Ok',
                                        font=OPCIONES,
                                        button_color=("black", "white"),
                                        border_width=(5),
                                        pad=((0,20),(10,50))), 
                                sg.Button('Cancel',
                                        font=OPCIONES,
                                        button_color=("black", "white"),
                                        pad=((0,20),(10,50)),
                                        border_width=(5)), sg.Push('white')]]

    w = sg.Window('Edicion perfil', 
                    layout,
                    size=(1500,1500), 
                    border_depth=(1),
                    location=(-10,0), 
                    background_color='White',
                    margins=(60,60),
                    finalize=True)
                    
    while True:
        event, values = w.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == "Ok":
            edad_nueva = values['-EDAD-']
            if values['-HOMBRE-']:
                genero_nuevo = "hombre"
            elif values['-MUJER-']:
                genero_nuevo = "mujer"
            else:
                genero_nuevo = "sin genero"
            prof_logic.modificacion_de_perfil(un_nombre, edad_nueva,genero_nuevo)
            break
    w.Close()
    abrir_perfil()



def abrir_perfil():
    """Procedimiento que devuelve la ventana de creacion de perfil y
    guarda una lista con los nombres de los pefiles para la listBox"""
    
    lista_perfiles = prof_logic.devolver_lista_perfiles()

    layout = [
        [sg.Button('Volver', 
                    font=OPCIONES,
                    button_color=("black", "white"),
                    border_width=(5)), sg.Push('White')],
        [sg.Push('White'), sg.Text('Ingrese los datos de su perfil',
                                        font = TITULO,
                                        background_color='White',
                                        text_color="black"), sg.Push('White')],
        [sg.Push('White'), sg.Text('Nick: ',
                                        font=OPCIONES,
                                        background_color='White',
                                        text_color="black"), 
                            sg.InputText("", 
                                        key='-NOMBRE-'), sg.Push('White')],
        [sg.Push('White'), sg.Text('Edad: ',
                                        font=OPCIONES,
                                        background_color='White',
                                        text_color="black"), 
                            sg.InputText("", 
                                        key='-EDAD-'), sg.Push('White')],
        [sg.Push('White'), sg.Radio('Hombre', 
                                        "Hombre", 
                                        key='-HOMBRE-',
                                        font=OPCIONES,
                                        background_color='White',
                                        text_color="black",
                                        circle_color=("light blue")),
                            sg.Radio('Mujer', 
                                        "Hombre", 
                                        key='-MUJER-',
                                        font=OPCIONES,
                                        background_color='White',
                                        text_color="black",
                                        circle_color=("light blue")),
                            sg.Radio('Sin genero', 
                                        'Hombre', 
                                        default=True, 
                                        key='-SIN_GENERO-',
                                        font=OPCIONES,
                                        background_color='White',
                                        text_color="black",
                                        circle_color=("light blue")), sg.Push('White')],
        [sg.Push('White'), sg.Button('Crear',
                                        font=OPCIONES,
                                        button_color=("black", "white"),
                                        border_width=(5),
                                        pad=((0,0),(10,50))), sg.Push('White')],

        [sg.Push('White'), sg.Text('Edicion de perfil',
                                        font=OPCIONES2,
                                        background_color='White',
                                        text_color="black"), sg.Push('White')],
        [sg.Push('White'), sg.Combo(lista_perfiles, 
                                        size=(50, 7), 
                                        key='-PERFIL-',default_value='Seleccione un perfil',
                                        enable_events=True), sg.Push('White')],
    ]
    return sg.Window('FiguRace (Creación/Edición de perfil)', 
                        layout,
                        size=(1500,1500), 
                        border_depth=(1),
                        location=(-10,0), 
                        background_color='White',
                        margins=(60,60), 
                        finalize=True)
