import socket
import select
import threading

def broadcast_data(sock, message, CONNECTION_LIST):
    print("Tamaño conn ", len(CONNECTION_LIST))
    for s in CONNECTION_LIST:
        if s != server_socket and s != sock:
            try:
                s.send(message.encode('utf-8'))
                print("Mensaje enviado")
            except Exception as e:
                print("Error al enviar el mensaje:", e)
                s.close()
                CONNECTION_LIST.remove(s)

def sendData(CONNECTION_LIST):
    try:
        with open("users.txt", 'r') as f:
            data = f.read()
            if len(data) == 0:
                return
            for s in CONNECTION_LIST:
                if s != server_socket:
                    try:
                        s.send(data.encode('utf-8'))
                    except Exception as e:
                        print("Error al enviar datos:", e)
                        s.close()
                        CONNECTION_LIST.remove(s)
            print("Datos enviados")
    except Exception as e:
        print("Error al abrir archivo:", e)

def getUsername(sock, dic):
    for u, s in dic.items():
        if s == sock:
            return u
    print("Usuario no encontrado")
    return None

def verifyUser(new_client, dic, CONNECTION_LIST, sock, COLOR_LIST, users_colors):
    while True:
        data = new_client.recv(1024).decode('utf-8').strip()
        print(f"Datos recibidos para verificación: {data}")
        user = data.split(":")
        print("Usuario: %s" % user)
        if len(user) < 2:
            new_client.send("Error en el formato de los datos\n".encode('utf-8'))
            continue
        if user[1] not in COLOR_LIST:
            new_client.send("Color ya ha sido utilizado\n".encode('utf-8'))
        elif user[0] in dic:
            new_client.send("Nombre de usuario ya ha sido utilizado\n".encode('utf-8'))
        else:
            COLOR_LIST.remove(user[1])
            CONNECTION_LIST.append(new_client)
            dic[user[0]] = new_client
            users_colors[user[0]] = user[1]
            new_client.send("Bienvenido\n".encode('utf-8'))
            break
    return ":".join(user)

def getSocket(username, dic):
    for u, s in dic.items():
        if u == username:
            return s
    print("Socket no encontrado")
    return None

def getIndex(username, dic, CONNECTION_LIST):
    s = getSocket(username, dic)
    return CONNECTION_LIST.index(s)

def save_user(data):
    try:
        with open("users.txt", 'a') as f:
            for user, color in data.items():
                f.write(user + ":" + color + "\n")
    except Exception as e:
        print("Error al escribir en archivo:", e)

def handle_client(conn, addr):
    global users_list
    global CONNECTION_LIST
    global server_socket

    print("Nueva conexión desde:", addr)
    try:
        username = verifyUser(conn, users_list, CONNECTION_LIST, server_socket, COLOR_LIST, users_colors)
        save_user(users_colors)

        sendData(CONNECTION_LIST)

        while True:
            data = conn.recv(RECV_BUFFER).decode('utf-8')
            if not data:
                break
            print("Datos recibidos por el servidor: " + data)
            user = getUsername(conn, users_list)
            print("Usuario que lo envió: " + user)

            if data == "Necesito el orden de los turnos" and len(users_list) == 4:
                sendData(CONNECTION_LIST)

            elif data.split(":")[0] == "Dados":
                broadcast_data(conn, data, CONNECTION_LIST)
                print("Se enviaron los dados: %s" % data)

            else:
                print("Se envía a todos los demás!!")
                broadcast_data(conn, data, CONNECTION_LIST)
    except Exception as e:
        print("Error en el hilo del cliente:", e)
    finally:
        conn.close()
        print("Cliente desconectado:", addr)
        CONNECTION_LIST.remove(conn)

if __name__ == "__main__":
    CONNECTION_LIST = []
    COLOR_LIST = ["red", "green", "yellow", "blue"]
    RECV_BUFFER = 4096
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", PORT))
    server_socket.listen(10)

    CONNECTION_LIST.append(server_socket)

    print("Servidor de chat iniciado en el puerto " + str(PORT))

    users_list = {}
    users_colors = {}

    with open("users.txt", 'w') as f:
        pass

    turnosEnviados = False

    while True:
        try:
            read_sockets, _, _ = select.select(CONNECTION_LIST, [], [])

            for sock in read_sockets:
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    if len(CONNECTION_LIST) > 4:
                        sockfd.send("Parques lleno, inténtalo más tarde".encode('utf-8'))
                        break
                    threading.Thread(target=handle_client, args=(sockfd, addr)).start()
                else:
                    print("Error: Socket no es el servidor")
        except KeyboardInterrupt:
            print("Servidor detenido")
            break

    server_socket.close()
