import Controlador, ControladorMP
import os
import sys
from Color import Color
from random import random

''' LINJA

Autor: Álvar Gómez Cuesta
Asignatura: Sistemas Inteligentes

Objetivo: programar una IA contra la que jugar al Linja.
Lenguaje: Python

Github: 
'''


intro = '''
█████████████████████████████████████████████████████
█               BIENVENIDO AL LINJA                 █
█                                                   █
█ Opciones:                                         █
█   1 - Jugar 1 vs 1                                █
█   2 - Jugar 1 vs IA (mononucleo)                  █
█   3 - Jugar 1 vs IA (multinucleo)                 █   
█   4 - Mostrar reglas                              █   
█   5 - Salir                                       █
█                                                   █
█████████████████████████████████████████████████████
'''

reglas1 = '''
█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
█                                                       REGLAS DE JUEGO                                                     █
█                                                                                                                           █
█  En su turno cada jugador realiza dos movimientos, conocidos como movimiento inicial y segundo movimiento.                █
█                                                                                                                           █
█  En su movimiento inicial el jugador debe mover una de sus fichas exactamente una casilla hacia delante.                  █
█                                                                                                                           █
█  El número de fichas presentes en la casilla a la que ha desplazado la ficha (sin contar ésta) determinará el número de   █
█  casillas que podrá mover una ficha el jugador en su segundo movimiento. Es decir, si en su movimiento inicial el jugador █ 
█  desplazó una ficha a una casilla que ya contenía tres fichas, en su segundo movimiento podrá mover una ficha tres        █
█  casillas hacia delante.                                                                                                  █
█                                                                                                                           █
█  Dos aclaraciones: las fichas desplazadas en ambos movimientos pueden o no ser la misma; y si en su movimiento inicial    █
█  un jugador movió una ficha a una casilla vacía perderá el derecho a su segundo movimiento y deberá pasar turno (algo     █
█  lógico, pudiendo entenderse como que su segundo movimiento ha sido de cero casillas).                                    █
█                                                                                                                           █
█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
█ 2 - Turno extra   █ 3 - Excepciones   █ 0 - Salir'''

reglas2 = '''
█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
█                                                REGLAS DE JUEGO - TURNO EXTRA                                              █
█                                                                                                                           █
█  Si en su segundo movimiento un jugador desplaza una ficha a una casilla vacía, dicho jugador obtendrá un turno extra     █
█  completo (consistente en otro movimiento inicial y otro segundo movimiento).                                             █
█                                                                                                                           █
█  Si en su turno extra el jugador desplaza de nuevo en su segundo movimiento una ficha a una casilla vacía no tendrá       █ 
█  derecho a otro turno extra y deberá pasar turno. Es decir, no pueden concatenarse dos turnos extra seguidos del mismo    █ 
█  jugador.                                                                                                                 █
█                                                                                                                           █
█  Es interesante recalcar cómo si un jugador mueve a una casilla vacía en su movimiento inicial pierde su segundo          █
█  movimiento; pero si hace lo mismo en su segundo movimiento es premiado con un turno extra.                               █
█                                                                                                                           █
█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
█ 1 - Reglas generales   █ 3 - Excepciones   █ 0 - Salir'''

reglas3 = '''
█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
█                                                REGLAS DE JUEGO - EXCEPCIONES                                              █
█                                                                                                                           █
█  El número máximo de fichas que puede haber en una casilla intermedia es de seis. Si una de estas casillas está completa  █
█  ningún jugador puede desplazar una ficha a ellas pero sí puede pasar a través de ellas. Las dos casillas de los extremos █ 
█  no tienen limitación en el número de fichas que pueden contener.                                                         █
█                                                                                                                           █
█  Si en su movimiento inicial un jugador desplaza su ficha a la casilla del extremo opuesto, su segundo movimiento         █
█  constará únicamente de un solo punto (es decir, no se tendrán en cuenta el número de fichas presentes en la casilla      █
█  final para determinar los puntos de movimiento).                                                                         █
█                                                                                                                           █
█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
█ 1 - Reglas generales   █ 2 - Turno extra   █ 0 - Salir'''

