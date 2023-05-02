from operator import truediv
import uuid
import PySimpleGUI as sg
from config import *
from ..functions.logicGameScreen import *
from ..functions.logicGeneric import *


def abrir_juego(dicc_juego, nombre_perfil, dificultad_elegida, dicc_config):

    dicc_imagenes = {
        "fifa": FIFA_IMG_FILE,
        "lagos": LAGO_IMG_FILE,
        "spotify": SPOTIFY_IMG_FILE
    }

    data_izquierda_layout = [
        [sg.Text(f'Dataset: {dicc_juego["nombre_dataset"]}',
                            font=OPCIONES2, 
                            text_color=("black"), 
                            background_color=("white"), 
                            pad=((0,0),(0,20)),
                            key="-DATASET-")],
        [sg.Text(f"Dificultad: {dificultad_elegida}", 
                            font=OPCIONES2, 
                            text_color=("black"), 
                            size=(20,2),
                            background_color=("white"), 
                            pad=((0,0),(0,0))) ],
        [sg.Image(filename = dicc_imagenes[f'{dicc_juego["nombre_dataset"].lower()}'], 
                    background_color=("white"), 
                    size=(300, 200),
                    pad=((0,0),(0,0)),
                    key="-IMAGEN-")],
        [sg.Text(f'Jugando: {nombre_perfil}', 
                font=OPCIONES2, 
                size=(20,3),
                text_color=("black"), 
                background_color=("white"))],
        [sg.VPush("white")],
        [sg.Button("Abandonar juego", 
                    font=OPCIONES, 
                    pad=((0,0),(175,0)),
                    button_color=("black", "white"), 
                    key="-JUEGO_ABANDONAR-"), sg.Push("white")]
    ]
    
    
    indicios_layout = []
    for i in range(dicc_config["cant_caract"]):
        indicios_layout.append([sg.Text(f'{dicc_juego["encabezado"] [i]} = {dicc_juego["dataset"][dicc_juego["fila_rta_correcta"]][i]}',
                    font=OPCIONES,
                    border_width=(2),
                    pad=((0,0),(0,0)),
                    justification="c",
                    size=(43,2),
                    text_color=("black"),
                    background_color=("white"),
                    key=f"-PISTA{i}-")])

    botones_layout = []
    for i in range(5):
        botones_layout.append([sg.Button(f'{dicc_juego["opciones"][i]}',
                    button_color=("white",COLOR1), 
                    font=OPCIONES3, 
                    border_width=(2),
                    size=(20,1),
                    pad=((0,0),(0,0)),
                    key=f"-OPCION{i}-")])  


    tarjeta_layout = [
        [sg.Push("white"), sg.Column(indicios_layout), sg.Push("white")],
        [sg.Text ("Elija la opcion que corresponda a esta información", 
                    font=OPCIONES, 
                    text_color=("black"),
                    pad=((0,0),(0,0)), 
                    background_color=("white"))],
        [sg.Push("white"), sg.Column(botones_layout), sg.Push("white")],
        [sg.Push("white"), sg.Button("Pasar", font=OPCIONES, 
                    button_color=("black", "white"), 
                    border_width=(5),
                    key="-SIGUIENTE-"), sg.Push("white")]
    ]
    
    data_derecha_layout = [
        [sg.Push("white"), sg.Text(int(dicc_config["tiempo_por_ronda"]), 
                    font=TITULO2, 
                    text_color=("black"), 
                    background_color=("white"), 
                    pad=((0,0),(0,0)),
                    key="-TIMER-"), sg.Push("white")],
    ]   
    for i in range(1, dicc_config["cant_rondas"]+1):
        data_derecha_layout.append([sg.Text(f'Ronda {i}:',
                                    font = TEXTO,
                                    text_color=("black"),
                                    background_color='white',
                                    key=f"-RONDA{i}-")])
    

    layout_izquierdo = [
        [sg.Column(data_izquierda_layout, background_color="white")]
    ]
    layout_central = [
        [sg.Column(tarjeta_layout, background_color="white")]
    ]
    layout_derecho = [
        [sg.Column(data_derecha_layout, background_color="white")]
    ]

    layout = [
        [sg.Frame(None, layout_izquierdo, background_color="white", size=(300,1500)),
        sg.Frame(None, layout_central, background_color="white", size=(700,1500), element_justification="c"),
        sg.Frame(None, layout_derecho, background_color="white", size=(250,1500))]
    ] 


    return sg.Window("FiguRace (Juego)", 
            layout, 
            margins=(60,60),
            size=(1500,1500),
            border_depth=(1),
            location=(-10,0), 
            background_color=("white"),
            finalize=True), str(uuid.uuid4())       #creo id de partida unica cada vez que creo juego