from config import *
from time import time
import json
import PySimpleGUI as sg
from ..functions import logicGeneric as gen_logic
from ..functions import logicConfigurationScreen as config_logic
from src.functions import logicGameScreen as game_logic
from src.functions import logicEvents as events_logic
from src.screens import gameScreen as game_layout
from src.screens import menuScreen as menu_layout
import random
import uuid


def inicializacion(dificultad_elegida):
    """Procedimiento que recibe la dificultad e inicializa variables correspondientes al juego.
    Devuelve diccionario con variables de configuracion, diccionario con imagenes y
    con datasets"""


    #cargo valores iniciales o utilies para el juego
    #abro los 3 csvs
    encabezado_fifa, datos_fifa = gen_logic.importador_csv("fifa_filtrado_pandas.csv")
    encabezado_spotify, datos_spotify = gen_logic.importador_csv("spotify_filtrado_pandas.csv")
    encabezado_lagos, datos_lagos = gen_logic.importador_csv("lagos_filtrado_pandas.csv")

    dicc_datasets = {"fifa": {"dataset": datos_fifa, "encabezado": encabezado_fifa}, 
                    "spotify": {"dataset": datos_spotify, "encabezado": encabezado_spotify}, 
                    "lagos": {"dataset": datos_lagos, "encabezado": encabezado_lagos}
    }

    dicc_imagenes = {
        "fifa": FIFA_IMG_FILE,
        "lagos": LAGO_IMG_FILE,
        "spotify": SPOTIFY_IMG_FILE
    }

    dificultad_seleccionada= config_logic.buscar_dificultad()

    dicc_config = {
        "dificultad": dificultad_elegida,
        "cant_rondas": int(dificultad_seleccionada["rondas_x_juego"]),
        "tiempo_por_ronda": dificultad_seleccionada["tiempo_x_ronda"],
        "ronda_actual": 1,
        "cant_caract": int(dificultad_seleccionada["car_a_mostrar"]),
        "puntaje_correcto": dificultad_seleccionada["suma_puntaje"],
        "puntaje_incorrecto": dificultad_seleccionada["resta_puntaje"],
        "suma_puntaje": 0
    }
    return dicc_datasets, dicc_imagenes, dicc_config


def choose_dataset(dicc_datasets):
    """Esta función recibe un diccionario de datasets y un diccionario de encabezados
    (correspondientes a dichos datasets) devuelve un dataset y una fila aleatoria (indice), con el elemento 'respuesta '
    de dicha fila en dicho dataset"""


    lista_datasets = [claves["dataset"] for nombres, claves in dicc_datasets.items()]

    dataset = random.choice ([lista_datasets[0], lista_datasets[1], lista_datasets[2]])      # "dataset" va a contener un dataset aleatorio


    if dataset == dicc_datasets["fifa"]["dataset"]:
        nombre_dataset = "Fifa"
        encabezado = dicc_datasets["fifa"]["encabezado"]
    elif dataset == dicc_datasets["lagos"]["dataset"]:
        nombre_dataset = "Lagos"
        encabezado = dicc_datasets["lagos"]["encabezado"]
    else:
        nombre_dataset = "Spotify"
        encabezado = dicc_datasets["spotify"]["encabezado"]

    fila = random.randrange (0,len(dataset))                                # selecciona un número de fila aleatoria del dataset 

    return dataset, fila, nombre_dataset, encabezado


def actualizar_ronda(dicc_config, estado_respuesta):
    """procedimiento que incrementa la cant de rondas llevadas a cabo
    si no son mayores a la cant. total"""
    if dicc_config["ronda_actual"] < dicc_config["cant_rondas"]:
        dicc_config["ronda_actual"] += 1
    else:
        dicc_config["ronda_actual"] = -1
    if estado_respuesta:
        dicc_config["suma_puntaje"] += dicc_config["puntaje_correcto"]
    else:
        dicc_config["suma_puntaje"] -= dicc_config["puntaje_incorrecto"]  
    return dicc_config


def crear_juego(dicc_datos_datasets):
    """procedimiento que toma un csv (elegido aleatoriamente en choose_dataset)
    y genera una respuesta correcta, cuatro incorrectas y una lista de respuestas"""
    
    sg.change_look_and_feel("LightGreen")
   
    dataset, fila_rta_correcta, nombre_dataset, encabezado = choose_dataset(dicc_datos_datasets)
    respuestas = [linea[5] for linea in dataset]

    respuestas = list(set(respuestas))
    respuestas.sort(key=str.lower)                                # "respuesta" contiene las soluciones posibles, ordenadas y sin repetir
    
    rta_correcta = dataset[fila_rta_correcta][5]
    options =  [(dataset[fila_rta_correcta][5])]                              #agrega la respuesta correcta a la lista "options"
    rtas_incorrectas = []
    while len(options) < 5 :
        nro = random.randrange (0,len(respuestas))
        if respuestas [nro] not in options:        #si el elemento de esa posicion, no estaba antes, lo guarda en options
            options.append (respuestas[nro])      #agrega la respuesta correcta a la lista options
            rtas_incorrectas.append(respuestas[nro])

    random.shuffle(options)
    random.shuffle(options)   

    return {"respuestas_incorrectas": rtas_incorrectas,
            "respuesta_correcta": rta_correcta, 
            "opciones": options, 
            "encabezado": encabezado, 
            "nombre_dataset": nombre_dataset, 
            "dataset": dataset, 
            "fila_rta_correcta": fila_rta_correcta
    }


