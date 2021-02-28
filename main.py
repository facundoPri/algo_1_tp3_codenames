#!/usr/bin/env python3
import random
import gamelib

TABLERO_ANCHO = 5
TABLERO_ALTO = 5


def main():
    juego = Juego()
    juego.iniciar()
    while not juego.terminado:
        # mostrar_estado_juego(juego)
        juego.generar_tablero()
        juego.generar_llave()
        juego.seleccionar_spymaster()
        juego.inicializar_rondas()
        while not juego.ronda_terminada:
            # mostrar_estado_juego(juego)
            juego.pedir_pista()
            if not juego.pista_es_valida():
                juego.penalizar()
            # Pedir agente hasta equivocarse o hasta que se terminen las chances
            while juego.seguir_turno:
                juego.pedir_agente()
    # mostrar_ganador(juego)



class Juego:
    def __init__(self):
        self.terminado = False
        self.ronda_terminada = False
        self.tablero = [["" for x in range(TABLERO_ANCHO)] for x in range(TABLERO_ALTO)]
        self.llave = [["" for x in range(TABLERO_ANCHO)] for x in range(TABLERO_ALTO)]
        self.equipos = []
        self.turno = ""
        self.ultima_pista = ()
        self.tarjetas = []
        self.jugadores = []
        self.jugadores_min = 4
        self.primer_equipo = ""
        self.seguir_turno = False

    def iniciar(self):
        """Inicializa el juego, creando los equipos y cambiando el estado del juego"""
        if len(self.jugadores) < self.jugadores_min:
            raise Exception("Se requieren mas jugadores para jugar")
        # Generar equipos
        equipo_rojo = Equipo("rojo")
        equipo_azul = Equipo("azul")
        self.generar_equipos(equipo_rojo, equipo_azul)
        # TODO: Puede agarrar los equipos del self.equipos en vez de pasarlos como argumentos
        self.equipos = [equipo_rojo, equipo_azul]
        # Inicializar juego
        self.terminado = False

    def agregar_jugador(self, jugador):
        """Recibe un jugador y lo agrega a la lista de jugadores"""
        if jugador in self.jugadores:
            raise Exception("Este jugador ya esta jugando")
        self.jugadores.append(jugador)

    def generar_equipos(self, equipo_rojo, equipo_azul):
        """Recibe dos equipos y asigna los jugadores a cada uno"""
        # Randomizar lista de jugadores
        random_list = random.sample(self.jugadores, len(self.jugadores))
        mitad = len(random_list) // 2
        equipos = [random_list[:mitad], random_list[mitad:]]
        # Randomizar lista de equipos
        equipo_random = random.sample(equipos, len(equipos))
        # Asignar equipos
        equipo_rojo.agregar_jugadores(equipo_random[0])
        equipo_azul.agregar_jugadores(equipo_random[1])

    def obtener_cartar(self, ruta):
        """Busca en la ruta pasada 25 cartas de forma aleatoria"""
        lista_cartas = []
        with open(ruta) as cartas:
            for carta in cartas:
                if len(carta) > 8 and carta in lista_cartas:
                    continue
                lista_cartas.append(carta.upper())
        self.cartas = random.sample(lista_cartas, 25)

    def generar_tablero(self):
        """Con la lista de cartas arma el tablero"""
        tarjetas = self.tarjetas
        self.tablero = [[tarjetas.pop() for x in tarjetas[:5]] for x in range(5)]

    def generar_llave(self):
        """Genera una llave y el primer turno"""
        # Elige un equpo para arrancar
        equipo = random.choice(self.equipos)
        self.turno = equipo
        self.primer_equipo = equipo
        # Generar llave
        rojo = ["rojo"] * (9 if equipo.nombre == "rojo" else 8)
        azul = ["azul"] * (9 if equipo.nombre == "azul" else 8)
        asesino = ["asesino"]
        resto = 25 - (len(rojo) + len(azul) + len(asesino))
        civil = ["civil"] * resto
        lista_agentes = rojo + azul + asesino + civil
        agentes = random.sample(lista_agentes, 25)
        self.llave = [[agentes.pop() for x in agentes[:5]] for x in range(5)]

    def pedir_pista(self, pista):
        """Recibe una pista en formato de (string, numero) y la agrega en el juego para ser validada y la lista del equipo"""
        if not type(pista[0]) == "str" or not type(pista[1]) == "int":
            raise Exception("Pista no tiene formato valido")
        self.ultima_pista = pista
        # Agrega la pista al equipo que le corresponde el turno
        self.turno.pistas.append(pista[0])

    def pista_es_valida(self):
        """Devuelve un booleano diciendo si la ultima pista pasada es valida o no"""
        # TODO: Mejorar validacion
        trampa = ultima_pista[0] in self.tarjetas
        if not trampa:
            self.seguir_turno = True
        return trampa

    def encontrar_en_tablero(self, tarjeta):
        """Recibe el nombre de una tarjeta y devuelve su posicion en el tablero"""
        for y in self.tablero:
            if not tarjeta in y:
                continue
            for x in y:
                if x == tarjeta:
                    return (x, y)

    def penalizar(self):
        """En caso de trampa se le otorgara una carta al azar al proximo equipo"""
        index_tramposo = self.equipos.index(self.turno)
        otro_equipo = self.equipos[1 if index_tramposo == 0 else 0]
        # TODO: agarrar una de las tarjetas faltantes del equipo y pasarsela a encontradas
        tarjeta_faltante_random = otro_equipo.seleccionar_tarjeta_random()
        x, y = self.encontrar_en_tablero(tarjeta_faltante_random)
        self.tablero[y][x] = ""

    def siguiente_turno(self):
        """Cambia el turno para el proximo equipo"""
        index = self.equipos.index(self.turno)
        self.turno = self.equipos[1 if index == 0 else 0]
        self.seguir_turno = False

    def pedir_agente(self, coordenadas):
        """Recibe las coordenadas x e y del tablero"""
        x, y = coordenadas
        valor = self.llave[y][x]
        tarjeta = self.tablero[y][x]
        self.tablero[y][x] = ""
        self.puntuar_equipo(valor)
        self.ultima_pista[1] -= 1

    def puntuar_equipo(self, valor, tarjeta):
        """Recibe un valor (string) y puntua al equipo y pasa de ronda si necesario"""
        # TODO: Repartir acciones en varias funciones
        if self.turno.nombre == valor:
            # Sumar valor y tarjeta a encontradas
            print(valor)
            self.turno.puntos += 1
            self.turno.agregar_tarjeta_adivinada(tarjeta)
            if self.turno.tarjetas_totales == len(self.turno.tarjetas_encontradas):
                self.finalizar_rondas()
            if self.ultima_pista[1] == 0:
                self.siguiente_turnto()
        elif valor == "asesino":
            # menor 5 puntos y termina juego
            print(valor)
            self.turno.puntos -= 5
            self.siguiente_turno()
        elif valor == "civil":
            # menor un punto y siguiente turno
            print(valor)
            self.turno.puntos -= 1
            self.siguiente_turno()
        else:
            # Sumar punto y tarjeta al otro equipo y siguiente turno
            print(valor)
            index = self.equipos.index(self.turno)
            otro_equipo = self.equipos[1 if index == 0 else 0]
            otro_equipo.puntos += 1
            otro_equipo.agregar_tarjeta_adivinada(tarjeta)
            if otro_equipo.tarjetas_totales == len(otro_equipo.tarjetas_encontradas):
                self.finalizar_rondas()
            self.siguiente_turno()

    def seleccionar_spymaster(self):
        """Seleccionar un spymaster para cada equipo"""
        for equipo in self.equipo:
            equipo.elegir_spymaster()

    def inicializar_rondas(self):
        """Inicializa la ronda"""
        self.ronda_terminada = False

    def finalizar_rondas(self):
        """Finaliza la ronda"""
        self.ronda_terminada = True


