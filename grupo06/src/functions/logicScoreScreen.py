import json
import operator
from tkinter import W
import PySimpleGUI as sg

from config import *
from src.screens import scoreScreen as score_layout
from src.screens import menuScreen as menu_layout


def generar_linea(usu, pts):
    """Retorna un objeto 'Text' de PySimpleGUI que contendrá el
    usuario y sus respectivos puntos pasados por parámetro"""
    
    color = "red" if usu == "vacío" else "white" 
    return [sg.Text((f'{pts} {usu}'), 
        text_color=color,
        font = OPCIONES,
        background_color='black', 
        size=(18,1),
        pad=((0,0),(0,0)))]


def generar_encabezado(texto, color):
    """Retorna un objeto 'Text' de PySimpleGUI con el texto y el 
    color pasados por parámetro"""
    
    return [[sg.Text(texto, 
        font= OPCIONES, 
        background_color=color)]]  
def ordenar_por_criterios(un_diccionario,tipo,orden):
    match tipo:
        case "nombre":  un_diccionario = dict(sorted(un_diccionario.items(),key=operator.itemgetter(0), reverse= True)) if orden == 'descendente' else dict(sorted(un_diccionario.items(),key=operator.itemgetter(0), reverse= False))
        case "puntos": un_diccionario = dict(sorted(un_diccionario.items(),  key=operator.itemgetter(1), reverse= True)) if orden == 'descendente' else dict(sorted(un_diccionario.items(),key=operator.itemgetter(1), reverse= False))
    return un_diccionario
def extraer_listas_con_claves_valores(un_diccionario):
    usuarios = [jugador for jugador in un_diccionario]
    puntos= [puntaje for puntaje in un_diccionario.values()]
    return usuarios,puntos
def generar_lista_puntajes(dificultad,tipo,orden):
    """Retorna las listas con los puntajes mayores y los promedio 
    mayores junto con sus respectivos usuarios. ordenados por los criterios de tipo y orden
    seleccionando a lo sumo 20 de los perfiles"""

    #guardo en un puntajes clave nombre, valor puntaje, de todos los jugadores
    puntajes=puntajes_mayores(dificultad)
    promedio= puntajes_promedio(dificultad)
    #lo separo en listas con la idea de acotarlos
    usuarios , puntos = extraer_listas_con_claves_valores(puntajes)
    usuarios_promedio,puntos_promedio =extraer_listas_con_claves_valores(promedio)
   
    '''paso a extraer si son mas de 20 jugadores, los mejores 20, acotando la lista'''
    if len(usuarios) > CANT_PTS_MOSTRAR:
        usuarios =  usuarios[0:CANT_PTS_MOSTRAR]
        puntos = puntos[0:CANT_PTS_MOSTRAR]
        usuarios_promedio = usuarios_promedio[0:CANT_PTS_MOSTRAR ]
        puntos_promedio = puntos_promedio[ 0:CANT_PTS_MOSTRAR]
    else: #sino me traigo los elementos que tengan,  para al final rellenar con 'vacio'
        usuarios =  usuarios[0:len(usuarios)]
        puntos = puntos[0:len(usuarios)]
        usuarios_promedio=usuarios_promedio[0:len(usuarios)]
        puntos_promedio=puntos_promedio[0:len(usuarios)]

    #transformo las listas acotadas a un diccionario para poder ordenarlos
    jugadores = dict(zip(usuarios,puntos))
    jugadores=ordenar_por_criterios(jugadores,tipo,orden)
    # para los promedios
    jugadores_promedios = dict(zip(usuarios_promedio,puntos_promedio))
    jugadores_promedios= ordenar_por_criterios(jugadores_promedios,tipo,orden)
    '''jugadores es un diccionario que ya esta ordenado segun los parametros pedidos'''

    # extraigo las listas con los nombres usuarios, y los puntos
    usuarios , puntos = extraer_listas_con_claves_valores(jugadores)
    usuarios_promedio,puntos_promedio =extraer_listas_con_claves_valores(jugadores_promedios)
    
    # relleno espacios
    if (len(usuarios)<CANT_PTS_MOSTRAR):
        usuarios_promedio.extend(["vacío"]*(CANT_PTS_MOSTRAR - len(usuarios_promedio)))
        puntos_promedio.extend([0]*(CANT_PTS_MOSTRAR - len(puntos_promedio)))
        
        usuarios.extend(["vacío"]*(CANT_PTS_MOSTRAR - len(usuarios)))
        puntos.extend([0]*(CANT_PTS_MOSTRAR - len(puntos)))

    return usuarios, puntos, usuarios_promedio, puntos_promedio



