#!/usr/bin/env python3
import random

TABLERO_ANCHO = 5
TABLERO_ALTO = 5


# def main():
#     juego = inicializar_juego()
#     while not juego.terminado():
#         mostrar_estado_juego(juego)
#         juego.generar_tablero()
#         juego.generar_llave()
#         juego.seleccionar_spymaster()
#         while not juego.ronda_terminada():
#             mostrar_estado_juego(juego)
#             if juego.turno() == spymaster:
#                 juego.pedir_pista()
#                 if not juego.pista_es_valida():
#                     juego.penalizar()
#             else:
#                 # Pedir agente hasta equivocarse o hasta que se terminen las chances
#                 juego.pedir_agente()
#     mostrar_ganador(juego)


class Juego:
    def __init__(self):
        self.terminado = False
        self.ronda_terminada = False
        self.tablero = [["" for x in range(TABLERO_ANCHO)] for x in range(TABLERO_ALTO)]
        self.llave = [["" for x in range(TABLERO_ANCHO)] for x in range(TABLERO_ALTO)]
        self.equipos = []
        self.turno = ""
        self.ultima_pista = ()
        self.cartas = []
        self.jugadores = []
        self.jugadores_min = 4

    def iniciar(self):
        """Inicializa el juego, creando los equipos y cambiando el estado del juego"""
        if len(self.jugadores) < self.jugadores_min:
            raise Exception("Se requieren mas jugadores para jugar")
        # Generar equipos
        equipo_rojo = Equipo("rojo")
        equipo_azul = Equipo("azul")
        self.generar_equipos()
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
                if len(carta) > 8:
                    continue
                lista_cartas.append(carta.upper())
        self.cartas = random.sample(lista_cartas, 25)

    def generar_tablero(self):
        """Con la lista de cartas arma el tablero"""
        cartas = self.cartas
        self.tablero = [[cartas.pop() for x in cartas[:5]] for x in range(5)]

    def generar_llave(self):
        """Genera una llave y el primer turno"""
        # Elige un equpo para arrancar
        equipo = random.choice(self.equipos)
        self.turno = equipo
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
        self.turno.pistas.append(pista)

    def pista_es_valida(self):
        """Devuelve un booleano diciendo si la ultima pista pasada es valida o no"""
        # TODO: Mejorar validacion
        return ultima_pista[0] in cartas
class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.jugadores = []
        self.futuros_spymaster = []
        self.puntos = 0
        self.victorias = 0
        self.spymaster = ""
        self.pistas = []

    def agregar_jugadores(self, jugadores):
        """Recibe una lista de jugadores y los agrega al equipo"""
        self.jugadores = jugadores
        self.para_spymaster = jugadores

    def elegir_spymaster(self):
        """Elije de manera random un spymaster de la lista que no fue todavia"""
        nuevo_spymaster = random.choice(self.futuros_spymaster)
        self.futuros_spymaster.remove(nuevo_spymaster)
        self.spymaster = nuevo_spymaster

    def agregar_puntos(self):
        """Suma"""
