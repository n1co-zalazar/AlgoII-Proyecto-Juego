import sys
import pygame
import math
import random
import itertools

pygame.init()
#size ventana
ANCHO = 800
ALTO = 600
#colores
BLANCO = (255,255,255)
NEGRO = (0,0,0)
AMARILLO = (255,204,0)
GRIS = (200,200,200)
AZUL = (100,150,255)
scroll_offset = 0
#generar letras validas
def generar_letras_validas(diccionario_path):
    with open(diccionario_path, "r", encoding="utf-8") as f:
        palabras = [line.strip().upper() for line in f if len(line.strip()) >= 3]

    letras_usadas = set("".join(palabras))
    combinaciones = list(itertools.combinations(letras_usadas, 7))
    random.shuffle(combinaciones)

    for letras in combinaciones:
        letras = list(letras)
        letras_set = set(letras)
        for letra_central in letras:
            palabras_validas_ = set()
            iniciales_con_palabra = set()
            tiene_pangrama = False

            for palabra in palabras:
                if (
                    set(palabra).issubset(letras_set) and
                    letra_central in palabra and
                    palabra[0] in letras_set
                ):
                    palabras_validas_.add(palabra)
                    iniciales_con_palabra.add(palabra[0])
                    if set(letras_set).issubset(set(palabra)):
                        tiene_pangrama = True

            # Verificar condiciones
            if len(palabras_validas_) > 0 and \
               all(letra in iniciales_con_palabra for letra in letras) and \
               tiene_pangrama:
                return letras, letra_central, palabras_validas_

    return None, None, set()

# Cargar las palabras validas desde un archivo de texto
def cargar_palabras_validas(archivo, letras, letra_central):
    letras_set = set(letras)
    palabras_filtradas = set()
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                palabra = linea.strip().upper()
                if (
                    len(palabra) >= 3 and
                    set(palabra).issubset(letras_set) and
                    letra_central in palabra and
                    palabra[0] in letras_set
                ):
                    palabras_filtradas.add(palabra)
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado.")
    return palabras_filtradas
#letras validas
LETRAS, LETRA_CENTRAL, palabras_validas = generar_letras_validas("diccionario_sin_acentos.txt")
if not LETRAS:
    print("No se pudo generar un conjunto válido de letras.")
    sys.exit()
# imprimir palabras validas al inicio
print("\n=== Palabras válidas para esta ronda ===")
print(f"Letras disponibles: {', '.join(LETRAS)}")
print(f"Letra central requerida: {LETRA_CENTRAL}\n")
print("Lista completa de palabras válidas:")
for i, palabra in enumerate(sorted(palabras_validas), 1):
    print(f"{i}. {palabra}")
print(f"\nTotal: {len(palabras_validas)} palabras válidas.\n")
# Inicializar palabras encontradas
palabras_encontradas = {
    letra: {
        'palabras': [],
        'contador': 0,
        'total': 0
    } for letra in LETRAS
}

# Calcular los totales por letra
for letra in LETRAS:
    palabras_encontradas[letra]['total'] = sum(
        1 for palabra in palabras_validas
        if palabra.startswith(letra) and LETRA_CENTRAL in palabra
    )
todas_encontradas = set() #para evitar palabras duplicadas
# Lista para guardar palabras aceptadas (para imprimir al final)
lista_palabras_encontradas = []
#fuente para las letras
FUENTE = pygame.font.SysFont(None,40)
FUENTE_BOTON = pygame.font.SysFont(None, 32)
#ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Lexireto")
seleccionados = []#letras seleccionadas
reloj = pygame.time.Clock()
#-----------------------------------------Funciones dibujos---------------------------------------------------------------------------
def obtener_puntos_hexagono(cx,cy,radio):
    puntos = []
    for i in range(6):
        angulo = math.radians(60 * i - 30)
        x = cx + radio * math.cos(angulo)
        y = cy + radio * math.sin(angulo)
        puntos.append((x,y))
    return puntos

def obtener_posiciones_hexagonos(cx,cy,distancia):
    posiciones = [
        (cx, cy),  # centro
        (cx + distancia, cy),  # derecha
        (cx - distancia, cy),  # izquierda
        (cx + distancia / 2, cy - distancia * math.sin(math.radians(60))),  # arriba derecha
        (cx - distancia / 2, cy - distancia * math.sin(math.radians(60))),  # arriba izquierda
        (cx + distancia / 2, cy + distancia * math.sin(math.radians(60))),  # abajo derecha
        (cx - distancia / 2, cy + distancia * math.sin(math.radians(60))),  # abajo izquierda
    ]
    return posiciones

