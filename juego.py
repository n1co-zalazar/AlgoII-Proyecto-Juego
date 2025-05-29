import pygame

import const


class Juego:
    def __init__(self):
        pygame.init()
        self.run, self.play = True, False
        self.clicDerecho, self.clicIzquierdo = False, False


        imagen_fon = pygame.image.load('fondos/fondo3.png') #nombre del archivo imagen
        self.fon = pygame.transform.scale(imagen_fon, (const.width, const.length))  # ajustamos la imagen a la ventana

        self.Ancho, self.Largo = const.width, const.length
        pygame.display.set_caption('Palabrerío')
        self.ventana = pygame.display.set_mode((self.Ancho, self.Largo))

        self.nombre_fuente = 'PressStart2P-Regular'
        self.mouse_posicion = (0,0)
        self.i = 0

    def actualizar_mouse_posicion(self):
        self.mouse_posicion = pygame.mouse.get_pos()

    def mover_fondo(self):
        """Actualiza la posición del fondo para el efecto de desplazamiento continuo."""
        # Decrementamos el índice para mover hacia la izquierda
        self.i -= 0.5

        # Reiniciar la posición del fondo cuando llegue al final
        if self.i <= -self.Ancho:
            self.i = 0

        # Dibujar el fondo en movimiento
        self.ventana.fill(const.negro)
        self.ventana.blit(self.fon, (self.i, 0))
        self.ventana.blit(self.fon, (self.Ancho + self.i, 0))

    def bucle_juego (self):
        while self.play:
            self.actualizar_mouse_posicion()
            self.check_eventos()

            self.mover_fondo()
            self.crea_titulo('PressStart2P-Regular', const.nombre_juego, const.negro, const.blanco,
                                const.posicion_titulo2, const.posicion_titulo)
            self.crea_subtitulo(const.nombre_lexireto, 'PressStart2P-Regular', const.posicion_sub_lexireto,
                                const.posicion_lexireto, const.negro, const.blanco)
            self.crea_subtitulo(const.nombre_letras, 'PressStart2P-Regular', const.posicion_sub_letras,
                                const.posicion_letras, const.negro, const.blanco)
            self.crea_subtitulo(const.nombre_salir, 'PressStart2P-Regular', const.posicion_sub_salir,
                                const.posicion_salir, const.negro, const.blanco)

            pygame.display.update()

    def check_eventos(self):
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                self.run, self.play = False, False

            if eventos.type == pygame.MOUSEBUTTONDOWN and eventos.button == 1:
                print("Hiciste clic con el mouse en ", self.mouse_posicion)

    def crea_titulo(self,letra, nombrejuego, colorsombra, colortitulo, posicionsombra, posiciontitulo):
        fuente_titulo = pygame.font.SysFont(letra, const.tamano_letra_titulo)

        titulo1 = fuente_titulo.render(nombrejuego, True, colorsombra)
        self.ventana.blit(titulo1, posicionsombra)

        titulo = fuente_titulo.render(nombrejuego, True, colortitulo)
        self.ventana.blit(titulo, posiciontitulo)

    def crea_subtitulo(self, nombre, letra, posicion_sombra, posicion_titulo, color_sombra, color_titulo):
        fuente_subtitulo = pygame.font.SysFont(letra, const.tamano_letra_subtitulos)

        subtitulo1 = fuente_subtitulo.render(nombre, True, color_sombra)
        self.ventana.blit(subtitulo1, posicion_sombra)
        subtitulo = fuente_subtitulo.render(nombre, True, color_titulo)
        self.ventana.blit(subtitulo, posicion_titulo)



