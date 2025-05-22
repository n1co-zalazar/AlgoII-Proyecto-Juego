import pygame
import random
import sys
import time
from collections import defaultdict

# --- CONFIGURACIÓN ---
PALABRAS = ["automovil", "sube", "puerta", "viaje", "miel", "luz", "vida"]  # Ejemplo
FILAS, COLUMNAS = 6, 6  # Tamaño matriz
TAM_CELDA = 50

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (100, 149, 237)
VERDE = (34, 139, 34)
ROJO = (200, 0, 0)
GRIS = (200, 200, 200)

DIRECCIONES = [(-1,0),(1,0),(0,-1),(0,1)]  # Arriba, abajo, izquierda, derecha

# Inicializar Pygame
pygame.init()
WIDTH = COLUMNAS * TAM_CELDA + 300  # Espacio para lista de palabras
HEIGHT = FILAS * TAM_CELDA + 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sopa de Letras Serpiente - Superposición")
fuente = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

# --- FUNCIONES AUXILIARES ---
def crear_matriz(filas, columnas):
    return [[" " for _ in range(columnas)] for _ in range(filas)]

def es_valido(fila, col):
    return 0 <= fila < FILAS and 0 <= col < COLUMNAS

def puede_colocar(matriz, fila, col, letra):
    return es_valido(fila, col) and (matriz[fila][col] == " " or matriz[fila][col] == letra)

def buscar_ruta_serpiente(matriz, palabra, index, fila, col, visitados):
    if index == len(palabra):
        return []

    letra = palabra[index]
    for dx, dy in random.sample(DIRECCIONES, len(DIRECCIONES)):
        nf, nc = fila + dx, col + dy
        if puede_colocar(matriz, nf, nc, letra) and (nf, nc) not in visitados:
            visitados.add((nf, nc))
            sub_ruta = buscar_ruta_serpiente(matriz, palabra, index + 1, nf, nc, visitados)
            if sub_ruta is not None:
                return [(nf, nc)] + sub_ruta
            visitados.remove((nf, nc))
    return None

def intentar_colocar_palabra(matriz, palabra):
    palabra = palabra.upper()
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if puede_colocar(matriz, fila, col, palabra[0]):
                visitados = {(fila, col)}
                ruta = buscar_ruta_serpiente(matriz, palabra, 1, fila, col, visitados)
                if ruta is not None:
                    ruta_completa = [(fila, col)] + ruta
                    for (f, c), letra in zip(ruta_completa, palabra):
                        matriz[f][c] = letra
                    return ruta_completa
    return None

def rellenar_espacios(matriz):
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if matriz[i][j] == " ":
                matriz[i][j] = random.choice(letras)

def dibujar(matriz, seleccionadas, resaltado_ruta):
    screen.fill(BLANCO)
    max_letras = max(len(p) for p in PALABRAS)
    tamaño_fuente = min(TAM_CELDA - 10, 50 - max(0, (max_letras - 5) * 2))
    fuente_celda = pygame.font.SysFont(None, tamaño_fuente)

    for i in range(FILAS):
        for j in range(COLUMNAS):
            letra = matriz[i][j]
            x, y = j * TAM_CELDA, i * TAM_CELDA
            rect = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)
            if resaltado_ruta and (i, j) in resaltado_ruta:
                pygame.draw.rect(screen, VERDE, rect)
            elif (i, j) in seleccionadas:
                pygame.draw.rect(screen, AZUL, rect)
            else:
                pygame.draw.rect(screen, NEGRO, rect, 1)

            texto = fuente_celda.render(letra, True, NEGRO)
            text_rect = texto.get_rect(center=rect.center)
            screen.blit(texto, text_rect)

    palabra_actual = "".join([matriz[i][j] for i, j in seleccionadas])
    texto_palabra = fuente.render(f"Palabra: {palabra_actual}", True, ROJO)
    screen.blit(texto_palabra, (10, HEIGHT - 90))

    segundos = int(time.time() - inicio_tiempo)
    texto_tiempo = fuente.render(f"Tiempo: {segundos} seg", True, NEGRO)
    screen.blit(texto_tiempo, (10, HEIGHT - 30))

    pistas_agrupadas = defaultdict(list)
    for palabra in PALABRAS:
        pistas_agrupadas[len(palabra)].append(palabra.upper())

    # Mostrar palabras en el costado con estilo mejorado
    x_base = COLUMNAS * TAM_CELDA + 20
    y_base = 20
    espaciado_linea = 28
    sangría = 20

    for longitud in sorted(pistas_agrupadas.keys(), reverse=True):
        subtitulo = fuente.render(f"Palabras de {longitud} letras:", True, NEGRO)
        screen.blit(subtitulo, (x_base, y_base))
        y_base += espaciado_linea

        for palabra in pistas_agrupadas[longitud]:
            palabra_encontrada = palabra in palabras_encontradas

            if palabra_encontrada:
                texto = fuente.render(palabra, True, VERDE)
            else:
                progreso = ""
                progreso_palabra = pistas_progreso.get(palabra, "")
                if progreso_palabra:
                    for i, c in enumerate(progreso_palabra):
                        if i < len(palabra) and c == palabra[i]:
                            progreso += c + " "
                        else:
                            progreso += "_ "
                else:
                    progreso = palabra[0] + " " + "_ " * (len(palabra) - 1)
                texto = fuente.render(progreso.strip(), True, NEGRO)

            screen.blit(texto, (x_base + sangría, y_base))
            y_base += espaciado_linea

    pygame.display.flip()

