import pygame
import const
from boton import Boton
import LEXIRETO  # Importamos los módulos de los juegos
import LETRAS

class Juego:
    def __init__(self):
        pygame.init()
        self.run, self.play = True, False
        self.Ancho, self.Largo = const.width, const.length
        pygame.display.set_caption('Palabrerío')
        self.ventana = pygame.display.set_mode((self.Ancho, self.Largo))

        # Fondo
        imagen_fon = pygame.image.load('fondos/fondo3.png')
        self.fon = pygame.transform.scale(imagen_fon, (const.width, const.length))

        # Fuente
        self.titulo_fuente = pygame.font.SysFont('PressStart2P-Regular', const.tamano_letra_titulo)
        self.titulo_opciones = pygame.font.SysFont('PressStart2P-Regular', const.tamano_letra_subtitulos)
        self.i = 0  # Posicion del fondo

        # Botones
        self.botones = [
            Boton('Lexireto', self.titulo_opciones, const.blanco,
                  const.color_opciones, const.posicion_lexireto),
            Boton('Letras', self.titulo_opciones, const.blanco,
                  const.color_opciones, const.posicion_letras),
            Boton('Salir', self.titulo_opciones, const.blanco,
                  const.color_opciones, const.posicion_salir),
        ]

    def mover_fondo(self):
        self.i -= 0.5
        if self.i <= -self.Ancho:
            self.i = 0
        self.ventana.fill(const.negro)
        self.ventana.blit(self.fon, (self.i, 0))
        self.ventana.blit(self.fon, (self.Ancho + self.i, 0))

    def bucle_juego(self):
        while self.play:
            self.check_eventos()
            self.mover_fondo()
            self.crea_titulo('PressStart2P-Regular', const.nombre_juego,
                             const.negro, const.blanco, const.posicion_titulo2, const.posicion_titulo)

            mouse_pos = pygame.mouse.get_pos()
            for boton in self.botones:
                boton.dibujar(self.ventana, mouse_pos)

            pygame.display.update()

    def check_eventos(self):
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                self.run, self.play = False, False
                pygame.quit()
                quit()
            if eventos.type == pygame.MOUSEBUTTONDOWN and eventos.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for boton in self.botones:
                    if boton.clic(mouse_pos):
                        if boton.texto == 'Lexireto':
                            self.ejecutar_lexireto()
                        elif boton.texto == 'Letras':
                            self.ejecutar_letras()
                        elif boton.texto == 'Salir':
                            self.run, self.play = False, False
                            pygame.quit()
                            quit()

    def ejecutar_lexireto(self):
        """Ejecuta el juego Lexireto"""
        self.play = False  # Pausamos el menú principal
        LEXIRETO.main()  # Ejecutamos Lexireto
        self.play = True  # Volvemos al menú principal al terminar
        # Restablecemos la pantalla
        self.ventana = pygame.display.set_mode((self.Ancho, self.Largo))

    def ejecutar_letras(self):
        """Ejecuta el juego Letras"""
        self.play = False  # Pausamos el menú principal
        LETRAS.jugar_sopa_letras()  # Ejecutamos Letras
        self.play = True  # Volvemos al menú principal al terminar
        # Restablecemos la pantalla
        self.ventana = pygame.display.set_mode((self.Ancho, self.Largo))

    def crea_titulo(self, letra, nombrejuego, colorsombra, colortitulo, posicionsombra, posiciontitulo):
        fuente_titulo = pygame.font.SysFont(letra, const.tamano_letra_titulo)
        titulo1 = fuente_titulo.render(nombrejuego, True, colorsombra)
        self.ventana.blit(titulo1, posicionsombra)
        titulo = fuente_titulo.render(nombrejuego, True, colortitulo)
        self.ventana.blit(titulo, posiciontitulo)