def generar_columna(columna, usuarios, puntos):
    """Retorna una lista que contendrá el encabezado y lineas con los
    puntos y sus repectivos usuarios"""

    columna.extend(list(map(generar_linea, usuarios, puntos)))

    return columna


def generar_layout (dificultad, color, tipo, orden):
    """Retorna el layout correspondiente a la dificultad pasada como
    parámetro"""

    columna_pj_mas_alto = generar_encabezado('Puntajes Mayores', color)
    columna_pj_prom = generar_encabezado('Puntajes Promedio', color)

    usuarios, puntos, usuarios_prom, puntos_prom= generar_lista_puntajes(dificultad,tipo,orden)

    columna_pj_mas_alto= generar_columna (columna_pj_mas_alto, usuarios, puntos)
    columna_pj_prom= generar_columna (columna_pj_prom, usuarios_prom, puntos_prom)

    layout= [
        [sg.Push("white"), sg.Text(dificultad,font=OPCIONES3, text_color=("black"), 
        background_color=("white")),sg.Push("white")],
        [sg.Column(columna_pj_mas_alto, background_color=color,key=(f'-COLUMNA_PUNTAJES-{dificultad.upper()}')),
        sg.Column(columna_pj_prom, background_color=color,key=(f'-COLUMNA_PUNTAJES_PROMEDIO-{dificultad.upper()}'))]
    ]

    return layout



def puntajes_mayores (dificultad):
    """Devuelve un diccionario ordenado en forma descendente con los
    jugadores como claves y sus puntajes mayores como valores de la 
    dificultad pasada por parámetro"""

    with open (DATA_FILE_PATH, "r") as data_file:
        datos_perfiles= json.load(data_file)
    puntajes= {jugador.lower():int(datos["puntajes"][f"record_{dificultad}"]) for jugador, datos in datos_perfiles.items()}
   
    return dict(sorted(puntajes.items(),  key=operator.itemgetter(1), reverse= True))


def puntajes_promedio (dificultad):
    """Devuelve un diccionario ordenado en forma descendente con los
    jugadores como claves y sus puntajes promedio como valores de la
    dificultad pasada por parámetro"""

    with open (DATA_FILE_PATH, "r") as data_file:
        datos_perfiles= json.load(data_file)
    puntajes_prom= {jugador.lower():int(datos["puntajes"][f"total_{dificultad}"]/datos["partidas_jugadas"][f"{dificultad}"]) if datos["partidas_jugadas"][f"{dificultad}"]> 0 else 0 for jugador, datos in datos_perfiles.items()} 
    #Es necesario el if/else ya que en caso de que el usuario no tenga partidas jugadas se haría una división por cero ("ZeroDivisionError")

    return dict(sorted(puntajes_prom.items(),  key=operator.itemgetter(1), reverse= True)) 


def procesar_ventana_puntajes(current_window, nombre_selecto):
    """Función que cierra la ventana de menú y abre la ventana de 
       puntajes manteniéndola abierta hasta que se toque la cruz
       (WIN_CLOSED) o el botón 'Volver':  en el primer caso el juego
       se cerrará por completo y en el segundo se volverá a 
       abrir la ventana del menú principal"""
       
    current_window.close()
    tipo ,orden,cambios_aceptados = score_layout.abrir_formulario(nombre_selecto)
    if(cambios_aceptados):
        window = score_layout.abrir_puntajes(tipo,orden)
        while True:
            current_window, event, values = sg.read_all_windows()
            if event == sg.WIN_CLOSED:
                current_window.close()
                break
            elif event == "-PUNTAJES_VOLVER-":
                current_window.close()
                return menu_layout.abrir_menu(nombre_selecto)
    else:
        return menu_layout.abrir_menu(nombre_selecto)
        
