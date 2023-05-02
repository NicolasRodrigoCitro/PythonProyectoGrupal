from config import *
import csv
import os
import PySimpleGUI as sg


def agregar_fila(timestamp, myUUID, evento, usuario, estado, texto_ingresado, respuesta, nivel):
    """Procedimiento que agrega una fila al csv de eventos con los elementos recibidos como parametros
    si el archivo no esta vacio y existe. Si está vacio, primero agrega el encabezado. Si no existe
    lo crea, agrega el encabezo y la nueva linea
    
    El primer open va con a+ para que se cree si no existe, el segundo con a para agregar
    """

    fila_nueva = [timestamp, myUUID, evento, usuario, estado, texto_ingresado, respuesta, nivel]
    # si existe                                        y tiene dato
    if (os.path.exists(DATA_FILE_EVENTO_PATH)) and (os.stat(DATA_FILE_EVENTO_PATH).st_size > 0):    #os.stat toma el status de un archivo y .st_size el tamaño del mismo
        #si el archivo existe y tiene informacion agrega una linea                                                                                
        with open(DATA_FILE_EVENTO_PATH, "a", encoding="utf-8", newline = "") as archivo:
            writer = csv.writer(archivo, delimiter=',')
            writer.writerow(fila_nueva)
    else:
        #si el archivo no existe, o esta vacio, se crea el encabezado y se agrega la nueva fila
        with open(DATA_FILE_EVENTO_PATH, "a+", encoding="utf-8", newline = "")as archivo:
            encabezado = ["timestamp","id","evento","usuarie","estado","texto ingresado","respuesta","nivel"]
            writer = csv.writer(archivo, delimiter=',')
            writer.writerow(encabezado)
            writer.writerow(fila_nueva)
        

def inicio_partida(myUUID,un_perfil,un_timestamp,un_nivel):
    evento = "inicio_partida"
    estado=""
    texto_ingresado=""
    respuesta=""
    agregar_fila(un_timestamp, myUUID, evento, un_perfil, estado, texto_ingresado, respuesta, un_nivel)


def intento(myUUID, usuario, timestamp, estado, texto_ingresado, respuesta, nivel):
    """Se reciben los datos por parametros en este caso se completan todos los datos
    En el caso de estado los posibles valores son: “error”, “ok” o “timeout”.
    Si no es ninguno, aparecerá un popup mostrando un error
    """

    evento = "intento"
    if estado == 'error' or estado=='ok' or estado =='timeout':
        agregar_fila(timestamp, myUUID, evento, usuario, estado, texto_ingresado, respuesta, nivel)
    else:
        sg.Popup("Hay un error en la carga de datos, comuníquese con el programador",
                 button_color=("black", "white"),
                 font=OPCIONES2,
                 background_color="black")

def fin(myUUID, usuario, timestamp, estado, nivel):
    """Procedimiento encargado de mandar al csv de eventos la información del evento de fin
    Si no es ninguno, aparecerá un popup mostrando un error
    """
    evento = "fin"
    texto_ingresado = "-"
    respuesta = "-"
    #Se guardar una nueva fila en este caso el estado puede ser “finalizada” o “cancelada”.
    if estado == 'finalizado' or estado == 'abandonado':
        agregar_fila(timestamp, myUUID, evento, usuario, estado, texto_ingresado, respuesta, nivel)
    else:
        sg.Popup("Hay un error en la carga de datos, al cerrar el juego, comuníquese con el programador",
                 button_color=("black", "white"),
                 font=OPCIONES2,
                 background_color="black")