class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.jugadores = []
        self.futuros_spymaster = []
        self.puntos = 0
        self.victorias = 0
        self.spymaster = ""
        self.pistas = []
        self.tarjetas_totales = 0
        self.tarjetas_faltantes = []
        self.tarjetas_encontradas = []

    def agregar_jugadores(self, jugadores):
        """Recibe una lista de jugadores y los agrega al equipo"""
        self.jugadores = jugadores
        self.para_spymaster = jugadores

    def elegir_spymaster(self):
        """Elije de manera random un spymaster de la lista que no fue todavia"""
        nuevo_spymaster = random.choice(self.futuros_spymaster)
        self.futuros_spymaster.remove(nuevo_spymaster)
        self.spymaster = nuevo_spymaster

    def agregar_tarjeta_adivinada(self, tarjeta):
        """Recibe una tarjeta, la resta de tarjetas faltantes y la agrega a encontradas"""
        if tarjeta in self.tarjetas_encontradas:
            raise Exception("La tarjeta ya fue encontrada")
        index_tarjeta = self.tarjetas_faltantes.index(tarjeta)
        if index_tarjeta >= 0:
            self.tarjetas_faltantes.pop(index_tarjeta)
            self.tarjetas_encontradas.append(tarjeta)

    def seleccionar_tarjeta_random(self):
        """Devuelve una tarjeta faltante de forma aleatoria"""
        tarjeta = random.choice(self.tarjetas_faltantes)
        self.agregar_tarjeta_adivinada(tarjeta)
        return tarjeta

