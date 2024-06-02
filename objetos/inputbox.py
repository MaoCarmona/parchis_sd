import pygame
from pygame.locals import *
from objects import *
# Cargar imágenes y redimensionarlas
rojo1 = pygame.image.load("rojo.png")
rojo1 = pygame.transform.scale(rojo1, (50, 50))
rojo2 = pygame.image.load("ficha_roja_2.png")
rojo2 = pygame.transform.scale(rojo2, (50, 50))
verde1 = pygame.image.load("verde.png")
verde1 = pygame.transform.scale(verde1, (50, 50))
verde2 = pygame.image.load("ficha_verde_2.png")
verde2 = pygame.transform.scale(verde2, (50, 50))
azul1 = pygame.image.load("azul.png")
azul1 = pygame.transform.scale(azul1, (50, 50))
azul2 = pygame.image.load("ficha_azul_2.png")
azul2 = pygame.transform.scale(azul2, (50, 50))
amarillo1 = pygame.image.load("amarilla.png")
amarillo1 = pygame.transform.scale(amarillo1, (50, 50))
amarillo2 = pygame.image.load("ficha_amarillo_2.png")
amarillo2 = pygame.transform.scale(amarillo2, (50, 50))

# Crear botones
boton_rojo = Boton(rojo1, rojo2, 100, 100)
boton_verde = Boton(verde1, verde2, 160, 100)
boton_azul = Boton(azul1, azul2, 220, 100)
boton_amarillo = Boton(amarillo1, amarillo2, 280, 100)
def get_key(cursor, screen, current_color):
    color = current_color
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit', color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(boton_rojo.rect):
                    color = "red"
                elif cursor.colliderect(boton_verde.rect):
                    color = "green"
                elif cursor.colliderect(boton_azul.rect):
                    color = "blue"
                elif cursor.colliderect(boton_amarillo.rect):
                    color = "yellow"
            if event.type == KEYDOWN:
                return event.key, color

        cursor.posicion()
        boton_rojo.accion(screen, cursor)
        boton_verde.accion(screen, cursor)
        boton_azul.accion(screen, cursor)
        boton_amarillo.accion(screen, cursor)
        pygame.display.flip()

def display_box(screen, message, cursor, x, y):
    fontobject = pygame.font.Font(None, 25)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 500, 240), 0)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)), (x, y))
    pygame.display.flip()

def ask(screen, question, cursor, usr_err, color_err):
    current_color = None
    message_color = ""
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + ''.join(current_string), cursor, 100, 20)
    display_box(screen, usr_err, cursor, 120, 200)
    display_box(screen, color_err, cursor, 120, 250)

    while True:
        inkey, current_color = get_key(cursor, screen, current_color)
        
        if inkey == K_BACKSPACE:
            current_string = current_string[:-1]
        elif inkey == K_RETURN:
            if current_color is None:
                message_color = "Seleccione color"
                print("Seleccione color")
            else:
                break
        elif inkey == K_MINUS:
            current_string.append("-")
        elif isinstance(inkey, int) and inkey <= 127:
            if len(current_string) <= 10:
                current_string.append(chr(inkey))

        display_box(screen, question + ": " + ''.join(current_string), cursor, 100, 20)
        display_box(screen, message_color, cursor, 150, 170)
        display_box(screen, usr_err, cursor, 120, 200)
        display_box(screen, color_err, cursor, 120, 250)

    return ''.join(current_string) + ":" + current_color

def main_inputBox(cursor, screen, usr_err, color_err):
    screen = pygame.display.set_mode((500, 280))
    return ask(screen, "Nombre de usuario", cursor, usr_err, color_err)
