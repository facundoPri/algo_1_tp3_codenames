import random
import gamelib
import time

TABLERO_ANCHO = 5
TABLERO_ALTO = 5
TIMEPO_CANCION = 110
LIMITE_CARACTERES = 8
FILAS_ACIERTOS = 4
ANCHO_VENTANA_JUEGO, ALTO_VENTANA_JUEGO = 1280, 720
X_FONDO, Y_FONDO = 1, 1
X_PUNTAJE, Y_PUNTAJE = 10, 20
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
X_TEXTO_TARJETA_INV, Y_TEXTO_TARJETA_INV = 13, 15
X_TEXTO_PIZARRON, Y_TEXTO_PIZARRON = 123, 80
X_TARJETA_ASESINO, Y_TARJETA_ASESINO =  390, 203
X_TEXTO_GANADOR, Y_TEXTO_GANADOR = 450, 150
X_TEXTO_GANADOR_SALIDA, Y_TEXTO_GANADOR_SALIDA = 330, 600
X_SLOT_LLAVE, Y_SLOT_LLAVE = 31, 28
STEP_X_TARJETA, STEP_Y_TARJETA = 80, 50
STEP_X_SLOT, STEP_Y_SLOT = 40, 40
STEP_PUNTAJE = 1260
SEP_TARJETA = 4

def main():
	juego = Juego()
	gamelib.play_sound("musica/theme.wav")
	# TODO: descomentar
	# jugadores = gamelib.input("Listar todos los jugadores\nSepararlos por coma")
	jugadores = "facu, fede, juan, diego"
	juego.agregar_jugadores(jugadores)
	juego.iniciar()
	gamelib.resize(ANCHO_VENTANA_JUEGO, ALTO_VENTANA_JUEGO)
	while gamelib.is_alive() and not juego.terminado:
		gamelib.draw_begin()
		print("Arranca juego")
		juego.obtener_tarjetas("tarjetas.txt")
		juego.generar_tablero()
		juego.generar_llave()
		mostrar_estado_juego(juego)
		mostrar_llave(juego)
		juego.inicializar_rondas()
		while not juego.ronda_terminada:
			print(f"Turno de equipo {juego.turno.nombre}")
			# TODO: descomentar
			mostrar_llave(juego)
			#pista = gamelib.input("Ingresar pista:")
			pista = "hola 1"
			pista = pista.split()
			pista[0] = pista[0].upper()
			pista[1] = int(pista[1])
			juego.pedir_pista(pista)
			if not juego.pista_es_valida():
				juego.penalizar()
			# Pedir agente hasta equivocarse o hasta que se terminen las chances
			while not juego.pasar_turno:
				mostrar_estado_juego(juego)
				juego.pedir_agente(esperar_eleccion())
	mostrar_ganador(juego)

def mostrar_estado_juego(juego):
	"""Funcion que recibe el estado del juego y muestra el estado del mismo"""
	mostrar_fondo()
	mostrar_tablero(juego)
	mostrar_aciertos(juego)
	actualizar_tablero(juego)
	mostrar_puntaje(juego)

