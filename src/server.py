import socket
import threading
import datetime

seguros = [1, 6, 13, 18, 23, 30, 35, 40, 47, 52, 57, 64]
CLIENTS = []
NAME_LIST = [None, None, None, None]
FINAL_SERVER = False

TURN = 1
USAGE = True
ATTEMPTS = 3

class Board():
    def __init__(self):
        # All pieces start in jail
        self.player1 = [0, 0, 0, 0]  # Green
        self.player2 = [0, 0, 0, 0]  # Blue
        self.player3 = [0, 0, 0, 0]  # Red
        self.player4 = [0, 0, 0, 0]  # Yellow

    # Method to move pieces
    def move(self, player, moves):
        who = self.who(player)
        if who.count(0) != 0 and self.trapped(moves):
            self.release(player)
            moves = ['0', '0', '0', '0']
        for n in range(4):
            if who[n] > 0:
                moves = self.sky(player, moves)
                if int(moves[n]) > 0:
                    who[n] += int(moves[n])
                    who[n] = (who[n] % 69)
                    print(who[n], "DANGER")
                self.capture(who, player)
                print("here")
                self.winner(player)
                print("exited")

    def winner(self, player):
        for n in range(4):
            if player == "1" and self.player1[n] > 75:
                self.player1[n] = -1
            if player == "2" and self.player2[n] > 82:
                self.player2[n] = -1
            if player == "3" and self.player3[n] > 89:
                self.player3[n] = -1
            if player == "4" and self.player4[n] > 96:
                self.player4[n] = -1

    def capture(self, player, number):
        for n in range(4):
            for m in range(4):
                if number != "1":
                    if player[n] == self.player1[m] and (player[n] not in seguros):
                        self.player1[m] = 0
                if number != "2":
                    if player[n] == self.player2[m] and (player[n] not in seguros):
                        self.player2[m] = 0
                if number != "3":
                    if player[n] == self.player3[m] and (player[n] not in seguros):
                        self.player3[m] = 0
                if number != "4":
                    if player[n] == self.player4[m] and (player[n] not in seguros):
                        self.player4[m] = 0

    def sky(self, player, moves):
        if player == "1":
            for n in range(4):
                print("what to do")
                if self.player1[n] < 69 and self.player1[n] + int(moves[n]) > 68:
                    moves[n] = str(int(moves[n]) - (69 - self.player1[n]))
                    self.player1[n] = 1
                print(self.player1[n], moves[n])
                if self.player1[n] == 1 and int(moves[n]) >= 1:
                    print("here")
                    self.player1[n] = 69
                    moves[n] = str(int(moves[n]) - 1)
                    self.player1[n] += moves[n]
                    moves[n] = 0
        if player == "2":
            for n in range(4):
                if self.player2[n] < 18 and self.player2[n] + int(moves[n]) > 17:
                    moves[n] = str(int(moves[n]) - (18 - self.player2[n]))
                    self.player2[n] = 18
                if self.player2[n] == 18 and int(moves[n]) >= 1:
                    self.player2[n] = 76
                    print(self.player2)
                    moves[n] = str(int(moves[n]) - 1)
                    self.player2[n] += moves[n]
                    moves[n] = 0
        if player == "3":
            for n in range(4):
                if self.player3[n] < 35 and self.player3[n] + int(moves[n]) > 34:
                    moves[n] = str(int(moves[n]) - (35 - self.player3[n]))
                    self.player3[n] = 35
                if self.player3[n] == 35 and int(moves[n]) >= 1:
                    self.player3[n] = 83
                    moves[n] = str(int(moves[n]) - 1)
                    self.player3[n] += moves[n]
                    moves[n] = 0
        if player == "4":
            for n in range(4):
                if self.player4[n] < 52 and self.player4[n] + int(moves[n]) > 51:
                    moves[n] = str(int(moves[n]) - (52 - self.player4[n]))
                    self.player4[n] = 52
                if self.player4[n] == 52 and int(moves[n]) >= 1:
                    self.player4[n] = 90
                    moves[n] = str(int(moves[n]) - 1)
                    self.player4[n] += moves[n]
                    moves[n] = 0
        return moves

    def release(self, player):
        if player == "1":
            for n, i in enumerate(self.player1):
                if i == 0:
                    self.player1[n] = 6
        if player == "2":
            for n, i in enumerate(self.player2):
                if i == 0:
                    self.player2[n] = 23
        if player == "3":
            for n, i in enumerate(self.player3):
                if i == 0:
                    self.player3[n] = 40
        if player == "4":
            for n, i in enumerate(self.player4):
                if i == 0:
                    self.player4[n] = 57

    def jail(self, player):
        for n in player:
            if n != -1 and n != 0:
                return False
        return True

    def who(self, player):
        if player == "1":
            return self.player1
        if player == "2":
            return self.player2
        if player == "3":
            return self.player3
        if player == "4":
            return self.player4

    def trapped(self, play):
        if play.count('1') == 2:
            return True
        if play.count('2') == 2:
            return True
        if play.count('3') == 2:
            return True
        if play.count('4') == 2:
            return True
        if play.count('5') == 2:
            return True
        if play.count('6') == 2:
            return True
        return False

