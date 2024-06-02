import pygame
import sys
from pygame.locals import *
from objects import Boton

def menu(cursor, PANTALLA):
    ALTO = 600
    ANCHO = 600

    PANTALLA = pygame.display.set_mode([ANCHO,ALTO])
    pygame.key.set_repeat(100,10)

    fondo = pygame.image.load("game_(1).png")
    jugar1 = pygame.image.load("botones/1.png")
    jugar2 = pygame.image.load("botones/1.1.png")
    salir1 = pygame.image.load("botones/2.png")
    salir2 = pygame.image.load("botones/2.2.png")
    boton1 = Boton(jugar1,jugar2,230,350)
    boton2 = Boton(salir1,salir2,230,450)
    pygame.mixer.music.load("musica/1.mp3")
    pygame.mixer.music.play(3)

    cerrar= False

    while not cerrar:
        tecla = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                val = True
                cerrar = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(boton1.rect):
                    val = False
                    cerrar = True
                if cursor.colliderect(boton2.rect):
                    val = True
                    cerrar = False

        cursor.posicion()
        PANTALLA.blit(fondo,(0,0))
        boton1.accion(PANTALLA,cursor)
        boton2.accion(PANTALLA,cursor)
        pygame.display.flip()
    pygame.mixer.music.stop()
    return val