def actualizar_tablero(juego):
	"""Funcion que recibe el estado del juego y actualiza las tarjetas segun la eleccion hecha"""

	for indice_fil, fil in enumerate(juego.tablero):
		for indice_col, col in enumerate(fil):
			if col == "ROJO" or col == "AZUL":
				if (indice_fil + indice_col) % 2:
					genero = 'f'
				else:
					genero = 'm'
				elemento = juego.llave[indice_fil][indice_col]
				gamelib.draw_image(f"imagenes/tarjeta{elemento}{genero}.gif", X_TABLERO + indice_col * (STEP_X_TARJETA + SEP_TARJETA),
				Y_TABLERO + indice_fil * (STEP_Y_TARJETA + SEP_TARJETA))
				
				if juego.tablero[indice_fil][indice_col] == "ROJO":
					gamelib.draw_text(
					juego.tablero[indice_fil][indice_col],
					X_TABLERO
					+ indice_col * (STEP_X_TARJETA + SEP_TARJETA)
					+ X_TEXTO_TARJETA,
					Y_TABLERO
					+ indice_fil * (STEP_Y_TARJETA + SEP_TARJETA)
					+ Y_TEXTO_TARJETA,
					fill="red",
					size=9)

				else:
					gamelib.draw_text(
					juego.tablero[indice_fil][indice_col],
					X_TABLERO
					+ indice_col * (STEP_X_TARJETA + SEP_TARJETA)
					+ X_TEXTO_TARJETA,
					Y_TABLERO
					+ indice_fil * (STEP_Y_TARJETA + SEP_TARJETA)
					+ Y_TEXTO_TARJETA,
					fill="blue",
					size=9)					

def mostrar_fondo():
	"""Funcion que muestra el fondo del juego"""
	gamelib.draw_image("imagenes/fondo.gif", 1, 1)


def mostrar_tablero(juego):
	"""Funcion que recibe el estado del juego y muestra las tarjetas que hay en el tablero"""

	for fil in range(len(juego.tablero)):
		for col in juego.tablero[fil]:
			indice_fil, indice_col = fil, juego.tablero[fil].index(col)
			gamelib.draw_image(
				"imagenes/tarjetavacia.gif",
				X_TABLERO + indice_col * (STEP_X_TARJETA + SEP_TARJETA),
				Y_TABLERO + indice_fil * (STEP_Y_TARJETA + SEP_TARJETA),
			)
			gamelib.draw_text(
				juego.tablero[indice_fil][indice_col],
				X_TABLERO
				+ indice_col * (STEP_X_TARJETA + SEP_TARJETA)
				+ X_TEXTO_TARJETA,
				Y_TABLERO
				+ indice_fil * (STEP_Y_TARJETA + SEP_TARJETA)
				+ Y_TEXTO_TARJETA,
				fill="black",
				size=9,
			)
			gamelib.draw_text(
				juego.tablero[indice_fil][indice_col],
				X_TABLERO
				+ indice_col * (STEP_X_TARJETA + SEP_TARJETA)
				+ X_TEXTO_TARJETA
				+ X_TEXTO_TARJETA_INV,
				Y_TABLERO
				+ indice_fil * (STEP_Y_TARJETA + SEP_TARJETA)
				+ Y_TEXTO_TARJETA
				- Y_TEXTO_TARJETA_INV,
				fill="brown",
				anchor="w",
				size=7,
				angle=180,
			)


def mostrar_pistas(juego):
	"""Funcion que recibe el estado del juego y muestra las pistas de cada equipo en una pizarra"""

	if juego.turno.nombre == "rojo":
		str_pistas = "\n".join(juego.turno.pista)
		gamelib.draw_image(
			"imagenes/pizarronrojo.gif", X_PIZARRON_ROJO, Y_PIZARRON_ROJO
		)
		gamelib.draw_text(
			str_pistas,
			X_PIZARRON_ROJO + X_TEXTO_PIZARRON,
			Y_PIZARRON_ROJO + Y_TEXTO_PIZARRON, fill = 'red', size = 20
		)

	if juego.turno.nombre == "azul":
		str_pistas = "\n".join(juego.turno.pista)
		gamelib.draw_image(
			"imagenes/pizarronazul.gif", X_PIZARRON_AZUL, Y_PIZARRON_AZUL
		)
		gamelib.draw_text(
			str_pistas,
			X_PIZARRON_AZUL + X_TEXTO_PIZARRON,
			Y_PIZARRON_AZUL + Y_TEXTO_PIZARRON, fill = 'blue', size = 20
		)


