import random
import gamelib

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
X_TEXTO_TARJETA, Y_TEXTO_TARJETA = 40, 43
X_TEXTO_PIZARRON, Y_TEXTO_PIZARRON = 123, 80
X_SLOT_LLAVE, Y_SLOT_LLAVE = 31, 28
STEP_X_TARJETA, STEP_Y_TARJETA = 80, 50
STEP_X_SLOT, STEP_Y_SLOT = 40, 40
SEP_TARJETA = 4


def main():
    juego = Juego()
    # jugadores = gamelib.input("Listar todos los jugadores\nSepararlos por coma")
    jugadores = "facu, fede, juan, diego"
    juego.agregar_jugadores(jugadores)
    juego.iniciar()
    gamelib.resize(ANCHO_VENTANA_JUEGO, ALTO_VENTANA_JUEGO)
    while gamelib.is_alive() and not juego.terminado:
        gamelib.draw_begin()
        juego.obtener_tarjetas("tarjetas.txt")
        juego.generar_tablero()
        juego.generar_llave()
        mostrar_estado_juego(juego)
        mostrar_llave(juego)
        while not juego.ronda_terminada:
            print(f"Turno de equipo {juego.turno.nombre}")
            pista = gamelib.input("Ingresar pista:")
            pista = pista.split()
            print(pista)
            pista[0] = pista[0].upper()
            pista[1] = int(pista[1])
            juego.pedir_pista(pista)
            if not juego.pista_es_valida():
                juego.penalizar()
            # Pedir agente hasta equivocarse o hasta que se terminen las chances
            while not juego.pasar_turno:
                juego.pedir_agente(esperar_eleccion())
    # mostrar_ganador(juego)


# def main():
#     juego = Juego()
#     juego.iniciar()
#     gamelib.resize(ANCHO_VENTANA_JUEGO, ALTO_VENTANA_JUEGO)
#     while gamelib.is_alive() and not juego.terminado:
#         mostrar_estado_juego(juego)
#         juego.obtener_tarjetas("tarjetas.txt")
#         juego.generar_tablero()
#         juego.generar_llave()
#         juego.seleccionar_spymaster()
#         juego.inicializar_rondas()
#         while not juego.ronda_terminada:
#             mostrar_estado_juego(juego)
#             mostrar_llave()
#             juego.pedir_pista()
#             if not juego.pista_es_valida():
#                 juego.penalizar()
#             # Pedir agente hasta equivocarse o hasta que se terminen las chances
#             while juego.seguir_turno:
#                 juego.pedir_agente()
#     # mostrar_ganador(juego)


def mostrar_estado_juego(juego):
    mostrar_fondo()
    mostrar_tablero(juego)
    for indice_fil, fil in enumerate(juego.tablero):
        for indice_col, col in enumerate(fil):
            if col == "":
                genero = random.choice(("m", "f"))
                elemento = juego.llave[indice_fil][indice_col]
                gamelib.draw_image(
                    f"imagenes/tarjeta{elemento}{genero}.gif",
                    X_LLAVE + indice_col * STEP_X_SLOT,
                    Y_LLAVE + indice_fil * STEP_Y_SLOT,
                )


def mostrar_fondo():
    gamelib.draw_image("imagenes/fondo.gif", 1, 1)


def mostrar_tablero(juego):

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
                + 13,
                Y_TABLERO
                + indice_fil * (STEP_Y_TARJETA + SEP_TARJETA)
                + Y_TEXTO_TARJETA
                - 28,
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
            Y_PIZARRON_ROJO + Y_TEXTO_PIZARRON,
        )

    if juego.turno.nombre == "azul":
        str_pistas = "\n".join(juego.turno.pista)
        gamelib.draw_image(
            "imagenes/pizarronazul.gif", X_PIZARRON_AZUL, Y_PIZARRON_AZUL
        )
        gamelib.draw_text(
            str_pistas,
            X_PIZARRON_AZUL + X_TEXTO_PIZARRON,
            Y_PIZARRON_AZUL + Y_TEXTO_PIZARRON,
        )


def mostrar_llave(juego):
    """Funcion que recibe el estado del juego y muestra la llave del juego"""
    gamelib.draw_image(
        f"imagenes/llave{juego.primer_equipo.nombre}.gif", X_LLAVE, Y_LLAVE
    )
    print(juego.llave)
    for indice_fil, fil in enumerate(juego.llave):
        for indice_col, col in enumerate(fil):
            gamelib.draw_image(
                f"imagenes/slot{col}.gif",
                X_LLAVE + X_SLOT_LLAVE + indice_col * STEP_X_SLOT,
                Y_LLAVE + Y_SLOT_LLAVE + indice_fil * STEP_Y_SLOT,
            )


def esperar_eleccion():
    """Funcion que sirve para esperar el click del usuario cuando elige el agente"""

    evento = gamelib.wait(gamelib.EventType.ButtonPress)
    if (
        X_TABLERO < evento.x < X_TABLERO + TABLERO_ANCHO * STEP_X_TARJETA
        and Y_TABLERO < evento.y < Y_TABLERO + TABLERO_ALTO * STEP_Y_TARJETA
    ):
        x, y = (evento.x - X_TABLERO) // STEP_X_TARJETA, (
            evento.y - Y_TABLERO
        ) // STEP_Y_TARJETA
    return (x, y)


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
        print(f"trampa: {trampa}")
        if not trampa:
            self.pasar_turno = False
        return not trampa

    def encontrar_en_tablero(self, tarjeta):
        """Recibe el nombre de una tarjeta y devuelve su posicion en el tablero"""
        for y in self.tablero:
            if not tarjeta in y:
                continue
            for x in y:
                if x == tarjeta:
                    return (x, y)

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
        self.tablero[y][x] = ""
        self.puntuar_equipo(valor, tarjeta)
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
                self.siguiente_turno()
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