def punto_en_poligono(px,py,poligono):
    dentro = False
    j = len(poligono) - 1
    for i in range(len(poligono)):
        xi, yi = poligono[i]
        xj, yj = poligono[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi + 1e-10) + xi):
            dentro = not dentro
        j = i
    return dentro

def obtener_palabra_actual():
    return "".join(seleccionados)

def dibujar_boton(texto, x, y, ancho, alto, mouse_pos):
    rect = pygame.Rect(x, y, ancho, alto)
    if rect.collidepoint(mouse_pos):
        color = AZUL
    else:
        color = BLANCO
    pygame.draw.rect(ventana, color, rect, border_radius=5)
    pygame.draw.rect(ventana, NEGRO, rect, 2, border_radius=5)
    texto_render = FUENTE_BOTON.render(texto, True, NEGRO)
    ventana.blit(texto_render, texto_render.get_rect(center=rect.center))
    return rect
#----------------------------------Funciones algoritmos-----------------------------------------------------------
def palabra_es_valida(palabra, letras, letra_central):
    if len(palabra) < 3:
        return False
    if palabra[0] not in letras:  # debe comenzar con una letra del panal
        return False
    if letra_central not in palabra:  # debe contener la letra central
        return False
    if not set(palabra).issubset(set(letras)):  # las letras deben estar en el panal, repeticiones permitidas
        return False
    if palabra not in palabras_validas:  # debe estar en el diccionario
        return False
    return True


def aplicar_palabra():
    palabra = obtener_palabra_actual()
    letra_central = LETRA_CENTRAL

    if len(palabra) < 3:
        mostrar_mensaje("Palabra demasiado corta", (200, 0, 0))
        return False

    if letra_central not in palabra:
        mostrar_mensaje("Falta la letra central", (255, 102, 0))  # naranja
        return False

    if (palabra_es_valida(palabra, LETRAS, letra_central) and
            palabra not in todas_encontradas):
        letra_inicial = palabra[0]
        palabras_encontradas[letra_inicial]['palabras'].append(palabra)
        todas_encontradas.add(palabra)
        lista_palabras_encontradas.append(palabra)  # Agregar a la lista final
        seleccionados.clear()
        mostrar_mensaje("¡Palabra aceptada!", (0, 200, 0))
        return True

    mostrar_mensaje("Palabra no valida", (200, 0, 0))
    return False

def dibujar_palabras_encontradas():
    global scroll_offset
    x_inicio = 680
    y_inicio = 20
    area_altura = 500
    contenido_altura = 0

    # Calcular altura total del contenido
    for letra in LETRAS:
        contenido_altura += 30 + len(palabras_encontradas[letra]['palabras']) * 25 + 15

    # Ajustar scroll offset
    scroll_offset = max(0, min(scroll_offset, contenido_altura - area_altura))

    # Crear superficie para el contenido
    superficie_contenido = pygame.Surface((200, contenido_altura))
    superficie_contenido.fill(BLANCO)
    offset_y = -scroll_offset

    #dibujar
    for letra in LETRAS:
        info = palabras_encontradas[letra]
        texto = FUENTE.render(f"{letra}: {len(info['palabras'])}/{info['total']}", True, NEGRO)
        superficie_contenido.blit(texto, (0, offset_y))
        offset_y += 30

        for palabra in info["palabras"]:
            texto_palabra = FUENTE_BOTON.render(palabra, True, NEGRO)
            superficie_contenido.blit(texto_palabra, (20, offset_y))
            offset_y += 25

        offset_y += 15

    #dibujar solo la parte visible
    ventana.blit(superficie_contenido, (x_inicio, y_inicio), (0, scroll_offset, 200, area_altura))

    #dibujar barra de scroll
    if contenido_altura > area_altura:
        barra_height = int((area_altura ** 2) / contenido_altura)
        barra_pos = int((scroll_offset * (area_altura - barra_height)) / (contenido_altura - area_altura))
        pygame.draw.rect(ventana, GRIS, (880, y_inicio + barra_pos, 10, barra_height))


def mostrar_mensaje(mensaje, color):
    global mensaje_actual, color_mensaje, tiempo_mensaje_inicio
    mensaje_actual = mensaje
    color_mensaje = color
    tiempo_mensaje_inicio = pygame.time.get_ticks()

# Variables globales para el mensaje
mensaje_actual = ""
color_mensaje = NEGRO
tiempo_mensaje_inicio = 0
duracion_mensaje = 2000