def mostrar_llave(juego):
	"""Funcion que recibe el estado del juego y muestra la llave del juego"""
	gamelib.draw_image(f"imagenes/llave{juego.primer_equipo.nombre}.gif", X_LLAVE, Y_LLAVE)
	for indice_fil, fil in enumerate(juego.llave):
		for indice_col, elemento in enumerate(fil):
			gamelib.draw_image(f"imagenes/slot{elemento}.gif", X_LLAVE + X_SLOT_LLAVE + indice_col * STEP_X_SLOT, Y_LLAVE + Y_SLOT_LLAVE + indice_fil * STEP_Y_SLOT)

def mostrar_aciertos(juego):
	"""Funcion que recibe el estado del juego y muestra las tarjetas acertadas de cada equipo"""
	for equipo in juego.equipos:
		if equipo.nombre == "rojo":
			for indice in range(len(equipo.tarjetas_encontradas)):
				
				if indice <= FILAS_ACIERTOS - 1:
					gamelib.draw_image(f"imagenes/tarjetavacia.gif", X_ACIERTOS_ROJO + indice * (STEP_X_TARJETA + SEP_TARJETA), Y_ACIERTOS_ROJO)
					gamelib.draw_text(equipo.tarjetas_encontradas[indice], X_ACIERTOS_ROJO + X_TEXTO_TARJETA + indice * (STEP_X_TARJETA + SEP_TARJETA), Y_ACIERTOS_ROJO + Y_TEXTO_TARJETA ,
				fill="black",
				size=9)
					gamelib.draw_text(
				equipo.tarjetas_encontradas[indice],
				X_ACIERTOS_ROJO
				+ indice * (STEP_X_TARJETA + SEP_TARJETA)
				+ X_TEXTO_TARJETA
				+ X_TEXTO_TARJETA_INV,
				Y_ACIERTOS_ROJO
				+ Y_TEXTO_TARJETA
				- Y_TEXTO_TARJETA_INV,
				fill="brown",
				anchor="w",
				size=7,
				angle=180,
			)
				
				
				else:
					gamelib.draw_image(f"imagenes/tarjetavacia.gif", X_ACIERTOS_ROJO + (indice - FILAS_ACIERTOS) * (STEP_X_TARJETA + SEP_TARJETA), Y_ACIERTOS_ROJO + (STEP_Y_TARJETA + SEP_TARJETA))
					gamelib.draw_text(equipo.tarjetas_encontradas[indice], X_ACIERTOS_ROJO + X_TEXTO_TARJETA + (indice - FILAS_ACIERTOS) * (STEP_X_TARJETA + SEP_TARJETA), Y_ACIERTOS_ROJO + Y_TEXTO_TARJETA + (STEP_Y_TARJETA + SEP_TARJETA) ,
				fill="black",
				size=9)
					gamelib.draw_text(
				equipo.tarjetas_encontradas[indice],
				X_ACIERTOS_ROJO
				+ (indice - FILAS_ACIERTOS) * (STEP_X_TARJETA + SEP_TARJETA)
				+ X_TEXTO_TARJETA
				+ X_TEXTO_TARJETA_INV,
				Y_ACIERTOS_ROJO
				+ (STEP_Y_TARJETA + SEP_TARJETA)
				+ Y_TEXTO_TARJETA
				- Y_TEXTO_TARJETA_INV,
				fill="brown",
				anchor="w",
				size=7,
				angle=180,
			)				
		else:
			for indice, tarjeta in enumerate(equipo.tarjetas_encontradas):
				
				if indice <= FILAS_ACIERTOS - 1:
					gamelib.draw_image(f"imagenes/tarjetavacia.gif", X_ACIERTOS_AZUL + indice * (STEP_X_TARJETA + SEP_TARJETA), Y_ACIERTOS_AZUL)
					gamelib.draw_text(equipo.tarjetas_encontradas[indice], X_ACIERTOS_AZUL + X_TEXTO_TARJETA + indice * (STEP_X_TARJETA + SEP_TARJETA), Y_ACIERTOS_AZUL + Y_TEXTO_TARJETA ,
				fill="black",
				size=9)
					gamelib.draw_text(
				equipo.tarjetas_encontradas[indice],
				X_ACIERTOS_AZUL
				+ indice * (STEP_X_TARJETA + SEP_TARJETA)
				+ X_TEXTO_TARJETA
				+ X_TEXTO_TARJETA_INV,
				Y_ACIERTOS_AZUL
				+ Y_TEXTO_TARJETA
				- Y_TEXTO_TARJETA_INV,
				fill="brown",
				anchor="w",
				size=7,
				angle=180,
			)
				
				
				else:
					gamelib.draw_image(f"imagenes/tarjetavacia.gif", X_ACIERTOS_AZUL + (indice - FILAS_ACIERTOS) * (STEP_X_TARJETA + SEP_TARJETA), Y_ACIERTOS_AZUL + (STEP_Y_TARJETA + SEP_TARJETA))
					gamelib.draw_text(equipo.tarjetas_encontradas[indice], X_ACIERTOS_AZUL + X_TEXTO_TARJETA + (indice - FILAS_ACIERTOS) * (STEP_X_TARJETA + SEP_TARJETA), Y_ACIERTOS_AZUL + (STEP_Y_TARJETA + SEP_TARJETA)+ Y_TEXTO_TARJETA ,
				fill="black",
				size=9)
					gamelib.draw_text(
				equipo.tarjetas_encontradas[indice],
				X_ACIERTOS_AZUL
				+ (indice - FILAS_ACIERTOS) * (STEP_X_TARJETA + SEP_TARJETA)
				+ X_TEXTO_TARJETA
				+ X_TEXTO_TARJETA_INV,
				Y_ACIERTOS_AZUL
				+ (STEP_Y_TARJETA + SEP_TARJETA)
				+ Y_TEXTO_TARJETA
				- Y_TEXTO_TARJETA_INV,
				fill="brown",
				anchor="w",
				size=7,
				angle=180,
			)			

