# telnet program example
import socket, select, string, sys
from objetos.objects import Boton, Cursor
import pygame
import sys
from pygame.locals import *

sys.path.append('./objetos/')

from objetos import *
 
def prompt(username) :
    sys.stdout.write(username+": ")
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":

    ANCHO=600
    ALTO=600
    ANCHO_PANTALLA=800

    pygame.init()
    PANTALLA = pygame.display.set_mode([ANCHO_PANTALLA,ALTO])

    jugar1 = pygame.image.load("objetos/botones/1.png")
    jugar2 = pygame.image.load("objetos/botones/1.1.png")
    boton1 = Boton(jugar1,jugar2,100,100)

    fondo = pygame.image.load("objetos/game.png")
    
    cursor= Cursor()

     
    host = "localhost"
    port = 5000
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # connect to remote host
    try :
        s.connect((host, port))
        #username  = raw_input('Username: ')
        #s.sendall(username)
    except :
        print ('Unable to connect')
        sys.exit()
     
    print ('Connected to remote host. Start sending messages')

    while True:
        data = s.recv(4096).decode('utf-8')
        print (data)
        if (data=="Parques lleno, intentalo mas tarde"):
            s.close()
            Correcto = False
            break
        if (data == "Bienvenido al chat"):
            Correcto = True
            break
        username = input()
        s.send(username)

    if Correcto:
        prompt(username)
     
    while Correcto:
        PANTALLA.blit(fondo,(0,0))
        #print ("while")
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096).decode('utf-8')
                if not data :
                    print ('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt(username)
             
            #user entered a message
            #else :
                #msg = sys.stdin.readline()
                #s.send(msg)
                #prompt(username)

            event = pygame.event.poll()
            #print ("evento")
            
            if event.type == QUIT:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(boton1.rect):
                    s.send("presiono %s" %username)
                    print ("presionooo", username)
                    
            cursor.posicion()
            PANTALLA.blit(fondo,(0,0))
            boton1.accion(PANTALLA,cursor)
            pygame.display.flip()