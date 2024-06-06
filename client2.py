import socket, select, string, sys

def prompt(username) :
    sys.stdout.write(username+": ")
    sys.stdout.flush()

#main function
if __name__ == "__main__":

    host = "localhost"
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to remote host
    try :
        s.connect((host, port))
        #username  = raw_input('Username: ')
        #s.sendall(username)
    except :
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host. Start sending messages') 

    while True:
        data = s.recv(4096).decode('utf-8')
        print(data)
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
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096).decode('utf-8')
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt(username)

            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                prompt(username)
