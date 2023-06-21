import pygame
from pygame.locals import *
import random

pygame.init()

# crea la ventana
width = 500
height = 500
tamaño_pantalla = (width, height)
pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption('juego de carreras')

# colores
gris = (100, 100, 100)
verde = (76, 208, 56)
rojo = (200, 0, 0)
blanco = (255, 255, 255)
amarillo = (255, 232, 0)

# tamaños de caminos y marcadores
ancho_carril = 300
ancho_marcador = 10
alto_marcador = 50

# coordenadas de carril
carril_izquierdo = 150
carril_centro = 250
carril_derecho = 350
carriles = [carril_izquierdo, carril_centro, carril_derecho]

# marcadores de carril y borde
camino = (100, 0, ancho_carril, height)
marcador_borde_izquierdo = (95, 0, ancho_marcador, height)
marcador_borde_derecho = (395, 0, ancho_marcador, height)

# sirve para animar el movimiento de los marcadores de carril
mover_marcador_carril_y = 0

# coordenadas iniciales del jugador
jugador_x = 250
jugador_y = 400

# configuración de fotogramas
reloj = pygame.time.Clock()
fps = 120

# configuracion de juego
gameover = False
velocidad = 2
puntaje = 0

class Auto(pygame.sprite.Sprite):
    
    def __init__(self, imagen, x, y):
        pygame.sprite.Sprite.__init__(self)
        
    # escalar la imagen hacia abajo para que no sea más ancha que el carril
        imagen_escala = 45 / imagen.get_rect().width
        nuevo_ancho = imagen.get_rect().width * imagen_escala
        nuevo_alto = imagen.get_rect().height * imagen_escala
        self.image = pygame.transform.scale(imagen, (nuevo_ancho, nuevo_alto))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class JugadorAuto(Auto):
    
    def __init__(self, x, y):
        imagen = pygame.image.load('imagenes/auto.png')
        self.image = imagen
        super().__init__(imagen, x, y)
        
# grupos de sprites
grupo_jugadores = pygame.sprite.Group()
auto_grupo = pygame.sprite.Group()

# crea el auto del jugador
jugador = JugadorAuto(jugador_x, jugador_y)
grupo_jugadores.add(jugador)

# cargar las imágenes automaticamente
nombres_imagenes_autos = ['camioneta.png', 'camion.png', 'taxi.png', 'camioneta2.png']
auto_imagenes = []
for nombres_imagenes_autos in nombres_imagenes_autos:
    imagen = pygame.image.load('imagenes/' + nombres_imagenes_autos)
    auto_imagenes.append(imagen)
    
# carga las imágenes del vehículo
choque = pygame.image.load('imagenes/choque.png')
choque_rect = choque.get_rect()

# bucle de juego
correr = True
while correr:
    
    reloj.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            correr = False
            
    # mueve el auto del jugador usando las teclas de flecha izquierda/derecha
        if event.type == KEYDOWN:
            
            if event.key == K_LEFT and jugador.rect.center[0] > carril_izquierdo:
                jugador.rect.x -= 100
            elif event.key == K_RIGHT and jugador.rect.center[0] < carril_derecho:
                jugador.rect.x += 100
                
    # verifica si hay una colisión de deslizamiento después de cambiar de carril
            for auto in auto_grupo:
                if pygame.sprite.collide_rect(jugador, auto):
                    
                    gameover = True
                    
                    # coloca el auto del jugador al lado de otro vehículo
                     # y determina dónde colocar la imagen del accidente
                    if event.key == K_LEFT:
                        jugador.rect.left = auto.rect.right
                        choque_rect.center = [jugador.rect.left, (jugador.rect.center[1] + auto.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        jugador.rect.right = auto.rect.left
                        choque_rect.center = [jugador.rect.right, (jugador.rect.center[1] + auto.rect.center[1]) / 2]
            

    # dibuja el pasto
    pantalla.fill(verde)
    
    # dibuja el camino
    pygame.draw.rect(pantalla, gris, camino)
    
    # dibuja los bordes
    pygame.draw.rect(pantalla, amarillo, marcador_borde_izquierdo)
    pygame.draw.rect(pantalla, amarillo, marcador_borde_derecho)
    
    # dibuja las lineas del carril
    mover_marcador_carril_y += velocidad * 2
    if mover_marcador_carril_y >= alto_marcador * 2:
        mover_marcador_carril_y = 0
    for y in range(alto_marcador * -2, height, alto_marcador * 2):
        pygame.draw.rect(pantalla, blanco, (carril_izquierdo + 45, y + mover_marcador_carril_y, ancho_marcador, alto_marcador))
        pygame.draw.rect(pantalla, blanco, (carril_centro + 45, y + mover_marcador_carril_y, ancho_marcador, alto_marcador))
        
    # auto del jugador
    grupo_jugadores.draw(pantalla)

    # agrega un auto
    if len(auto_grupo) < 2:
        
        # espacio entre los autos
        agregar_auto = True
        for auto in auto_grupo:
            if auto.rect.top < auto.rect.height * 1.5:
                agregar_auto = False
                
        if agregar_auto:
            
            ## selecciona un carril aleatorio
            carril = random.choice(carriles)
            
            # seleccionea un vehículo al azar
            imagen = random.choice(auto_imagenes)
            auto = Auto(imagen, carril, -height / 2)
            auto_grupo.add(auto)
    
    # hace que los autos se muevan
    for auto in auto_grupo:
        auto.rect.y += velocidad
        
        # elimina el auto cuando sale de la pantalla
        if auto.rect.top >= height:
            auto.kill()
            
            # puntuacion
            puntaje += 1
            
            # acelerar el juego después de pasar 5 autos
            if puntaje > 0 and puntaje % 5 == 0:
                velocidad += 1
    
    # dibuja los autos
    auto_grupo.draw(pantalla)
    
    # muestra la puntuacion
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    texto = font.render('puntaje: ' + str(puntaje), True, blanco)
    texto_rect = texto.get_rect()
    texto_rect.center = (50, 400)
    pantalla.blit(texto, texto_rect)
    
    # comprola si hay una colisión de frente
    if pygame.sprite.spritecollide(jugador, auto_grupo, True):
        gameover = True
        choque_rect.center = [jugador.rect.center[0], jugador.rect.top]
            
    # juego terminado 
    if gameover:
        pantalla.blit(choque, choque_rect)
        
        pygame.draw.rect(pantalla, rojo, (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        texto = font.render('Game over. Jugar de nuevo? (Enter S or N)', True, blanco)
        texto_rect = texto.get_rect()
        texto_rect.center = (width / 2, 100)
        pantalla.blit(texto, texto_rect)
            
    pygame.display.update()

    # espera la entrada del usuario para empezar de nuevo o salir
    while gameover:
        
        reloj.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                correr = False
                
            # entrada del usuario (y ó n)
            if event.type == KEYDOWN:
                if event.key == K_s:
                    # reinicia el juego
                    gameover = False
                    velocidad = 2
                    puntaje = 0
                    auto_grupo.empty()
                    jugador.rect.center = [jugador_x, jugador_y]
                elif event.key == K_n:
                    # salir del bucle (juego)
                    gameover = False
                    correr = False

pygame.quit()

 