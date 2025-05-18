import pygame
from pygame import MOUSEBUTTONDOWN

import const


pygame.init()

# Formateo de ventana
pygame.display.set_caption("Palabrerío")
ventana = pygame.display.set_mode((const.width, const.length))
imagen_fon = pygame.image.load('fondos/fondo3.png') #nombre del archivo imagen
fon = pygame.transform.scale(imagen_fon, (const.width, const.length)) #ajustamos la imagen a la ventana
i = 0   # Empieza en cero por default nada más.

#Texto
fuenteBitPrincipal = pygame.font.SysFont('PressStart2P-Regular', const.tamano_letra_titulo)
fuenteBitOpciones = pygame.font.SysFont('PressStart2P-Regular', const.tamano_letra_subtitulos)

run = True

while run:

    ventana.fill(const.negro)
    ventana.blit(fon, (i, 0))  # .blit es una función que nos ayuda a cargar una imagen en una superficie, en este caso sería en "Ventana"
    # El primer argumento es la imagen de fondo, el segundo son las coordenadas donde deseamos cargar.

    ventana.blit(fon, (const.width + i, 0))  # Volvemos a añadir la misma imagen porque si continuamos el bucle,
    # la imagen se va a congelar hacia infinito

    # Para añadir movimiento, creamos un índice fuera del bucle que desplazará la imagen hacia la izquierda.
    i -= 0.25  # Decrementamos el índice en cada iteración del while

    if i == -const.width:
        ventana.blit(fon, (const.width + i, 0))
        i = 0

    # Obtenemos la Posición del mouse
    mouse_posicion = pygame.mouse.get_pos()

    palabrerio1 = fuenteBitPrincipal.render(const.nombre_juego, True, const.negro)  # Se renderiza el texto, pero lo de arriba sería la sombra de la letrazx
    ventana.blit(palabrerio1, const.posicion_titulo2)  # Se muestra en pantalla
    palabrerio = fuenteBitPrincipal.render(const.nombre_juego, True, const.blanco)
    ventana.blit(palabrerio, const.posicion_titulo)

    lexireto1 = fuenteBitOpciones.render(const.nombre_lexireto, True, const.negro)
    ventana.blit(lexireto1, const.posicion_sub_lexireto)
    lexireto = fuenteBitOpciones.render(const.nombre_lexireto, True, const.blanco)
    ventana.blit(lexireto, const.posicion_lexireto)
    lexireto_cambio = lexireto.get_rect(center=const.posicion_lexireto)

    # Cambio de color al ubicar el cursor sobre la letra
    if lexireto_cambio.collidepoint(mouse_posicion):
        lexireto = fuenteBitOpciones.render(const.nombre_lexireto, True, const.color_opciones)
        ventana.blit(lexireto, const.posicion_lexireto)

    letras1 = fuenteBitOpciones.render(const.nombre_letras, True, const.negro)
    ventana.blit(letras1, const.posicion_sub_letras)
    letras = fuenteBitOpciones.render(const.nombre_letras, True, const.blanco)
    ventana.blit(letras, const.posicion_letras)
    letras_cambio = letras.get_rect(center=const.posicion_letras)

    # Cambio de color al ubicar el cursor sobre la letra
    if letras_cambio.collidepoint(mouse_posicion):
        letras = fuenteBitOpciones.render(const.nombre_letras, True, const.color_opciones)
        ventana.blit(letras, const.posicion_letras)

    salir1 = fuenteBitOpciones.render(const.nombre_salir, True, const.negro)
    ventana.blit(salir1, const.posicion_sub_salir)
    salir = fuenteBitOpciones.render(const.nombre_salir, True, const.blanco)
    ventana.blit(salir, const.posicion_salir)
    salir_cambio = salir.get_rect(center=const.posicion_salir)

    # Cambio de color al ubicar el cursor sobre la letra
    if salir_cambio.collidepoint(mouse_posicion):
        salir = fuenteBitOpciones.render(const.nombre_salir, True, const.color_opciones)
        ventana.blit(salir, const.posicion_salir)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False
        if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
            if lexireto_cambio.collidepoint(mouse_posicion):
                ventana.fill(const.negro)
            if letras_cambio.collidepoint(mouse_posicion):
                ventana.fill(const.blanco)
            if salir_cambio.collidepoint(mouse_posicion):

                run = False

    pygame.display.update()

pygame.quit()