def guardarData(puntaje, dificultad, nombre_perfil):
    """El procedimiento recibe la valores post-partida de un jugador y realiza
    actualizaciones en su estadisticas correspondientes"""

    with open(DATA_FILE_PATH, "r") as data_file:
        data = json.load(data_file)
    if dificultad != "personalizado":
        if data[nombre_perfil]["puntajes"][f"record_{dificultad}"] < puntaje:
            data[nombre_perfil]["puntajes"][f"record_{dificultad}"] = puntaje
        data[nombre_perfil]["partidas_jugadas"][dificultad] += 1
        data[nombre_perfil]["puntajes"][f"total_{dificultad}"] += puntaje


        with open(DATA_FILE_PATH, "w") as data_file:
            json.dump(data, data_file, indent=4)

def actualizar_layout(window, dicc_config, dicc_imagenes, dicc_datasets):

    dicc_juego= game_logic.crear_juego(dicc_datasets)
                    
    #actualizo text de dataset
    window["-DATASET-"].update(dicc_juego["nombre_dataset"])
    window["-IMAGEN-"].update(dicc_imagenes[dicc_juego["nombre_dataset"].lower()], size=(300, 200))
    #actualizo caracteristicas mostradas
    for i in range(dicc_config["cant_caract"]):
        window[f"-PISTA{i}-"].update(f'{dicc_juego["encabezado"] [i]} = {dicc_juego["dataset"][dicc_juego["fila_rta_correcta"]][i]}')
    #actualizo botones de opciones
    for i in range(5):
        window[f"-OPCION{i}-"].update(f'{dicc_juego["opciones"][i]}')
    window["-TIMER-"].update(str(int(dicc_config["tiempo_por_ronda"])))

    return dicc_juego