jvsj = '''
█████████████████████████████████████████████████████
█            ELECCION DEL TURNO INICIAL             █
█                                                   █
█ Opciones:                                         █
█   1 - Jugador ROJO comienza                       █
█   2 - Jugador NEGRO comienza                      █
█   3 - Aleatorio                                   █
█   4 - Volver atras                                █
█                                                   █
█████████████████████████████████████████████████████
'''

ajustes = '''
█████████████████████████████████████████████████████
█                     AJUSTES                       █
█                                                   █
█  Introduzca la profundidad maxima de exploracion  █
█  que desea (1-3 para un rendimiento correcto)     █
█                                                   █
█████████████████████████████████████████████████████
'''
aviso_mp = '''
█████████████████████████████████████████████████████
█                      AVISO                        █
█                                                   █
█  Este modo de juego usará todos los recursos de   █
█  su ordenador.                                    █
█                                                   █
█████████████████████████████████████████████████████
'''
def main():
    '''Funcion principal que inicia la ejecucion del programa
    
    Hace una limpieza de la pantalla y muestra un menu con las opciones
    disponibles. Estas son:
        Empezar partida
        Mostrar reglas
        Salir del juego
    '''
    while(True):
        os.system('cls')
        print(intro)
        key = input("█ Introduce la opción que quieras ejecutar: ")
        match(key):
            case "1":
                jugar1()
            case "2":
                jugar2()
            case "3":
                jugar3()
            case "4":
                reglas()
            case "5":
                exit()

def jugar1():
    '''Bucle que comienza la ejecucion de la partida
    
    Modo de juego jugador contra jugador
    
    Se mostrará un mensaje inicial para elegir el jugador que empieza
    la partida y posterior mente se iniciará el bucle while sobre el
    que se jugará la partida.
    '''
    os.system('cls')
    print(jvsj)
    key = input_data(1,3, "█ Introduce la opción que quieras ejecutar: ")
    AI = ControladorMP.controlador(key)
    match(key):
        case 1:
            AI = ControladorMP.controlador(Color.RED)
        case 2:
            AI = ControladorMP.controlador(Color.BLACK)
        case 3:
            num = round(random())
            if num == 0:
                AI = ControladorMP.controlador(Color.RED)
            elif num == 1:
                AI = ControladorMP.controlador(Color.BLACK)
    try:
        while(True):
            os.system('cls')
            AI.imprimir_tablero()
            AI.imprimir_puntuacion()
            AI.seleccionar_movimiento(1,1)
            if AI.comprobar_fin(AI.Tb):
                os.system('cls')
                AI.imprimir_tablero()
                AI.imprimir_puntuacion()
                if AI.calcular_puntuacion_rojas(AI.Tb) < AI.calcular_puntuacion_negras(AI.Tb):
                    print("El jugador NEGRO ha ganado la partida. Enhorabuena\n")
                elif AI.calcular_puntuacion_rojas(AI.Tb) > AI.calcular_puntuacion_negras(AI.Tb):
                    print("El jugador ROJO ha ganado la partida. Enhorabuena\n")
                else:
                    print("La partida ha acabado en empate. Enhorabuena a los dos jugadores")
                exit()
            AI.cambiar_turno()
    except Exception:
        print(f"El jugador {AI.turno.__str__()} ha perdido la partida por quedarse sin movimientos.\n")
        exit()


