import socket
import select
import os
import sys
import random

def build_play(play):
    message = f"{NUMBER}:{' '.join(map(str, play))}"
    return message

def roll_dice():
    global IN_USE
    if not IN_USE:
        IN_USE = True
        user_input = input("¿Quieres lanzar los dados? (s/n): ")
        if user_input.lower() == "s":
            play = [random.randint(1, 6) for _ in range(4)]
            print("Tirada de dados:", play)
            message = build_play(play)
            SERVER.send(message.encode())
        IN_USE = False

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.connect(('localhost', 3005))

os.system('cls' if os.name == 'nt' else 'clear')
NAME = input("Ingresa tu nombre: ")
SERVER.send(f":{NAME}".encode())
NUMBER = "0"
GAME_OVER = False
IN_USE = False

while not GAME_OVER:
    sockets = [SERVER]
    read_sockets, _, _ = select.select(sockets, [], [])
    for sock in read_sockets:
        if sock == SERVER:
            message = sock.recv(1024).decode()
            os.system('cls' if os.name == 'nt' else 'clear')
            if message.count("#") > 0:
                print("Mi número es #" + message[-1])
                NUMBER = message[-1]
                GAME_OVER = True
                break
            print(message)

while GAME_OVER:
    roll_dice()
    sockets = [SERVER]
    read_sockets, _, _ = select.select(sockets, [], [])
    for sock in read_sockets:
        if sock == SERVER:
            message = sock.recv(1024).decode()
            print(message)
            if message.startswith("Ganan"):
                print(message)
                GAME_OVER = False
                break

SERVER.close()
