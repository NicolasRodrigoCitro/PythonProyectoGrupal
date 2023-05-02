from config import *
import json
import PySimpleGUI as sg

from src.functions import logicProfileScreen as prof_logic
from src.screens import profileScreen as prof_layout
from src.screens import menuScreen as menu_layout

def edad_permitida(texto_edad):
    """Procedimiento que determina si un texto recibido (edad, pantalla perfil) es numerico,
    y si lo es, devuelve true. en caso que no, devuelve false"""
    
    if texto_edad != " " and texto_edad.isdigit():  #los isdigit()método devuelve True si todos los los caracteres 
                                                    #son dígitos and texto_edad > 0 and texto_edad < 100
        return True  
    else:
        return False          
    

def modificacion_de_perfil(un_nombre, un_edad, un_genero):
    """procedimiento que abre el archivo de perfiles y permite modificarlos"""
    #Un llamado de atenicon, el with es un manejador de contexto, 
    #lo que cierra seria contenido pero se conserva jugadores como varible

    with open(DATA_FILE_PATH, "r") as contenido:
        jugadores = json.load(contenido)
    if not edad_permitida(un_edad):
        jugadores[un_nombre]['genero'] = un_genero
        sg.Popup("Perfil modificado satisfactoriamente", 
                button_color=("black", "white"), 
                font=OPCIONES2, background_color="black")
    else:
        jugadores[un_nombre]['edad'] = un_edad
        jugadores[un_nombre]['genero'] = un_genero
        sg.Popup("Perfil modificado satisfactoriamente", 
                button_color=("black", "white"), 
                font=OPCIONES2, background_color="black")
    with open(DATA_FILE_PATH, "w") as contenido:
        json.dump(jugadores, contenido, indent=4)


def crear_data_perfil_excepcion():
    """Procedimiento que crea un perfil 'unamed' (sin nombre) y lo guarda en
    el archivo de perfiles (si no existe lo crea)"""

    with open(DATA_FILE_PATH, "x") as archivo_perfiles:
        jugadores={}
        json.dump(jugadores, archivo_perfiles, indent=4)


def agregar_perfil_a_data(un_nombre, un_edad, un_genero):
    """Procedimiento que agrega un perfil al archivo de perfiles.
    Crea un diccionario con valores predeterminados (menos edad y genero) y los guarda en
    el archivo de perfiles
    """


    with open(DATA_FILE_PATH, "r") as data_file:
            jugadores = json.load(data_file)
    jugadores[f"{un_nombre}"] = {
                "edad": un_edad, 
                "genero": un_genero, 
                "tiempo_x_ronda": 40.0, 
                "rondas_x_juego": 15.0, 
                "suma_puntaje": 30.0,
                "resta_puntaje": 20.0, 
                "car_a_mostrar": 3.0,
                "partidas_jugadas": {"facil": 0.0,
                            "normal": 0.0,
                            "dificil": 0.0
                            },
                "puntajes": {"record_facil": 0.0,
                                "record_normal": 0.0,
                                "record_dificil": 0.0,
                                "total_facil": 0.0,
                                "total_normal": 0.0,
                                "total_dificil": 0.0,
                            }
                }
    with open(DATA_FILE_PATH, "w") as data_file:
            json.dump(jugadores, data_file, indent=4)

def agregar_perfil(un_nombre, un_edad, un_genero):
    """procedimiento que recibe parametros ingresados en la ventana perfil
    y los guarda como informacion de usuario en el archivo data.json'"""
    
    # with open(DATA_FILE_PATH, "r") as data_file:
    #     jugadores = json.load(data_file)
    # lista_nombres = [x['nombre'].lower() for x in jugadores['jugador']] #lista de los nombre de los jugadores

    lista_nombres = devolver_lista_perfiles()
    if un_nombre == "":
        sg.Popup("Ingrese un nick", 
                    button_color=("black", "white"), 
                    font=OPCIONES2, 
                    background_color="black")
    elif un_nombre == "vacio":
        sg.Popup("Nick no válido.\nPor favor ingrese otro", 
                    button_color=("black", "white"), 
                    font=OPCIONES2, 
                    background_color="black")
    elif un_nombre.lower() in lista_nombres:
        sg.Popup("Nick ya registrado. \nPor favor ingrese otro", 
                    button_color=("black", "white"), 
                    font=OPCIONES2, 
                    background_color="black")
    elif not edad_permitida(un_edad):
        sg.Popup("Ingrese una edad", 
                    button_color=("black", "white"), 
                    font=OPCIONES2, 
                    background_color="black")
    else:
        sg.Popup(f"Felicidades! A creado con exito su perfil.\n nombre '{un_nombre}' edad {un_edad} genero '{un_genero}'", 
                    button_color=("black", "white"), 
                    font=OPCIONES2, 
                    text_color="white",
                    background_color="black")
        agregar_perfil_a_data(un_nombre, un_edad, un_genero)
        #Cada vez que se crea un nuevo perfil, por defecto se asignan los valores de la dificultad 'normal' a la configuración personalizada de ese nuevo usuario  

         

def devolver_lista_perfiles():
    """procedimiento que abre el archivo donde se almacena la info. de usuarios"""

    with open(DATA_FILE_PATH, "r") as data_file:
        jugadores = json.load(data_file)
    return[nombres for nombres in jugadores]


def procesar_ventana_perfil(current_window, nombre_selecto):
    """Función que cierra la ventana de menú y abre la ventana de 
       configuración/edición de perfil manteniéndola abierta hasta 
       que se toque la cruz(WIN_CLOSED), el botón 'Abandonar juego' o
       el nombre de algún usuario ya registrado: En el primer caso se
       cerrará el juego por completo, en el segundo se volverá a 
       abrir la ventana de menú principal y en el tercero llamaremos 
       a la función 'abrir_segunda_ventana' del módulo 
       'profileScreen' y le pasaremos como argumento el perfil 
       elegido por el usuario. Si el usuario decide crearse un perfil
       nuevo, se guardarán los datos en variables y se pasarán como 
       argumentos a la función 'agregar_perfil' del módulo 
       'profileScreen' """
    current_window.close()
    prof_layout.abrir_perfil()
    while True:
        current_window, event, values = sg.read_all_windows()
 
        if event == sg.WIN_CLOSED:
            current_window.close()
            break
        elif event == 'Volver':
            current_window.close()
            return menu_layout.abrir_menu(nombre_selecto)
        elif event == 'Crear':
            un_nombre = values['-NOMBRE-']
            un_edad = values['-EDAD-']
            if values['-HOMBRE-']:
                un_genero = 'hombre'
            elif values['-MUJER-']:
                un_genero = 'mujer'
            else:
                un_genero = 'sin genero'
            prof_logic.agregar_perfil(un_nombre, un_edad, un_genero)
            prof_layout.abrir_perfil()
            current_window.close()

        if event == '-PERFIL-':
            current_window.close()
            prof_layout.abrir_segunda_ventana(values['-PERFIL-'])  # devuelve el nombre str