def mostrar_puntaje(juego):
	"""Funcion que recibe el estado del juego y muestra los puntos obtenidos por cada equipo"""
	for indice, equipo in enumerate(juego.equipos):
		puntaje = equipo.puntos
		if equipo.nombre == "rojo":
			gamelib.draw_text(f"Puntaje equipo {equipo.nombre}: {str(puntaje)}", X_PUNTAJE + indice * STEP_PUNTAJE, Y_PUNTAJE, anchor = 'w', fill = "red", size = 25)
		else:
			gamelib.draw_text(f"Puntaje equipo {equipo.nombre}: {str(puntaje)}", X_PUNTAJE + indice * STEP_PUNTAJE, Y_PUNTAJE, anchor = 'e', fill = "blue", size = 25)

def mostrar_ganador(juego):
	"""Funcion que recibe el estado del juego y muestra al equipo ganador"""
	ganador = ""
	puntajes = []

	for equipo in juego.equipos:
		puntajes.append(equipo.puntos)
	for equipo in juego.equipos:
		if equipo.puntos == max(puntajes):
			ganador = equipo.nombre

	while gamelib.is_alive():

		gamelib.draw_begin()
		gamelib.draw_image("imagenes/fondoganador.gif", X_FONDO, Y_FONDO)
		gamelib.draw_text(f"El equipo {ganador} es el ganador!\nPuntaje final: {str(max(puntajes))}", X_TEXTO_GANADOR, Y_TEXTO_GANADOR, fill = 'gray', size = 50, justify = 'c')
		gamelib.draw_text('Presiona cualquier tecla para salir', X_TEXTO_GANADOR_SALIDA, Y_TEXTO_GANADOR_SALIDA, fill = 'gray', size = 30)
		gamelib.draw_end()

		ev = gamelib.wait(gamelib.EventType.KeyPress)

		if not ev:
			break
		if ev.type == gamelib.EventType.KeyPress:
			break

