from Color import Color
from copy import deepcopy
from typing import Any, Optional
GLOBAL_WIDTH = 6
GLOBAL_HEIGHT = 8
class Tablero:
    '''Clase que representa el tablero de juego

    Attributes:
        casillas (list): array bidimensional que representará el tablero
    '''

    def __init__(self) -> None:
        '''Inicializa el tablero y pone todas las casillas a 0'''
        self.casillas = [[0 for i in range(GLOBAL_WIDTH)] for j in range(GLOBAL_HEIGHT)]
        self.extremo_black = []
        self.extremo_red = []

    def __str__(self) -> str:
        '''Genera una representacion visual del tablero actual
        
        Returns:
            empty (str): 
                String que contiene el tablero en forma visual
        '''
        empty = f"Extremo rojas -> {len(self.extremo_black)} x \033[90m█\033[0m \n" 
        empty += "   ┌" + ("─"*3 + "┬")*(GLOBAL_WIDTH-1) + "───┐   \n"
        temp = 1
        ptL = [5,3,2,1,1,2,3,5]
        for i in self.casillas:
            empty += f" {temp-1} │"
            if temp != GLOBAL_HEIGHT:
                for j in i:
                    if j != None:
                        if j == 2 :
                            empty += (f" \033[90m{j}\033[0m │")
                        elif j == 1:
                            empty += (f" \033[91m{j}\033[0m │")
                        else:
                            empty += (f"   │")
                    else:
                        empty += ("   │")
                empty += str(" " + str(ptL[temp-1]) + " pt ")
                empty += "\n   ├" + ("═"*3 + "┼")*(GLOBAL_WIDTH-1) + "═══┤   \n" 
                temp += 1
            else: 
                for j in i:
                    if j != None:
                        if j == 2:
                            empty += (f" \033[90m{j}\033[0m │")
                        elif j == 1:
                            empty += (f" \033[91m{j}\033[0m │")
                        else:
                            empty += (f"   │")
                    else:
                        empty += ("   │")
                empty += str(" " + str(ptL[temp-1]) + " pt ")
        empty += "\n   └" + ("─"*3 + "┴")*(GLOBAL_WIDTH-1) + "───┘   \n"
        empty += "    0   1   2   3   4   5      \n"
        empty += "\033[0m"
        empty += f"Extremo rojas -> {len(self.extremo_red)} x \033[91m█\033[0m \n" 
        return empty
    
    def rellenar_tablero(self):
        '''Rellena el tablero incial con las piezas en sus posiciones iniciales de partida'''
        #Relleno Negras
        iniPosBlack = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0)]

        #Relleno Blancas
        iniPosRed = [(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(6,5),(5,5),(4,5),(3,5),(2,5),(1,5)]

        for i in iniPosBlack:
            self.casillas[i[0]][i[1]] = 2
        for j in iniPosRed:
            self.casillas[j[0]][j[1]] = 1
    
    def devolver_posicion_negras(self) -> list:
        '''Genera una lista con las posiciones de las piezas negras del tablero actual y las devuelve
        
        Returns:
            temp (list): 
                Lista con las posiciones de las piezas negras del tablero
        '''
        temp = []
        for i in range(8):
            for j in range(6):
                if self.casillas[i][j] == 2:
                    temp.append([i,j])
        return temp
    
    def devolver_posicion_rojas(self) -> list:
        '''Genera una lista con las posiciones de las piezas rojas del tablero actual y las devuelve
        
        Returns:
            temp (list): 
                Lista con las posiciones de las piezas rojas del tablero
        '''
        temp = []
        for i in range(8):
            for j in range(6):
                if self.casillas[i][j] == 1:
                    temp.append([i,j])
        return temp
    
    def get_num_piezas_fila(self, fila) -> int:
        '''Devuelve el numero de piezas que se encuentran en una fila 

        Args:
            fila (int): 
                Fila que se quiere consultar
        
        Returns:
            num (int): 
                numero de piezas en la fila solicitada
                *Devuelve None si la fila no pertenece al tablero
        '''
        num = 0
        if fila < 0 or fila > 7:
            return None
        if fila == 0 or fila == 7:
            return 1
        try:
            for i in self.casillas[fila]: 
                if i != 0: 
                    num+=1
            return num
        except(IndexError):
            return None
    
    def mover_pieza(self,pieza:list, num: int , turno: Color) -> int:
        '''Mueve una pieza determinada un numero determinado de posiciones
        
        Args:
            pieza (list): 
                Posiciones de la pieza que se va a querer mover
            num (int): 
                Numero de movimientos que se quiere mover la pieza
            turno (Color): 
                Color de la pieza que se va a mover
        
        Returns:
            new_row (int): 
                Fila a la que se ha movido la pieza
        '''
        self.casillas[pieza[0]][pieza[1]] = 0
        if turno == Color.RED:
            num_jugador = 1
            new_row = pieza[0] - num
        else: 
            num_jugador = 2
            new_row = pieza[0] + num
        
        contador = 0
        if new_row == 0:
            self.extremo_black.append(1)
            return 0
        if new_row == 7:
            self.extremo_red.append(2)
            return 7
        for i in self.casillas[new_row]:
            if i == 0: 
                self.casillas[new_row][contador] = num_jugador
                return new_row
            contador+=1
        