def obtener_celda(pos):
    x, y = pos
    fila, col = y // TAM_CELDA, x // TAM_CELDA
    if fila >= FILAS or col >= COLUMNAS:
        return None
    return fila, col

def menu_inicio():
    screen.fill(GRIS)
    titulo = fuente.render("Sopa de Letras Serpiente Superpuesta", True, NEGRO)
    instruccion = fuente.render("Presiona cualquier tecla para comenzar", True, NEGRO)
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 40))
    screen.blit(instruccion, (WIDTH//2 - instruccion.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                esperando = False

def pantalla_fin():
    screen.fill(GRIS)
    tiempo_final = int(time.time() - inicio_tiempo)
    mensaje = fuente.render("\u00a1Felicidades! Encontraste todas las palabras.", True, NEGRO)
    tiempo = fuente.render(f"Tiempo total: {tiempo_final} segundos", True, NEGRO)
    instruccion = fuente.render("Presiona cualquier tecla para salir", True, NEGRO)
    screen.blit(mensaje, (WIDTH//2 - mensaje.get_width()//2, HEIGHT//2 - 60))
    screen.blit(tiempo, (WIDTH//2 - tiempo.get_width()//2, HEIGHT//2 - 30))
    screen.blit(instruccion, (WIDTH//2 - instruccion.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                esperando = False

def generar_sopa_serpiente_superpuesta(palabras):
    matriz = crear_matriz(FILAS, COLUMNAS)
    rutas = {}
    for palabra in palabras:
        ruta = intentar_colocar_palabra(matriz, palabra)
        if ruta is None:
            raise Exception(f"No se pudo colocar la palabra {palabra}")
        rutas[palabra.upper()] = ruta
    rellenar_espacios(matriz)
    return matriz, rutas

def son_adyacentes(celdas):
    for i in range(len(celdas) - 1):
        f1, c1 = celdas[i]
        f2, c2 = celdas[i + 1]
        if abs(f1 - f2) + abs(c1 - c2) != 1:
            return False
    return True

# --- JUEGO PRINCIPAL ---
menu_inicio()
try:
    matriz, rutas_palabras = generar_sopa_serpiente_superpuesta(PALABRAS)
except Exception as e:
    print(e)
    pygame.quit()
    sys.exit()

seleccionadas = []
resaltado_ruta = None
palabras_encontradas = []
pistas_progreso = {}
inicio_tiempo = time.time()

corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            celda = obtener_celda(pygame.mouse.get_pos())
            if celda and celda not in seleccionadas:
                if not seleccionadas or any(abs(celda[0]-f)+abs(celda[1]-c) == 1 for f,c in [seleccionadas[-1]]):
                    seleccionadas.append(celda)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                palabra_actual = "".join([matriz[i][j] for i,j in seleccionadas])
                if son_adyacentes(seleccionadas):
                    for palabra, ruta in rutas_palabras.items():
                        if palabra_actual == palabra and palabra not in palabras_encontradas:
                            palabras_encontradas.append(palabra)
                            pistas_progreso[palabra] = palabra
                            break
                seleccionadas = []
                resaltado_ruta = None
            elif event.key == pygame.K_BACKSPACE:
                if seleccionadas:
                    seleccionadas.pop()

    dibujar(matriz, seleccionadas, resaltado_ruta)

    if len(palabras_encontradas) == len(PALABRAS):
        pantalla_fin()
        corriendo = False

    clock.tick(30)

pygame.quit()
sys.exit()