def main():
    run = True
    #hallar el centro de la pantalla
    cx,cy = ANCHO//2, ALTO//2
    radio = 60
    distancia = radio * 2 * math.cos(math.radians(30))
    posiciones = obtener_posiciones_hexagonos(cx,cy,distancia)
    hexagonos = [obtener_puntos_hexagono(x,y,radio) for (x,y) in posiciones]
    tiempo_inicio = pygame.time.get_ticks()  # cronometro
    global mensaje_actual, color_mensaje, tiempo_mensaje_inicio
    global scroll_offset
    #bucle principal
    while run:
#----------------------------Pantalla-------------------------------------------------------------------------------------------------
        ventana.fill(BLANCO)

        mx, my = pygame.mouse.get_pos()
        # Mostrar palabra formada
        texto_palabra = FUENTE.render("Palabra: " + obtener_palabra_actual(), True, NEGRO)
        ventana.blit(texto_palabra, (70, 90))  # posicion de mostrar palabra formada
        # dibujar los hexagonos
        for i, (x, y) in enumerate(posiciones):
            puntos = hexagonos[i]
            if punto_en_poligono(mx, my, puntos):
                color = AZUL
            elif i == 0:  # la primera letra es la del centro, verificar en posiciones
                color = AMARILLO
            else:
                color = BLANCO

            pygame.draw.polygon(ventana, color, puntos)
            pygame.draw.polygon(ventana, NEGRO, puntos, 2)  # borde
            # dibujar letras en Palabra:
            texto = FUENTE.render(LETRAS[i], True, NEGRO)
            rect = texto.get_rect(center=(x, y))
            ventana.blit(texto, rect)
        #dibujar botones
        boton_borrar_palabra = dibujar_boton("Borrar palabra", 130, 500, 180, 40, (mx, my))
        boton_borrar_letra = dibujar_boton("Borrar letra", 490, 500, 160, 40, (mx, my),)
        #llamda a funcion que dibuja las palabras encontradas
        dibujar_palabras_encontradas()
        #dibujar boton de "APLICAR"
        boton_aplicar_rect = dibujar_boton("Aplicar",340, 500, 120, 40,(mx,my))
        texto_aplicar = FUENTE_BOTON.render("Aplicar", True, NEGRO)
        rect_texto = texto_aplicar.get_rect(center=boton_aplicar_rect.center)
        ventana.blit(texto_aplicar, rect_texto)

#------------------------------------EVENTOS-------------------------------------------------------------------------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # mostrar palabras encontradas
                print("\n=== Palabras encontradas ===")
                for palabra in lista_palabras_encontradas:
                    print(palabra)
                print(f"\nTotal: {len(lista_palabras_encontradas)} palabras encontradas.")
                # Calcular palabras no encontradas
                palabras_no_encontradas = sorted(palabras_validas - set(lista_palabras_encontradas))
                # mostrar palabras no encontradas
                print("\n=== Palabras NO encontradas ===")
                for palabra in palabras_no_encontradas:
                    print(palabra)
                print(f"\nTotal: {len(palabras_no_encontradas)} palabras no encontradas.")
                run = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # click en boton de borrar palabra
                if boton_borrar_palabra.collidepoint(mx, my):
                    seleccionados.clear()
                # click en boton de borrar letra
                elif boton_borrar_letra.collidepoint(mx, my):
                    if seleccionados:
                        seleccionados.pop()
                # click en boton de aplicar
                elif boton_aplicar_rect.collidepoint(mx, my):
                    aplicar_palabra()
                else:
                    for i, poligono in enumerate(hexagonos):
                        if punto_en_poligono(mx, my, poligono):
                            seleccionados.append(LETRAS[i])
<<<<<<< HEAD
            elif evento.type == pygame.MOUSEWHEEL:
                scroll_offset -= evento.y * 30  #sensibilidad del scroll
                scroll_offset = max(0, scroll_offset)

# Calcular tiempo transcurrido en segundos
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_inicio) // 1000 #segundos
        minutos = tiempo_transcurrido // 60
        segundos = tiempo_transcurrido % 60
        texto_tiempo = FUENTE.render(f"Tiempo: {minutos:02d}:{segundos:02d}", True, NEGRO)
        ventana.blit(texto_tiempo, (10, 570))  #posicion


        # Mostrar mensaje si está activo
        if mensaje_actual:
            tiempo_ahora = pygame.time.get_ticks()
            if tiempo_ahora - tiempo_mensaje_inicio < duracion_mensaje:
                texto = FUENTE.render(mensaje_actual, True, color_mensaje)
                ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 30))
            else:
                mensaje_actual = ""  # Oculta el mensaje después del tiempo

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

main()
=======
pygame.display.quit
>>>>>>> 8efdb81d7d069fe4aeed1294f723f5cda2f9fe43
