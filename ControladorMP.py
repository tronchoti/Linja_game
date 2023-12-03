from Tablero import Tablero
from Color import Color
import time
import multiprocessing
from copy import deepcopy
import math


class controlador:
    '''Clase que contiene el "arbitro" de la partida, que se encargara
    de controlar el correcto funcionamiento de esta.

    Attributes:
        alpha (int): valor de alpha
        beta (int): valor de beta
        Tb (Tablero): tablero de la partida
        turno (Color): color del turno actual
        num_recur (int): recursividad de la exploracion actual
    '''

    def __init__(self, turno: Color = Color.RED) -> None:
        '''Inicializa el Controlador de la partida

        Crea un tablero nuevo y lo rellena con las posiciones
        iniciales de la partida.

        Establece las variables alpha y beta a menosinfinito 
        y mas infinito respectivamente.

        Args:
            turno (Color):
                Color del jugador que tendrá el turno inicial
        '''
        self.Tb = Tablero()
        self.Tb.rellenar_tablero()
        self.alpha = -math.inf
        self.beta = math.inf
        self.turno = turno
        self.num_recur = 0
    
    def imprimir_tablero(self) -> None:
        '''Muestra por pantalla el tablero de la partida'''
        print(self.Tb.__str__())
    
    def imprimir_puntuacion(self) -> None:
        '''Muestra por pantalla la puntuacion de cada jugador

        Calcula la puntuacion de cada jugador por separado y 
        posteriormente formatea el resultado en una string,
        en la cual se incluye tambien el turno acutal.
        '''
        points_red = self.calcular_puntuacion_rojas(self.Tb)
        points_black = self.calcular_puntuacion_negras(self.Tb)
        str_puntuacion = "█ Rojo: {0}\n█ Negro: {1}\n█ Turno: {2}".format(points_red, points_black, self.turno)
        print(str_puntuacion)

    def calcular_puntuacion_rojas(self, tablero: Tablero) -> int:
        '''Calcula la puntuacion de las piezas rojas

        Solicita las posiciones de las piezas rojas del tablero
        y calcula la puntuacion.
        
        Args:
            tablero (Tablero): tablero del que se obtendran las piezas
            
        Returns:
            points_red (int): puntos piezas rojas
        '''
        points_red = 0
        for j in tablero.devolver_posicion_rojas():
            match(j[0]):
                case 0: points_red+=5
                case 1: points_red+=3
                case 2: points_red+=2
                case 3: points_red+=1
        for i in tablero.extremo_black:
            points_red+=5
        return points_red

    def calcular_puntuacion_negras(self, tablero: Tablero) -> int:
        '''Calcula la puntuacion de las piezas negras

        Solicita las posiciones de las piezas negras del tablero
        y calcula la puntuacion.
        
        Args:
            tablero (Tablero): tablero del que se obtendran las piezas
            
        Returns:
            points_black (int): puntos piezas negras
        '''
        points_black = 0
        for i in tablero.devolver_posicion_negras():
            match(i[0]):
                case 4: points_black+=1
                case 5: points_black+=2
                case 6: points_black+=3
                case 7: points_black+=5
        for i in tablero.extremo_red:
            points_black+=5
        return points_black

    def get_movimientos_negras(self, avanza: int, tablero: Tablero, salida_pantalla: bool = True) -> list:
        '''Calcula los movimientos legales de las piezas negras
        
        Se genera una lista con los movimientos que puede realizar el
        jugador negro dado un numero determinado de posiciones a
        avanzar.
        
        Args: 
            avanza (int): 
                Numero de posiciones a avanzar.
            tablero (Tablero): 
                Tablero sobre el que se va a realizar el calculo.
            salida_pantalla (bool): 
                Si es verdadero se mostrara por pantalla los movimientos 
                disponibles formateados en una string.
                
        Returns:
            movs (list):
                Lista que contiene las posiciones de las piezas que se
                pueden mover.'''
        piezas = tablero.devolver_posicion_negras()
        movs = []
        exit = ""
        counter = 1
        temp = 0
        if avanza == 0:
            return movs
        for i in piezas:
            long_temp = tablero.get_num_piezas_fila(i[0]+avanza)
            if long_temp == None:
                pass
            elif long_temp < 6 or (i[0]+avanza) == 7:
                exit += "{0:30}".format(f"Opcion {counter} -> {i}")
                temp += 1
                if temp == 3:
                    exit += "\n"
                    temp = 0
                movs.append(i)
                counter +=1
        if salida_pantalla == True: print(exit)
        return movs
    
    def get_movimientos_rojas(self, avanza: int, tablero: Tablero, salida_pantalla:bool = True) -> list:
        '''Calcula los movimientos legales de las piezas rojas
        
        Se genera una lista con los movimientos que puede realizar el
        jugador rojo dado un numero determinado de posiciones a
        avanzar.
        
        Args: 
            avanza (int): 
                Numero de posiciones a avanzar.
            tablero (Tablero): 
                Tablero sobre el que se va a realizar el calculo.
            salida_pantalla (bool): 
                Si es verdadero se mostrara por pantalla los movimientos 
                disponibles formateados en una string.
                
        Returns:
            movs (list):
                Lista que contiene las posiciones de las piezas que se
                pueden mover.'''
        piezas = tablero.devolver_posicion_rojas()
        movs = []
        exit = ""
        counter = 1
        temp = 0
        if avanza == 0:
            return movs
        for i in piezas:
            long_temp = tablero.get_num_piezas_fila(i[0] - avanza)
            if long_temp == None:
                continue
            if long_temp < 6 or (i[0] - avanza) == 0:
                exit += "{0:30}".format(f"Opción {counter} -> {i}")
                temp += 1
                if temp == 3:
                    exit += "\n"
                    temp = 0
                movs.append(i)
                counter+=1
        if salida_pantalla==True: 
            print(exit)
        return movs

    def input_data(self,min: int, max: int) -> int:
        '''Recoge un valor entre min y max del teclado
        
        Se asegura de que el valor introducido por teclado se
        encuentra comprendido entre min y max y lo devuelve.
        
        Args:
            min (int):
                Valor minimo que debe tener la entrada.
            max (int):
                Valor maximo que debe tener la entrada.
        
        Returns:
            key (int):
                Valor introducido por teclado.
        '''
        while(True):
            try:
                key = int(input())
                if min<=key<=max:
                    return key
                else:
                    print(f"Introduce un número entre {min} y {max}, ambos incluidos")
            except(KeyboardInterrupt):
                exit()
            except(ValueError):
                pass

    def seleccionar_movimiento(self, numMov: int = 1, avanza: int = 1):
        '''Permite al turno actual jugar sus movimientos
        
        Si el turno es Rojo, el usuario se iniciara el ciclo de juego para
        el turno rojo y este podra ejecutar sus movimientos.
        
        Si el turno es Negro, la IA realizara sus jugadas correspondientes.
        
        Args:
            numMov (int): 
                Movimiento de la jugada ne la que se encuentra.
                Este valor puede ir desde 1 hasta 4.
            depth (int): 
                Profundidad maxima hasta la que explorara la IA.
                Cada 5 de profundidad corresponde con un movimiento
            avanza (int):
                Numero de posiciones que el jugador puede mover hacia
                delante en el movimiento actual
        '''
        print(f"Puedes realizar {avanza} movimientos. Selecciona una de las siguientes opciones que se muestran:\n")
        if self.turno == Color.RED:
            options = self.get_movimientos_rojas(avanza, self.Tb)
        else:
            options = self.get_movimientos_negras(avanza, self.Tb)
        if len(options) == 0:
            raise Exception
        print("Elige el movimiento que deseas hacer: ")
        selected = self.input_data(1,options.__len__())-1
        print(f"\nHas selccionado la opción {options[selected]}")
        if self.turno == Color.RED: num_mov_2 = self.Tb.get_num_piezas_fila(options[selected][0]-avanza)
        else: num_mov_2 = self.Tb.get_num_piezas_fila(options[selected][0]+avanza)
        new_row = self.Tb.mover_pieza(options[selected], avanza, self.turno)
        self.imprimir_tablero()
        if self.comprobar_fin(self.Tb):
            return 
        if numMov == 1 or numMov == 3:
            if new_row == 0 or new_row == 7:
                num_mov_2 = 1
            elif num_mov_2 == 0:
                return
            else:
                pass
            self.seleccionar_movimiento(numMov+1, num_mov_2)
        elif numMov == 2:
            if num_mov_2 == 0:
                num_mov_2 = 1
            else:
                return
            self.seleccionar_movimiento(numMov+1, num_mov_2)
        elif numMov == 4:
            return

    def seleccionar_movimiento_IA(self, numMov: int = 1,  depth: int = 15, avanza: int = 1):
        '''Permite al turno actual jugar sus movimientos
        
        Si el turno es Rojo, el usuario se iniciara el ciclo de juego para
        el turno rojo y este podra ejecutar sus movimientos.
        
        Si el turno es Negro, la IA realizara sus jugadas correspondientes.
        
        Args:
            numMov (int): 
                Movimiento de la jugada ne la que se encuentra.
                Este valor puede ir desde 1 hasta 4.
            depth (int): 
                Profundidad maxima hasta la que explorara la IA.
                Cada 5 de profundidad corresponde con un movimiento
            avanza (int):
                Numero de posiciones que el jugador puede mover hacia
                delante en el movimiento actual
        '''
        if self.turno == Color.RED:
            print(f"Puedes realizar {avanza} movimientos. Selecciona una de las siguientes opciones que se muestran:\n")
            options = self.get_movimientos_rojas(avanza, self.Tb)
            if len(options) == 0:
                raise Exception
            print("Elige el movimiento que deseas hacer: ")
            selected = self.input_data(1,options.__len__())-1
            print(f"\nHas selccionado la opción {options[selected]}")
            num_mov_2 = self.Tb.get_num_piezas_fila(options[selected][0]-avanza)
            new_row = self.Tb.mover_pieza(options[selected], avanza, self.turno)
            self.imprimir_tablero()
            if self.comprobar_fin(self.Tb):
                return 
            if numMov == 1 or numMov == 3:
                if new_row == 0 or new_row == 7:
                    num_mov_2 = 1
                elif num_mov_2 == 0:
                    return
                else:
                    pass
                self.seleccionar_movimiento_IA(numMov+1, 2,num_mov_2)
            elif numMov == 2:
                if num_mov_2 == 0:
                    num_mov_2 = 1
                else:
                    return
                self.seleccionar_movimiento_IA(numMov+1, 2, num_mov_2)
            elif numMov == 4:
                return
        else:
            start = time.time()
            self.IA(1, 1, depth)
            finish = time.time()
            print(f"numero de hojas = {self.num_recur}\ntiempo_total = {finish-start}\n")
            self.num_recur = 0
            print("\n\n")

    def calcular_puntuacion_total(self, tablero:Tablero) -> int:
        '''Devuelve el resultado de la funcion heuristica.
        
        La funcion heuristica usada es la siguiente:
            puntos_negro - puntos_rojo
            
        Returns:
            puntos_negro - puntos_rojo (int): 
                Resultado funcion heuristica.
        '''
        return (self.calcular_puntuacion_negras(tablero) - self.calcular_puntuacion_rojas(tablero))
    
    def cambiar_turno(self):
        '''Cambia el turno actual al del jugador contrario'''
        if self.turno == Color.RED:
            self.turno = Color.BLACK
        else: self.turno = Color.RED

    def comprobar_fin(self, tablero: Tablero):
        '''Comprueba si el estado del tablero es de fin de partida.
        
        Se recoge las posiciones de las piezas negras y rojas y
        posteriormente se comprueba, iterando sobre todas las piezas,
        si todas las piezas de un color han sobrepasado a las de otro
        color.
        
        Args:
            tablero (Tablero): 
                Tablero del que se comprobara el estado.
        
        Returns:
            Devuelve True si el estado es de fin de partida.'''
        negras = tablero.devolver_posicion_negras()
        rojas = tablero.devolver_posicion_rojas()
        for i in range(len(negras)):
            for j in range(len(rojas)):
                if negras[i][0]>rojas[j][0]:
                    pass
                else:
                    return False
        return True

    def MIN(self, tablero: Tablero, numMovs: int, tipo: int, depth, alpha:int, beta: int) -> int:
        '''Funcion MIN del algoritmo MINIMAX
        
        Se encarga de realizar la mejor jugada del jugador contrario y
        devolver el resultado
        
        Args:
            tablero (Tablero): 
                Tablero sobre el cual se va a jugar
            numMovs (int):
                Numero de movimientos que puede realizar en este movimiento
            tipo (int):
                Indica el movimiento en el que se encuentra. Este valor puede
                ir desde 1 hasta 5.

        Returns:
            puntuacion (int):
                Devuelve la puntuacion mas alta de los movimientos realizados'''
        puntuaciones = []
        last_row = None
        if depth == 0:
            self.num_recur+=1
            return self.calcular_puntuacion_total(tablero)
        if tipo == 5:
            value = self.MAX(tablero, 1, 1, depth-1, alpha, beta)
            return value[0]
        if numMovs == 0:
            value = self.MAX(tablero, 1, 1, depth-1, alpha, beta)
            return value[0]
        else:
            options = self.get_movimientos_rojas(numMovs, tablero, False)
            for i in options:
                if last_row == None:
                    last_row = i[0]
                elif last_row == i[0]:
                    continue
                new_tablero = deepcopy(tablero)
                num_movs_2 = new_tablero.get_num_piezas_fila(i[0]-numMovs) 
                new_row = new_tablero.mover_pieza(i,numMovs,Color.RED)
                num_movs_2 = self.comprobar_reglas(tipo, num_movs_2, new_row)
                value = self.MIN(new_tablero, num_movs_2, tipo + 1, depth, alpha, beta)
                puntuaciones.append(value)
                last_row = i[0]
            if len(puntuaciones) == 0:
                return 999
            return min(puntuaciones)

    def MAX(self, tablero: Tablero, numMovs: int, tipo: int, depth:int, alpha: int, beta: int, return_dict: dict = None, proc_counter: int = None):
        '''Funcion MAX del algoritmo MINIMAX
        
        Se encarga de realizar la mejor jugada del jugador y
        devolver el resultado
        
        Args:
            tablero (Tablero): 
                Tablero sobre el cual se va a jugar
            numMovs (int):
                Numero de movimientos que puede realizar en este movimiento
            tipo (int):
                Indica el movimiento en el que se encuentra. Este valor puede
                ir desde 1 hasta 5.
        
        Returns:
            movs (list):
                Lista que contiene los movimientos a realizar para llegar a 
                la jugada ganadora.
        '''
        puntuaciones = []
        last_row = None
        movs = []
        if depth == 0:
            self.num_recur+=1
            return (self.calcular_puntuacion_total(tablero),[])
        if tipo == 5:
            return (self.MIN(tablero, 1, 1, depth-1, alpha, beta), [])
        if numMovs == 0:
            return (self.MIN(tablero, 1, 1, depth-1, alpha, beta),[])
        else:
            options = self.get_movimientos_negras(numMovs, tablero, False)
            for i in options:
                if last_row == None:
                    last_row = i[0]
                elif last_row == i[0]:
                    puntuaciones.append(-999)
                    movs.append([])
                    continue
                new_tablero = deepcopy(tablero)
                num_movs_2 = new_tablero.get_num_piezas_fila(i[0]+numMovs) 
                new_row = new_tablero.mover_pieza(i,numMovs,Color.BLACK)
                num_movs_2 = self.comprobar_reglas(tipo, num_movs_2, new_row)
                value = self.MAX(new_tablero, num_movs_2, tipo + 1, depth, alpha, beta)
                movs.append(value[1])
                puntuaciones.append(value[0])
                last_row = i[0]
            if len(puntuaciones) == 0:
                return (-999,[])
            index_max = puntuaciones.index(max(puntuaciones))
            movs[index_max].append(index_max)
            if return_dict != None:
                movs[index_max].append(proc_counter)
                respuesta = (puntuaciones[index_max], movs[index_max])
                return_dict[proc_counter] = respuesta
            else:
                respuesta = (puntuaciones[index_max], movs[index_max])
            return respuesta
            
    def comprobar_reglas(self, tipo:int, numMovs:int, row:int) -> int:
        '''Comprueba cuantos movimientos se pueden realizar en la siguiente jugada
        
        Dado el numero de movimiento en el que se encuentra el jugador dentro
        de su turno y la fila a la que ha movido, este metodo devuelve el numero
        de movimientos disponibles para la siguiente jugada.
        
        Args:
            tipo (int):
                Movimiento en el que se encuentra el jugador dentro de su turno.
            numMovs (int): 
                Numero de piezas en la nueva fila a la que se ha movido.
            row (int):
                Fila nueva a la que se ha movido.
        
        Returns:
            num_movs_2 (int): 
                Numero de movimientos que se pueden realizar en
                la siguiente jugada.
        '''
        num_movs_2 = 0
        if tipo == 1 or tipo == 3:
            if numMovs == 0:
                num_movs_2 = 0
            elif row == 0:
                num_movs_2 = 1
            else:
                num_movs_2 = numMovs
        if tipo == 2:
            if numMovs == 0:
                num_movs_2 = 1
            elif numMovs != 0:
                num_movs_2 = 0
        return num_movs_2


    def IA(self, numMovs: int, tipo: int, depth: int):
        manager = multiprocessing.Manager()
        jobs = []
        
        movs_options = self.get_movimientos_negras(numMovs, self.Tb, False)
        return_dict = manager.dict()
        values = []
        movs = []
        last_row = None
        proc_counter = 0
        for i in movs_options:
            if last_row == None:
                last_row = i[0]
            elif last_row == i[0]:
                return_dict[proc_counter] = (-200,[])
                proc_counter+=1
                continue
            # COPIA DEL TABLERO
            tablero_copia = deepcopy(self.Tb)
            # REALIZAR EL MOVIMIENTO i SOBRE EL TABLERO NUEVO
            num_movs_2 = tablero_copia.get_num_piezas_fila(i[0]+numMovs)
            new_row = tablero_copia.mover_pieza(i, numMovs, Color.BLACK)
            num_movs_2 = self.comprobar_reglas(1, num_movs_2, new_row)
            # LLAMADA AL MÉTODO MAX PARA HACER LOS SIGUIENTES
            p = multiprocessing.Process(target=self.MAX, args=(tablero_copia, num_movs_2, 2, depth, self.alpha, self.beta, return_dict, proc_counter))
            jobs.append(p)
            p.start()
            proc_counter+=1
            last_row = i[0]
            
        for i in jobs:
            i.join()

        # SACAR LA OPCION CON MAYOR PUNTUACION
        respuestas = return_dict.values()
        for i in respuestas:
            values.append(i[0])
            movs.append(i[1])

        index_max = values.index(max(values))
        movs_final = movs[index_max]

        for i in reversed(movs_final):
            if numMovs == 0:
                return
            options = self.get_movimientos_negras(numMovs, self.Tb,False)
            num_movs_2 = self.Tb.get_num_piezas_fila(options[i][0]+numMovs) 
            new_row = self.Tb.mover_pieza(options[i],numMovs,Color.BLACK)
            
            if self.comprobar_fin(self.Tb) == True:
                return
            numMovs = self.comprobar_reglas(tipo, num_movs_2, new_row)
            tipo += 1      