def esperar_eleccion():
	"""Funcion que sirve para esperar el click del usuario cuando elige el agente"""

	evento = gamelib.wait(gamelib.EventType.ButtonPress)
	while (
		evento.x <= X_TABLERO or evento.x >= X_TABLERO + TABLERO_ANCHO * STEP_X_TARJETA
		or evento.y <= Y_TABLERO or evento.y >= Y_TABLERO + TABLERO_ALTO * STEP_Y_TARJETA
	):
		evento = gamelib.wait(gamelib.EventType.ButtonPress)

	x, y = (evento.x - X_TABLERO) // STEP_X_TARJETA, (
		evento.y - Y_TABLERO
	) // STEP_Y_TARJETA

	return (x, y)

def encontrado_asesino():
	gamelib.draw_image("imagenes/tarjetaasesino.gif", X_TARJETA_ASESINO, Y_TARJETA_ASESINO)
	gamelib.play_sound("musica/sfasesino.wav")
	gamelib.say("Te encontraste con el asesino!\nFin de la ronda")



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
		self.pasar_turno = False

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

	def agregar_jugadores(self, jugadores):
		"""Recibe un string con todos los jugadores, lo transforma a lista y los agrega al juego"""
		lista_jugadores = jugadores.split(",")
		for jugador in lista_jugadores:
			self.agregar_jugador(jugador.strip())

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

	def obtener_tarjetas(self, ruta):
		"""Busca en la ruta pasada 25 tarjetas de forma aleatoria"""
		lista_tarjetas = []
		with open(ruta) as tarjetas:
			for tarjeta in tarjetas:
				if not len(tarjeta) > 8 and not tarjeta in lista_tarjetas:
					lista_tarjetas.append(tarjeta.upper().rstrip())
		self.tarjetas = random.sample(lista_tarjetas, 25)

	def generar_tablero(self):
		"""Con la lista de tarjetas arma el tablero"""
		tarjetas = self.tarjetas.copy()
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
		self.repartir_tarjetas_equipos()

	def repartir_tarjetas_equipos(self):
		"""Compara la llave con el tablero y le pasa a cada equipo sus tarjetas"""
		dic_tarjetas = {"rojo": [], "azul": []}
		for index_y, valor_y in enumerate(self.llave):
			for index_x, valor_x in enumerate(valor_y):
				if valor_x == "rojo" or valor_x == "azul":
					dic_tarjetas[valor_x].append(self.tablero[index_y][index_x])
		for equipo in self.equipos:
			equipo.tarjetas_faltantes = dic_tarjetas[equipo.nombre]
			equipo.tarjetas_totales = len(dic_tarjetas[equipo.nombre])
			equipo.tarjetas_encontradas = []

	def pedir_pista(self, pista):
		"""Recibe una pista en formato de (string, numero) y la agrega en el juego para ser validada y la lista del equipo"""
		if not type(pista[0]) == str or not type(pista[1]) == int:
			raise Exception("Pista no tiene formato valido")
		self.ultima_pista = pista
		# Agrega la pista al equipo que le corresponde el turno
		self.turno.pistas.append(pista[0])

	def pista_es_valida(self):
		"""Devuelve un booleano diciendo si la ultima pista pasada es valida o no"""
		# TODO: Mejorar validacion
		trampa = self.ultima_pista[0] in self.tarjetas
		if not trampa:
			self.pasar_turno = False
		return not trampa

	def encontrar_en_tablero(self, tarjeta):
		"""Recibe el nombre de una tarjeta y devuelve su posicion en el tablero"""
		for index_y, valor_y in enumerate(self.tablero):
			if not tarjeta in valor_y:
				continue
			for index_x, valor_x in enumerate(valor_y):
				if valor_x == tarjeta:
					return (index_x, index_y)

	def penalizar(self):
		"""En caso de trampa se le otorgara una tarjeta al azar al proximo equipo"""
		index_tramposo = self.equipos.index(self.turno)
		otro_equipo = self.equipos[1 if index_tramposo == 0 else 0]
		tarjeta_faltante_random = otro_equipo.seleccionar_tarjeta_random()
		x, y = self.encontrar_en_tablero(tarjeta_faltante_random)
		self.tablero[y][x] = ""

	def siguiente_turno(self):
		"""Cambia el turno para el proximo equipo"""
		index = self.equipos.index(self.turno)
		self.turno = self.equipos[1 if index == 0 else 0]
		self.pasar_turno = True

	def pedir_agente(self, coordenadas):
		"""Recibe las coordenadas x e y del tablero"""
		x, y = coordenadas
		valor = self.llave[y][x]
		tarjeta = self.tablero[y][x]
		if tarjeta == "ROJO" or tarjeta == "AZUL":
			self.pedir_agente(esperar_eleccion())
		else:
			self.tablero[y][x] = self.turno.nombre.upper()
			self.puntuar_equipo(valor, tarjeta)
		self.ultima_pista[1] -= 1

	def puntuar_equipo(self, valor, tarjeta):
		"""Recibe un valor (string) y puntua al equipo y pasa de ronda si necesario"""
		# TODO: Repartir acciones en varias funciones
		if self.turno.nombre == valor:
			# Sumar valor y tarjeta a encontradas
			self.turno.puntos += 1
			self.turno.agregar_tarjeta_adivinada(tarjeta)
			# print(f"Cartas totales {self.turno.tarjetas_totales}")
			# print(f"Cartas encontradas len {len(self.turno.tarjetas_encontradas)}")
			if self.turno.tarjetas_totales == len(self.turno.tarjetas_encontradas):
				gamelib.play_sound("musica/sfrondafinalizada.wav")
				gamelib.say(f"Ronda finalizada!\nEl equipo {self.turno.nombre} encontró a todos sus agentes")
				self.siguiente_turno()
				self.finalizar_ronda()
			if self.ultima_pista[1] == 0:
				self.siguiente_turno()
		elif valor == "asesino":
			# menor 5 puntos y termina juego
			encontrado_asesino()
			self.turno.puntos -= 5
			self.siguiente_turno()
			self.finalizar_ronda()
		elif valor == "civil":
			# menor un punto y siguiente turno
			self.turno.puntos -= 1
			self.siguiente_turno()
		else:
			# Sumar punto y tarjeta al otro equipo y siguiente turno
			index = self.equipos.index(self.turno)
			otro_equipo = self.equipos[1 if index == 0 else 0]
			otro_equipo.puntos += 1
			otro_equipo.agregar_tarjeta_adivinada(tarjeta)
			if otro_equipo.tarjetas_totales == len(otro_equipo.tarjetas_encontradas):
				gamelib.play_sound("musica/sfrondafinalizada.wav")
				gamelib.say(f"Ronda finalizada!\nEl equipo {otro_equipo.nombre} encontró a todos sus agentes")
				self.finalizar_ronda()
			self.siguiente_turno()

	def seleccionar_spymaster(self):
		"""Seleccionar un spymaster para cada equipo"""
		for equipo in self.equipos:
			equipo.elegir_spymaster()

	def inicializar_rondas(self):
		"""Inicializa la ronda"""
		self.ronda_terminada = False

	def finalizar_ronda(self):
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
		print(self.tarjetas_faltantes)
		index_tarjeta = self.tarjetas_faltantes.index(tarjeta)
		if index_tarjeta >= 0:
			self.tarjetas_faltantes.pop(index_tarjeta)
			self.tarjetas_encontradas.append(tarjeta)

	def seleccionar_tarjeta_random(self):
		"""Devuelve una tarjeta faltante de forma aleatoria"""
		tarjeta = random.choice(self.tarjetas_faltantes)
		self.agregar_tarjeta_adivinada(tarjeta)
		return tarjeta


gamelib.init(main)