def start_player(name, address):
    for n in range(len(NAME_LIST)):
        if NAME_LIST[n] is None:
            NAME_LIST[n] = [name, address]
            break

def incomplete():
    for n in NAME_LIST:
        if n is None:
            return True
    return False

def build_state():
    message = ""
    for n in NAME_LIST:
        if n is not None:
            message += n[0] + "\n"
    return message

def board_state():
    message = ""
    for n in GAME.player1:
        message += str(n) + " "
    message = message[:-1]
    message += "#"
    for n in GAME.player2:
        message += str(n) + " "
    message = message[:-1]
    message += "#"
    for n in GAME.player3:
        message += str(n) + " "
    message = message[:-1]
    message += "#"
    for n in GAME.player4:
        message += str(n) + " "
    message = message[:-1]
    now = datetime.datetime.now()
    message += "#" + str(now.hour) + ":" + str(now.minute)
    print(message)
    return message

def winner():
    if GAME.player3 == [-1, -1, -1, -1]:
        return "Red"
    if GAME.player4 == [-1, -1, -1, -1]:
        return "Yellow"
    if GAME.player1 == [-1, -1, -1, -1]:
        return "Green"
    if GAME.player2 == [-1, -1, -1, -1]:
        return "Blue"
    return "Nobody"

def client_thread(conn, addr):
    conn.send(b"Welcome to Parchis Game for SD <3\n")
    # Either all players are in or we don't start
    message = conn.recv(1024)
    if message[0] == ord(":"):
        start_player(message.decode(), addr[0])
        sending = message + b" has joined\n" + build_state().encode()
        broadcast(sending)
        if not incomplete():
            assign()
    else:
        remove(conn)

    while incomplete():
        continue

    print("room full\n")

    global TURN
    global USAGE
    global ATTEMPTS

    while True:
        if winner() != "Nobody":
            broadcast(b"Ganan las fichas " + winner().encode())
            break
        try:
            message = conn.recv(1024)
            print(message, TURN, USAGE)
            if message[0] == ord("1") and TURN == 1 and USAGE:
                USAGE = False
                move = message.split(b":")[1].split(b" ")
                if not GAME.jail(GAME.player1):
                    ATTEMPTS = 0
                ATTEMPTS -= 1
                if not GAME.trapped(move) and ATTEMPTS <= 0:
                    TURN = 2
                    ATTEMPTS = 3
                GAME.move(message[0], move)
                USAGE = True
                print(board_state())
                broadcast(board_state())
                print("sent")
            if message[0] == ord("2") and TURN == 2 and USAGE:
                USAGE = False
                move = message.split(b":")[1].split(b" ")
                if not GAME.jail(GAME.player2):
                    ATTEMPTS = 0
                ATTEMPTS -= 1
                if not GAME.trapped(move) and ATTEMPTS <= 0:
                    TURN = 3
                    ATTEMPTS = 3
                GAME.move(message[0], move)
                USAGE = True
                broadcast(board_state())
            if message[0] == ord("3") and TURN == 3 and USAGE:
                USAGE = False
                move = message.split(b":")[1].split(b" ")
                if not GAME.jail(GAME.player3):
                    ATTEMPTS = 0
                ATTEMPTS -= 1
                if not GAME.trapped(move) and ATTEMPTS <= 0:
                    TURN = 4
                    ATTEMPTS = 3
                GAME.move(message[0], move)
                USAGE = True
                broadcast(board_state())
            if message[0] == ord("4") and TURN == 4 and USAGE:
                USAGE = False
                move = message.split(b":")[1].split(b" ")
                if not GAME.jail(GAME.player4):
                    ATTEMPTS = 0
                ATTEMPTS -= 1
                if not GAME.trapped(move) and ATTEMPTS <= 0:
                    TURN = 1
                    ATTEMPTS = 3
                GAME.move(message[0], move)
                USAGE = True
                broadcast(board_state())
        except:
            continue

def assign():
    message = 1
    for client in CLIENTS:
        try:
            client.send(b"#" + str(message).encode())
            message += 1
        except:
            client.close()
            remove(client)

def broadcast(message):
    for client in CLIENTS:
        try:
            client.send(message)
        except:
            client.close()
            remove(client)

def remove(connection):
    if connection in CLIENTS:
        CLIENTS.remove(connection)

GAME = Board()
def start_server():
    try:
        # Creamos el socket del servidor
        SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Asociamos y escuchamos en una dirección y un puerto específico
        SERVER.bind(('localhost', 3005))
        SERVER.listen(5)
        print("Servidor iniciado. Esperando conexiones...")

        # Bucle principal del servidor
        while not FINAL_SERVER:
            # Aceptamos conexiones de clientes
            conn, addr = SERVER.accept()
            CLIENTS.append(conn)
            print(addr[0] + " se ha conectado")

            # Iniciamos un nuevo hilo para manejar la solicitud del cliente
            client_th = threading.Thread(target=client_thread, args=(conn, addr))
            client_th.start()

        # Cerramos la conexión del servidor
        SERVER.close()

    except Exception as e:
        print("Ha ocurrido un error:", e)

start_server()
