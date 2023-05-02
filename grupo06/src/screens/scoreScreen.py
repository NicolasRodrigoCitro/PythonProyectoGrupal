import PySimpleGUI as sg
import json
import operator
from config import *
from ..functions import logicScoreScreen as logic_score
from ..functions import logicProfileScreen as logic_profile
from src.screens import menuScreen as menu_layout

def abrir_formulario(nombre_selecto):
      layout = [
        [                   sg.Button("Volver", 
                            font=OPCIONES, 
                            button_color=("black", "white"), 
                            border_width=(5),
                            pad=((0,0),(0,20)),
                            key="-PUNTAJES_VOLVER-"), sg.Push("white")],
        [sg.Push('White'), sg.Text('ELIJA COMO QUIERE ORDENAR LA TABLA DE PUNTAJES ',
                                        font=TITULO2,
                                        background_color='White',
                                        text_color="black"),sg.Push("white")],
        [sg.Push('White'), sg.Text('CAMBIO DE TIPO',
                                        font=TITULO,
                                        background_color='White',
                                        text_color="black"), 
                             
                            sg.Radio('nombre', 
                                        "puntaje", 
                                        key='-NOMBRE-',
                                        font=OPCIONES3,
                                        background_color='White',
                                        text_color="black",
                                        circle_color=("light blue")),
                            sg.Radio('puntaje', 
                                        "puntaje", 
                                        key='-PUNTAJE-',
                                        font=OPCIONES3,
                                        default=True,
                                        background_color='White',
                                        text_color="black",
                                        circle_color=("light blue")),sg.Push("white")], 
                        
                [sg.Push('White'), sg.Text('CAMBIO DE ORDEN',
                                        font=TITULO,
                                        background_color='White',
                                        text_color="black"), 
                             
                            sg.Radio('ASCENDENTE', 
                                        "ascendente", 
                                        key='-ASCENDENTE-',
                                        font=OPCIONES3,
                                        background_color='White',
                                        text_color="black",
                                        circle_color=("light blue")),
                            sg.Radio('DESCENDENTE', 
                                        "ascendente", 
                                        key='-DESCENDENTE-',
                                        font=OPCIONES3,
                                        default=True,
                                        background_color='White',
                                        text_color="black",
                                        circle_color=("light blue")),sg.Push("white")], 
                          [sg.Push("white"), sg.Button("APLICAR CAMBIOS", 
                                        font=OPCIONES, 
                                        button_color=("black", "white"), 
                                        border_width=(5),
                                        pad=((0,0),(0,20)),
                                        key="-CAMBIO_ORDEN-"), sg.Push("white")],
      ]
        
      w = sg.Window("formulario", 
                        layout,
                        size=(1500,1500), 
                        border_depth=(1),
                        location=(-10,0), 
                        margins=(10,10), 
                        background_color=("white"), 
                        finalize=True)
      '''cambios aceptados me va a determinar si se producen cambios para abrir la pantalla de
      puntajes o no, de no ser aceptados retorna false para que vuelva a la pantalla menu'''
      cambios_aceptados=False
      tipo='puntos'
      orden='descendente'
      while True:
        event, values = w.read()
        if event == sg.WIN_CLOSED or event == "-PUNTAJES_VOLVER-":
            return(tipo,orden,cambios_aceptados)
        elif event == '-CAMBIO_ORDEN-':
            cambios_aceptados=True
            if values['-NOMBRE-']:
                tipo = 'nombre'
            elif values['-PUNTAJE-']:
                tipo = 'puntos'
            if values['-DESCENDENTE-']:
                orden= 'descendente'
            elif values['-ASCENDENTE-']:
                orden='ascendente'
            break
      w.Close()
      return tipo,orden,cambios_aceptados
      
def abrir_puntajes(tipo,orden):
    """Recibe partes de layout pertenecientes a la pantalla de puntajes, genera
    el layout completo y devuelve la ventana de puntajes"""
    
    
    layout_facil= logic_score.generar_layout("facil", COLOR3,tipo,orden)
    layout_normal= logic_score.generar_layout("normal", COLOR2,tipo,orden)
    layout_dificil= logic_score.generar_layout("dificil", COLOR1,tipo,orden)
    
    layout = [
        [                   sg.Button("Volver", 
                            font=OPCIONES, 
                            button_color=("black", "white"), 
                            border_width=(5),
                            pad=((0,0),(0,20)),
                            key="-PUNTAJES_VOLVER-"), sg.Push("white")],
                             
        [sg.Push("white"),
        sg.Frame(None, layout_dificil, background_color=("white"), border_width=8),
        sg.Frame(None, layout_normal, background_color=("white"), border_width=8),
        sg.Frame(None, layout_facil, background_color=("white"), border_width=8),
        sg.Push("white")],
    ]

    return sg.Window("FiguRace (Puntajes)", 
                        layout,
                        size=(1500,1500), 
                        border_depth=(1),
                        location=(-10,0), 
                        margins=(10,10), 
                        background_color=("white"), 
                        finalize=True)

