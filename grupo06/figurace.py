import PySimpleGUI as sg

#importa constantes y rutas.
from config import *

#importa modulos de logica
from src.functions import logicConfigurationScreen as config_logic
from src.functions import logicGameScreen as game_logic
from src.functions import logicProfileScreen as prof_logic
from src.functions import logicScoreScreen as score_logic

#import modulo de layout
from src.screens import menuScreen as menu_layout

                  
def main():
    nombre_perfil = "Elija un perfil"
    dificultad_elegida = config_logic.buscar_dificultad_por_nombre()
    hubo_eleccion = False
    
    menu_layout.abrir_menu(nombre_perfil)

    while True:
        current_window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED:
            break
        match event:
            case "Jugar": game_logic.procesar_ventana_juego(current_window, nombre_perfil, dificultad_elegida) if hubo_eleccion else sg.popup ("Debe elegir un perfil para jugar",
                                                                                                                button_color=("white","grey"),
                                                                                                                keep_on_top=True)
            case "Configuracion": config_logic.procesar_ventana_config(current_window, nombre_perfil) if hubo_eleccion else sg.popup ("Primero elija un perfil",
                                                                                                                button_color=("white","grey"),
                                                                                                                keep_on_top=True)
            case "Puntajes": score_logic.procesar_ventana_puntajes(current_window, nombre_perfil)
            case "Perfil": prof_logic.procesar_ventana_perfil(current_window, nombre_perfil)
            case "Salir": break
            case "-FACIL-": 
                config_logic.cambiar_dificultad("facil") 
                dificultad_elegida = "facil"
            case "-NORMAL-": 
                config_logic.cambiar_dificultad("normal")
                dificultad_elegida = "normal"
            case "-DIFICIL-": 
                config_logic.cambiar_dificultad("dificil")
                dificultad_elegida = "dificil"
            case "-PERSONALIZADO-": 
                config_logic.cambiar_dificultad ("personalizado")
                dificultad_elegida = "personalizado"
                if hubo_eleccion: 
                    config_logic.procesar_ventana_config(current_window, nombre_perfil)
                else:
                    sg.Popup("Seleccione un perfil para jugar", button_color=("white","grey"),keep_on_top=True)            
            case "-PERFIL_SELECTO-": 
                hubo_eleccion = True
                nombre_perfil = values["-PERFIL_SELECTO-"]
                config_logic.cargar_personalizado(nombre_perfil)

if __name__ == "__main__":
    main()