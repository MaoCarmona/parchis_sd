import socket
import sys
import os
import select
from _thread import start_new_thread
from game_classes import *

# Server connection from App
SERVER_CONNECTION = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_CONNECTION.connect(('localhost', 3005))

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# Main game loop
while not GAME:
    sockets = [SERVER_CONNECTION]
    try:
        leidos, escrito, error = select.select(sockets, [], [])
    except select.error as e:
        print("Error de select:", e)
        break
    
    for socks in leidos:
        if socks == SERVER_CONNECTION:
            mensaje = socks.recv(1024)
            os.system('cls' if os.name == 'nt' else 'clear')
            if mensaje.count(b"#") > 0:
                print("My number is #: " + mensaje[-1])
                NUMBER = mensaje[-1]
                GAME = True
                break
            print(mensaje)

if GAME:
    start_new_thread(throw, ())
    while not END:
        SCREEN.fill([255, 255, 255])
        sockets = [SERVER_CONNECTION]
        try:
            leidos, escrito, error = select.select(sockets, [], [])
        except select.error as e:
            print("Error de select:", e)
            break
        
        for socks in leidos:
            if socks == SERVER_CONNECTION:
                mensaje = socks.recv(1024)
                print(mensaje)
                mensaje = mensaje.split("#")
                aux = mensaje[3]
                mensaje[3] = mensaje[2]
                mensaje[2] = aux
                SCREEN.blit(DICE_FONT.render(str(mensaje[-1]), False, [0, 0, 0]), [700, 600])
                for n in range(4):
                    mensaje[n] = mensaje[n].split(" ")
                print(mensaje)
                print(len(fichos))
                for n in fichos:
                    print(len(n), "elemento")

                for i in range(4):
                    for j in range(4):
                        fichos[i][j].pos = int(mensaje[i][j])

                for i in range(4):
                    for j in range(4):
                        print(fichos[i][j].pos)
                print("Updated")
                if mensaje[0] == 'G':
                    GAME = False
                    END = True
                break

SERVER_CONNECTION.close()
