import pygame
import random
import sys
import time
from collections import defaultdict

def jugar_sopa_letras(palabras=None, filas=7, columnas=7, tam_celda=65):
    """Función principal del juego de Sopa de Letras"""
    
    # Configuración del juego
    NUM_PALABRAS = 8
    MARGEN_DERECHO = 400
    MARGEN_INFERIOR = 150
    
    # Colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    AZUL = (100, 149, 237)
    VERDE = (34, 139, 34)
    ROJO = (200, 0, 0)
    GRIS = (200, 200, 200)
    
    DIRECCIONES = [(-1,0), (1,0), (0,-1), (0,1)]
    
    # Cargar palabras si no se proporcionan
    def cargar_palabras_desde_archivo(nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                return [linea.strip() for linea in f if linea.strip() and len(linea.strip()) >= 3]
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {nombre_archivo}")
            return ["PYTHON", "PROGRAMA", "SERPIENTE", "JUEGO", "CODIGO", "TECLADO", "VENTANA", "COMPUTADORA"]  # Palabras por defecto

    if palabras is None:
        palabras = cargar_palabras_desde_archivo("diccionariooficial.txt")
    
    if len(palabras) < NUM_PALABRAS:
        print(f"Error: No hay suficientes palabras de 3+ letras. Necesitas al menos {NUM_PALABRAS}.")
        return

    # Inicializar Pygame
    pygame.init()
    WIDTH = columnas * tam_celda + MARGEN_DERECHO
    HEIGHT = filas * tam_celda + MARGEN_INFERIOR
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sopa de Letras Serpiente - Superposición")
    fuente = pygame.font.SysFont('Arial', 36)
    fuente_celda = pygame.font.SysFont('Arial', tam_celda - 15)
    clock = pygame.time.Clock()

    # Funciones auxiliares
    def crear_matriz(filas, columnas):
        return [[" " for _ in range(columnas)] for _ in range(filas)]

    def es_valido(fila, col):
        return 0 <= fila < filas and 0 <= col < columnas

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
        for fila in range(filas):
            for col in range(columnas):
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
        for i in range(filas):
            for j in range(columnas):
                if matriz[i][j] == " ":
                    matriz[i][j] = random.choice(letras)

    def dibujar(matriz, seleccionadas):
        screen.fill(BLANCO)
        
        # Dibujar matriz
        for i in range(filas):
            for j in range(columnas):
                letra = matriz[i][j]
                x, y = j * tam_celda, i * tam_celda
                rect = pygame.Rect(x, y, tam_celda, tam_celda)
                
                if (i, j) in seleccionadas:
                    pygame.draw.rect(screen, AZUL, rect)
                else:
                    pygame.draw.rect(screen, NEGRO, rect, 1)

                texto = fuente_celda.render(letra, True, NEGRO)
                text_rect = texto.get_rect(center=rect.center)
                screen.blit(texto, text_rect)

        # Información del juego
        palabra_actual = "".join([matriz[i][j] for i, j in seleccionadas])
        texto_palabra = fuente.render(f"Palabra actual: {palabra_actual}", True, ROJO)
        screen.blit(texto_palabra, (10, HEIGHT - 130))

        segundos = int(time.time() - inicio_tiempo)
        texto_tiempo = fuente.render(f"Tiempo: {segundos}s | Encontradas: {len(palabras_encontradas)}/{len(PALABRAS)}", True, NEGRO)
        screen.blit(texto_tiempo, (10, HEIGHT - 90))

        # Panel de palabras
        x_base = columnas * tam_celda + 20
        y_base = 30
        titulo_panel = fuente.render("Palabras a encontrar:", True, NEGRO)
        screen.blit(titulo_panel, (x_base, y_base))
        y_base += 40

        palabras_por_longitud = defaultdict(list)
        for palabra in PALABRAS:
            palabras_por_longitud[len(palabra)].append(palabra)

        for longitud in sorted(palabras_por_longitud.keys(), reverse=True):
            texto_longitud = fuente.render(f"Palabras de {longitud} letras:", True, NEGRO)
            screen.blit(texto_longitud, (x_base, y_base))
            y_base += 30

            for palabra in palabras_por_longitud[longitud]:
                if palabra in palabras_encontradas:
                    texto = fuente.render(palabra, True, VERDE)
                else:
                    texto = fuente.render(f"{palabra[0]} {'-' * (longitud-1)}", True, NEGRO)
                screen.blit(texto, (x_base + 20, y_base))
                y_base += 30
            y_base += 10

        pygame.display.flip()

    def obtener_celda(pos):
        x, y = pos
        fila, col = y // tam_celda, x // tam_celda
        if fila >= filas or col >= columnas:
            return None
        return fila, col

    def menu_inicio():
        screen.fill(GRIS)
        titulo = fuente.render("Sopa de Letras Serpiente - Superposición", True, NEGRO)
        subtitulo = fuente.render(f"Encuentra {NUM_PALABRAS} palabras", True, NEGRO)
        instruccion = fuente.render("Presiona cualquier tecla para comenzar", True, NEGRO)
        
        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 60))
        screen.blit(subtitulo, (WIDTH//2 - subtitulo.get_width()//2, HEIGHT//2 - 20))
        screen.blit(instruccion, (WIDTH//2 - instruccion.get_width()//2, HEIGHT//2 + 20))
        
        pygame.display.flip()
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:
                    esperando = False
        return True

    def pantalla_fin():
        screen.fill(GRIS)
        tiempo_final = int(time.time() - inicio_tiempo)
        mensaje = fuente.render("¡FELICIDADES!", True, VERDE)
        subtitulo = fuente.render("Encontraste todas las palabras", True, NEGRO)
        tiempo = fuente.render(f"Tiempo total: {tiempo_final} segundos", True, NEGRO)
        instruccion = fuente.render("Presiona cualquier tecla para salir", True, NEGRO)
        
        screen.blit(mensaje, (WIDTH//2 - mensaje.get_width()//2, HEIGHT//2 - 80))
        screen.blit(subtitulo, (WIDTH//2 - subtitulo.get_width()//2, HEIGHT//2 - 40))
        screen.blit(tiempo, (WIDTH//2 - tiempo.get_width()//2, HEIGHT//2))
        screen.blit(instruccion, (WIDTH//2 - instruccion.get_width()//2, HEIGHT//2 + 60))
        
        pygame.display.flip()
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    esperando = False

    def generar_sopa_serpiente_superpuesta(lista_palabras, cantidad_objetivo):
        matriz = crear_matriz(filas, columnas)
        rutas = {}
        usadas = set()
        intentos = 0
        max_intentos = 1000

        while len(rutas) < cantidad_objetivo and intentos < max_intentos:
            palabra = random.choice(lista_palabras).upper()
            if palabra in usadas:
                intentos += 1
                continue
                
            ruta = intentar_colocar_palabra(matriz, palabra)
            if ruta:
                rutas[palabra] = ruta
                usadas.add(palabra)
            intentos += 1

        if len(rutas) < cantidad_objetivo:
            print(f"Advertencia: Solo se colocaron {len(rutas)} de {cantidad_objetivo} palabras")
        
        rellenar_espacios(matriz)
        return matriz, rutas

    def son_adyacentes(celdas):
        for i in range(len(celdas) - 1):
            f1, c1 = celdas[i]
            f2, c2 = celdas[i + 1]
            if abs(f1 - f2) + abs(c1 - c2) != 1:
                return False
        return True

    # Iniciar el juego
    if not menu_inicio():
        return

    try:
        matriz, rutas_palabras = generar_sopa_serpiente_superpuesta(palabras, NUM_PALABRAS)
        PALABRAS = list(rutas_palabras.keys())
    except Exception as e:
        print(f"Error al generar la sopa de letras: {e}")
        pygame.quit()
        return

    seleccionadas = []
    palabras_encontradas = []
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
                                break
                    seleccionadas = []
                elif event.key == pygame.K_BACKSPACE:
                    if seleccionadas:
                        seleccionadas.pop()

        dibujar(matriz, seleccionadas)

        if len(palabras_encontradas) == len(PALABRAS):
            pantalla_fin()
            corriendo = False

        clock.tick(30)

pygame.display.quit()
