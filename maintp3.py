import random

TABLERO_ANCHO = 5
TABLERO_ALTO = 5
LIMITE_CARACTERES = 8
ANCHO_VENTANA_JUEGO, ALTO_VENTANA_JUEGO = 1280, 720
X_FONDO, Y_FONDO = 1, 1
X_TABLERO, Y_TABLERO = 434, 160
X_ACIERTOS_ROJO, Y_ACIERTOS_ROJO = 173, 528
X_ACIERTOS_AZUL, Y_ACIERTOS_AZUL = 780, 528
X_AGENTEDOBLE_ROJO, Y_AGENTEDOBLE_ROJO = 297, 654
X_AGENTEDOBLE_AZUL, Y_AGENTEDOBLE_AZUL = 904, 654
X_LLAVE, Y_LLAVE = 510, 450
X_PIZARRON_ROJO, Y_PIZARRON_ROJO = 181, 159
X_PIZARRON_AZUL, Y_PIZARRON_AZUL = 899, 159
X_BOTON_PASAR, Y_BOTON_PASAR = 509, 20
X_TEXTO_TARJETA, Y_TEXTO_TARJETA = 40, 35
X_TEXTO_PIZARRON, Y_TEXTO_PIZARRON = 123, 80
X_SLOT_LLAVE, Y_SLOT_LLAVE = 31, 28
STEP_X_TARJETA, STEP_Y_TARJETA = 80, 50
STEP_X_SLOT, STEP_Y_SLOT = 40, 40
SEP_TARJETA = 3



 def main():
    juego = Juego()
    juego.iniciar()
    gamelib.resize(ANCHO_VENTANA_JUEGO, ALTO_VENTANA_JUEGO)
    while gamelib.is_alive() and not juego.terminado():
    	gamelib.play_sound('musica/theme.wav')
        mostrar_estado_juego(juego)
        juego.generar_tablero()
        juego.generar_llave()
        juego.seleccionar_spymaster()
        while not juego.ronda_terminada():
            mostrar_estado_juego(juego)
            if juego.turno() == spymaster:
				mostrar_llave()
                juego.pedir_pista()
                if not juego.pista_es_valida():
                    juego.penalizar()
             else:
                # Pedir agente hasta equivocarse o hasta que se terminen las chances
                juego.pedir_agente()
     mostrar_ganador(juego)




def mostrar_estado_juego(juego):
	mostrar_tablero(juego)
	mostrar_pistas(juego)
	for fil in len(juego.tablero):
		for col in juego.tablero[fil]:
			indice_fil, indice_col = fil, juego.tablero[fil].index(col)
			if col == "":
				genero = random.choice(('m', 'f'))
				elemento = juego.llave[indice_fil][indice_col]
				gamelib.drawimage(f"imagenes/tarjeta{elemento}{genero}.gif", X_LLAVE + indice_col * STEP_X_SLOT, Y_LLAVE + indice_fil * STEP_Y_SLOT)



def mostrar_tablero(juego):
"""Funcion que recibe el estado del juego y devuelve el tablero con 25 cartas"""

	for fil in len(juego.tablero):
		for col in juego.tablero[fil]:
		indice_fil, indice_col = fil, juego.tablero[fil].index(col)
		gamelib.drawimage("imagenes/tarjetavacia.gif", X_TABLERO + indice_col * STEP_X_TARJETA, Y_TABLERO + indice_fil * STEP_Y_TARJETA)
		gamelib.drawtext(juego.tarjetas[indice_fil][indice_col], X_TABLERO + indice_col * STEP_X_TARJETA + X_TEXTO_TARJETA, Y_TABLERO + indice_fil * STEP_Y_TARJETA + Y_TEXTO_TARJETA)

def mostrar_pistas(juego):
"""Funcion que recibe el estado del juego y muestra las pistas de cada equipo en una pizarra"""

	if juego.turno.nombre == "rojo":
		str_pistas = "\n".join(juego.turno.pista)
		gamelib.drawimage("imagenes/pizarronrojo.gif", X_PIZARRON_ROJO, Y_PIZARRON_ROJO)
		gamelib.drawtext(str_pistas, X_PIZARRON_ROJO + X_TEXTO_PIZARRON, Y_PIZARRON_ROJO + Y_TEXTO_PIZARRON)

	if juego.turno.nombre == "azul":
		str_pistas = "\n".join(juego.turno.pista)
		gamelib.drawimage("imagenes/pizarronazul.gif", X_PIZARRON_AZUL, Y_PIZARRON_AZUL)
		gamelib.drawtext(str_pistas, X_PIZARRON_AZUL + X_TEXTO_PIZARRON, Y_PIZARRON_AZUL + Y_TEXTO_PIZARRON)

def mostrar_llave(juego):
"""Funcion que recibe el estado del juego y muestra la llave del juego"""

	for fil in len(juego.llave):
		for elemento in juego.llave[fil]:
			indice_fil, indice_elemento = fil, juego.llave[fil].index(elemento)
			gamelib.drawimage(f"imagenes/llave{juego.primerequipo}.gif", X_LLAVE, Y_LLAVE)
			gamelib.drawimage(f"imagenes/slot{elemento}.gif", X_LLAVE + indice_col * STEP_X_SLOT, Y_LLAVE + indice_fil * STEP_Y_SLOT)


def esperar_eleccion():
"""Funcion que sirve para esperar el click del usuario cuando elige el agente"""

	evento = gamelib.wait(gamelib.EventType.ButtonPress)
	if X_TABLERO < evento.x < X_TABLERO + TABLERO_ANCHO * STEP_X_TARJETA and Y_TABLERO < evento.y < Y_TABLERO + TABLERO_ALTO * STEP_Y_TARJETA :
		x, y = (evento.x - X_TABLERO) // STEP_X_TARJETA, (evento.y - Y_TABLERO) // STEP_Y_TARJETA
	return x, y




class Juego:
    def _init_(self):
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
        self.primer_equipo = ""
        self.pasar_turno = False

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
        # TODO: adicionar las tarjetas a su respectivo equipo

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
        trampa = ultima_pista[0] in cartas
        if not trampa:
            self.pasar_turno = False
        return trampa

    def penalizar(self):
        """En caso de trampa se le otorgara una carta al azar al proximo equipo"""
        index_tramposo = self.equipos.index(self.turno)
        otro_equipo = self.equipos[1 if index_tramposo == 0 else 0]
        # TODO: agarrar una de las cartas faltantes del equipo y pasarsela a encontradas

    def siguiente_turno(self):
        """Cambia el turno para el proximo equipo"""
        index = self.equipos.index(self.turno)
        self.turno = self.equipos[1 if index == 0 else 0]
        self.pasar_turno = True

    def pedir_agente(self, coordenadas):
        """Recibe las coordenadas x e y del tablero"""
        x, y = coordenadas
        valor = llave[y][x]
        tarjeta = tablero[y][x]
        tablero[y][x] = ""
        self.puntuar_equipo(valor)
        self.ultima_pista[1] += 1

    def puntuar_equipo(self, valor, tarjeta):
        """Recibe un valor (string) y puntua al equipo y pasa de ronda si necesario"""
        if self.turno.nombre == valor:
            # Sumar valor y tarjeta a encontradas
            print(valor)
            self.turno.puntos += 1
            self.turno.agregar_tarjeta_adivinada(tarjeta)
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
            self.otro_equipo.agregar_tarjeta_adivinada(tarjeta)
            self.siguiente_turno()


class Equipo:
    def _init_(self, nombre):
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