def jugar2():
    '''Bucle que comienza la ejecucion de la partida
    
    Modo de juego contra la IA usando un solo hilo para la exploracion.

    Se muestra un mensaje inicial, y posteriormente dentro del bucle
    while se ejecutan las acciones:
        Mostrar tablero
        Mostrar puntuacion
        Dar la opcion al jugador de seleccionar el movimiento que desea realizar
    '''
    os.system('cls')
    print(ajustes)
    key = input_data(1,5,"Introduce la profundidad maxima que deseas: ")
    AI = Controlador.controlador()
    while True: 
        os.system('cls')
        AI.imprimir_tablero()
        AI.imprimir_puntuacion()
        AI.seleccionar_movimiento(1,key,1)
        if AI.comprobar_fin(AI.Tb):
            AI.imprimir_tablero()
            AI.imprimir_puntuacion()
            if AI.calcular_puntuacion_rojas(AI.Tb) < AI.calcular_puntuacion_negras(AI.Tb):
                print("El jugador NEGRO ha ganado la partida. Enhorabuena\n")
            elif AI.calcular_puntuacion_rojas(AI.Tb) > AI.calcular_puntuacion_negras(AI.Tb):
                print("El jugador ROJO ha ganado la partida. Enhorabuena\n")
            else:
                print("La partida ha acabado en empate. Enhorabuena a los dos jugadores")
            exit()
        AI.cambiar_turno()

def jugar3():
    '''Bucle que comienza la ejecucion de la partida
    
    Modo de juego contra la IA usando todos los nucleos del procesador.
    
    Se muestra un mensaje inicial, y posteriormente dentro del bucle
    while se ejecutan las acciones:
        Mostrar tablero
        Mostrar puntuacion
        Dar la opcion al jugador de seleccionar el movimiento que desea realizar
    '''
    os.system('cls')
    print(ajustes)
    key = input_data(1,5,"Introduce la profundidad maxima que deseas: ")
    AI = ControladorMP.controlador()

    while True: 
        os.system('cls')
        AI.imprimir_tablero()
        AI.imprimir_puntuacion()
        AI.seleccionar_movimiento_IA(1,key,1)
        if AI.comprobar_fin(AI.Tb):
            #os.system('cls')
            AI.imprimir_tablero()
            AI.imprimir_puntuacion()
            if AI.calcular_puntuacion_rojas(AI.Tb) < AI.calcular_puntuacion_negras(AI.Tb):
                print("El jugador NEGRO ha ganado la partida. Enhorabuena\n")
            elif AI.calcular_puntuacion_rojas(AI.Tb) > AI.calcular_puntuacion_negras(AI.Tb):
                print("El jugador ROJO ha ganado la partida. Enhorabuena\n")
            else:
                print("La partida ha acabado en empate. Enhorabuena a los dos jugadores")
            exit()
        AI.cambiar_turno()

def reglas():
    '''Muestra las reglas de la partida

    Se muestran las reglas de juego y se puede rotar sobre diferentes 
    menus mediante la pulsacion de los botones correspondientes
    '''
    os.system('cls')
    print(reglas1)
    while(True):
        key = input()
        match(key):
            case "0":
                os.system('cls')
                return
            case "1": 
                os.system('cls')
                print(reglas1)
            case "2": 
                os.system('cls')
                print(reglas2)
            case "3":
                os.system('cls')
                print(reglas3)
        
def input_data(min: int, max: int, mesg: str = None) -> int:
        '''Pregunta por un valor al usuario dentro de unos limites
        
        Se asegura de que el valor introducido por teclado se
        encuentra comprendido entre min y max y lo devuelve.
        
        Args:
            min (int):
                Valor minimo que debe tener la entrada.
            max (int):
                Valor maximo que debe tener la entrada.
            mesg (str):
                Mensaje a mostrar cuando se pida la entrada por teclado
        Returns:
            key (int):
                Valor introducido por teclado.
        '''
        while(True):
            
            try:
                if mesg != None:
                    key = int(input(mesg))
                if min<=key<=max:
                    return key
                else:
                    print(f"Introduce un número entre {min} y {max}, ambos incluidos")
            except(KeyboardInterrupt):
                exit()
            except(ValueError):
                pass
    
if __name__ == "__main__":
    main()