def procesar_ventana_juego(current_window, nombre_perfil, dificultad_elegida):
    """procedimiento que implementa el layout de la ventana juego, en la que se crea
    una nueva tarjeta cada vez que se termina el tiempo, se elige una opcion o se pasa
    hasta llegar a la cantidad de rondas especificada por la configuracion"""

    current_window.close()

    dicc_datasets, dicc_imagenes, dicc_config = game_logic.inicializacion(dificultad_elegida)

    tiempo_transcurrido = 0
    
    hora_inicio_ronda = time()                       #time me brinda la hora actual precisa
    hora_inicial = hora_inicio_ronda                #tomo la hora de inicio de la primera ronda para luego calcular tiempo total de partida

    #elijo dataset con el que voy a jugar la primera ronda
    dicc_juego= game_logic.crear_juego(dicc_datasets)

    #abro el layout
    window, myUUID = game_layout.abrir_juego(dicc_juego, nombre_perfil, dificultad_elegida, dicc_config)

    #registro de evento de inicio de partida
    events_logic.inicio_partida(myUUID, nombre_perfil, hora_inicial, dificultad_elegida)
    
    while True:
        event, values = window.read(timeout=300)
        if event == sg.WIN_CLOSED:
            window.close()
            break

        #bloque que actualiza el timer
        if event != sg.WIN_CLOSED and hora_inicial:
            tiempo_transcurrido = time() - hora_inicio_ronda              
            tiempo_restante = dicc_config["tiempo_por_ronda"] - tiempo_transcurrido

            if tiempo_restante > 0:                                         #si el tiempo restante es mayor a 0, actualiza el timer
                window["-TIMER-"].update(str(int(tiempo_restante)))     
            
            else:                                                           #si el tiempo restante es menor o igual a 0, pasa a la sig. tarjeta
                window["-TIMER-"].update("0")
                window[f'-RONDA{dicc_config["ronda_actual"]}-'].update(f'Ronda {dicc_config["ronda_actual"]}: INCORRECTO')
                
                sg.popup ("Se te acabó el tiempo...Resta puntos",
                            button_color=("white","grey"),
                                auto_close=True,
                                auto_close_duration=(2),
                                keep_on_top=True)
                
                dicc_config = game_logic.actualizar_ronda(dicc_config, False)

                #registro de evento caso: timeout
                events_logic.intento(myUUID, nombre_perfil, time(), "timeout", "-", dicc_juego["fila_rta_correcta"], dificultad_elegida)

                #bloque que reinicia la tarjeta y el timer
                if dicc_config["ronda_actual"] != -1:  
                    dicc_juego = game_logic.actualizar_layout(window, dicc_config, dicc_imagenes, dicc_datasets)                        
                    hora_inicio_ronda = time() 

            #bloque que se ejecuta cuando se llega al maximo de rondas (o sea termina la partida)
            if dicc_config["ronda_actual"] == -1:
                tiempo_partida = time() - hora_inicial

                #regsitro evento caso: fin de juego
                events_logic.fin(myUUID, nombre_perfil, time(), "finalizado", dificultad_elegida)
                if dificultad_elegida != "personalizado":
                    game_logic.guardarData(dicc_config["suma_puntaje"], config_logic.buscar_dificultad_por_nombre(), nombre_perfil)
                sg.popup(f'Juego finalizado. \n Puntaje: {int(dicc_config["suma_puntaje"])} \n Tiempo total: {int(tiempo_partida)} segundos \n presione OK para volver al menu',
                    button_color=("white","grey"),
                    keep_on_top=True)
                window.close()
                return menu_layout.abrir_menu(nombre_perfil)

            #bloque que analiza que evento se lleva a cabo

            #si se toca el boton de abandonar, se vuelve al menu
            if event == "-JUEGO_ABANDONAR-":
                sg.popup ("Abandonaste el juego \n(Tu puntaje no se tomará en cuenta)",
                            button_color=("white","grey"),
                            keep_on_top=True)
                
                #registro de evento caso: abandono de partida
                events_logic.fin(myUUID, nombre_perfil, time(), "abandonado", dificultad_elegida)

                window.close()
                return menu_layout.abrir_menu(nombre_perfil)

            #si es evento es otro, sera tocar una de las respuestas o el boton "pasar"
            else:
                #hubo_evento indica si se hubo un evento relacionado a una respuesta, asi puede
                #entrar al siguiente if y pasar de tarjeta
                hubo_evento = False
                
                #si se presiona 'pasar' se pasa a la siguiente tarjeta 
                if event == "-SIGUIENTE-":
                    
                    sg.popup("Se toma como respuesta incorrecta...Resta puntos",
                            button_color=("white","grey"),
                            auto_close=True,
                            auto_close_duration=(2),
                            keep_on_top=True)
                    hubo_evento = True
                    estado_respuesta = False
                    window[f'-RONDA{dicc_config["ronda_actual"]}-'].update(f'Ronda {dicc_config["ronda_actual"]}: INCORRECTO')

                    #registro evento caso: pasar de ronda
                    events_logic.intento(myUUID, nombre_perfil, time(), "error", "-", dicc_juego["respuesta_correcta"], dificultad_elegida)


                #si el evento es la rta correcta:          
                elif event.replace("-", " ").strip()[:-1] == "OPCION" and window[event].get_text() == dicc_juego["respuesta_correcta"]:

                    sg.popup ("Respuesta correcta!!",
                                    button_color=("white","grey"),
                                    auto_close=True,
                                    auto_close_duration=(2),
                                    keep_on_top=True)
                    hubo_evento = True
                    estado_respuesta = True
                    window[f'-RONDA{dicc_config["ronda_actual"]}-'].update(f'Ronda {dicc_config["ronda_actual"]}: CORRECTO')

                    #registro evento caso: respuesta correcta
                    events_logic.intento(myUUID, nombre_perfil, time(), "ok", window[event].get_text(), dicc_juego["respuesta_correcta"], dificultad_elegida)
                
                #si el evento es una rta incorrecta:
                elif event.replace("-", " ").strip()[:-1] == "OPCION" and window[event].get_text() in dicc_juego["respuestas_incorrectas"]:
                    sg.popup ("Respuesta incorrecta...Resta puntos",
                                button_color=("white","grey"),
                                auto_close=True,
                                auto_close_duration=(2),
                                keep_on_top=True)
                    hubo_evento = True
                    estado_respuesta = False
                    window[f'-RONDA{dicc_config["ronda_actual"]}-'].update(f'Ronda {dicc_config["ronda_actual"]}: INCORRECTO')

                    #registro evento caso: respuesta incorrecta
                    events_logic.intento(myUUID, nombre_perfil, time(), "error", window[event].get_text(), dicc_juego["respuesta_correcta"], dificultad_elegida)
                
                #bloque que actualiza el layout si hubo algun evento (boton pasar o boton respuesta)
                if hubo_evento:
                    dicc_juego = game_logic.actualizar_layout(window, dicc_config, dicc_imagenes, dicc_datasets)
                    dicc_config = game_logic.actualizar_ronda(dicc_config, estado_respuesta)
                    hora_inicio_ronda = time() 


