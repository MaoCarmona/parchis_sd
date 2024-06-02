import pygame
import sys
import time
import random
from pygame.locals import *
from menu import menu
from inputbox import main_inputBox, display_box
from objects import *
import socket, select, string, sys

ANCHO=600
ALTO=600
ANCHO_PANTALLA=800
pygame.init()
PANTALLA = pygame.display.set_mode([ANCHO_PANTALLA,ALTO])

##################################################################################


class Imagen(pygame.sprite.Sprite):
	def __init__(self,imagen,x,y,ancho,alto):
		self.ancho=ancho
		self.alto=alto
		self.imagen= imagen
		self.imagen= pygame.transform.scale(self.imagen, (self.ancho,self.alto))
		self.rect=self.imagen.get_rect()
		self.rect.left,self.rect.top=x,y

	def dibujar(self,pantalla):
		pantalla.blit(self.imagen,self.rect)
		pygame.display.update()



class Dados(pygame.sprite.Sprite):
	def __init__(self,imagen,x,y,ancho,alto):
		self.ancho=ancho
		self.alto=alto
		self.valor=0;
		self.imagen= imagen
		self.imagen= pygame.transform.scale(self.imagen, (self.ancho,self.alto))
		self.rect=self.imagen.get_rect()
		self.rect.left,self.rect.top=x,y

	def dibujar(self,pantalla):
		pantalla.blit(self.imagen,self.rect)
		pygame.display.update()

	def animacion(self,pantalla, num, aleatorio):
		if (aleatorio):
			cont = random.randrange(1, 7)
		else:
			cont = num
		self.valor=cont
		self.imagen=pygame.image.load(str(cont)+".JPG")
		self.imagen= pygame.transform.scale(self.imagen, (self.ancho,self.alto))
		pantalla.blit(self.imagen,self.rect)
		pygame.display.update()
		return(cont)
##################################################################################

class Tile(object):

	def __init__(self):
		self.ocupantes=[] #Numero de personas que estan ocupando el tile
		self.seguro=False
		self.numerocasilla="null"
		self.salida=False
		self.color="null"
		self.acomodo=0
		self.acomodoy=0
		self.cuadrante="null"
	def anexarocupante(self,ob):
		self.ocupantes.append(ob)

	def comer(self,colordominante):
		if (self.seguro == False):
			for x in self.ocupantes:
				if(x.color!=colordominante):
					x.pos="carcel"

	def comerobligado(self,colordominante):
		for x in self.ocupantes:
			if(x.color!=colordominante):
				x.pos="carcel"


	def sacar(self,colordominante):
			contador=0
			for x in self.ocupantes:
				if(x.color==colordominante):
					return (self.ocupantes.pop(contador))
				contador+=1

	def validarocupantes(self):
		pass

def click(mx,my):
	#Cordenadas de priciones
	mx1=mx
	my1=my
	mx=int(mx/200)
	my=int(my/200)

	if(mx==0 and my==0):
		return  "green"

	if(mx==2 and my==0):
		return  "red"

	if(mx==0 and my==2):
		return  "yellow"


	if(mx==2 and my==2):
		return  "blue"
	#Cordenadas de secciones

	if(mx==1 and my==0):
		# print("seccion verde y roja")

		mx1=int(mx1/66)
		auxx=mx1-3
		mx1=55-mx1
		my1=int(my1/28)

		if(auxx==2):
			return(mx1-my1)
		if(auxx==0):
			return(mx1+my1)
		if(auxx==1):
			if(mx1==51 and my1==0):
				return 51
			else:
				return(mx1+my1+35)

	if(mx==0 and my==1):
		# print("seccion amarilla y verde")

		mx1=int(mx1/28)
		my1=int(my1/66)
		auxy=my1-3

		if(auxy==0):
			my1=my1+64
			return(my1-mx1)

		if(auxy==1):

			my1=my1+64
			if(my1+mx1>74):
				return 74
			else:
				return(my1+mx1)

		if(auxy==2):
			my1=my1
			return(mx1+1)


	if(mx==1 and my==2):
		# print("seccion amarilla y azul")
		mx1=int(mx1/66)
		auxx=mx1-3
		mx1=-mx1
		my1=int(my1/27.5)

		if(auxx==0):
			return(mx1+my1-2)

		if(auxx==2):
			return(mx1-my1+44)

		if(auxx==1):
				if(mx1==-4 and my1==21):
					return 17
				else:
					if(mx1-my1+43+56==81):
						return 80
					else:
						return(mx1-my1+43+56)


	if(mx==2 and my==1):
		# print("seccion azul y rojo")
		mx1=int(mx1/29)
		my1=int(my1/66)
		auxy=my1-3

		if(auxy==0):
			my1=my1+52
			if(my1-mx1==34):
				return 35
			return(my1-mx1)

		if(auxy==1):
			my1=my1+96

			if((mx1==20 or mx1==21) and my1==100):
				return 34
			else:
				return(my1-mx1)

		if(auxy==2):
			my1=my1+8
			if(my1+mx1==34):
				return 33
			return(my1+mx1)

	if(mx==1 and my==1):
		# print("cuadro medio")
		mx1=int(mx1/66)
		my1=int(my1/28)
		# print(mx1,my1)
		if(mx1==3 and my1==7):
			return 59

		if(mx1==5 and my1==7):
			return 43

		if((mx1==3 and my1==8) or  (mx1==3 and my1==9)):
			return 60

		if((mx1==3 and my1==12)):
			return 8

		if((mx1==5 and my1==8) or  (mx1==5 and my1==9)):
			return 42

		if(mx1==5 and my1==12):
			return 26


		if((mx1==3 and my1==14) or  (mx1==3 and my1==13)):
			return 9

		if(mx1==5 and my1==13 or (mx1==5 and my1==12)):
			return 25



	#Carceles__________________________________________________


def clickdado(mx,my):
	print ("clickdado")
	#Cordenadas de priciones
	mx1=mx
	my1=my
	mx=int(mx/200)
	my=int(my/200)

	if(mx==1 and my==1):
		print ("entra a clickdado")
		return "dado"



	#Carceles__________________________________________________

#____________________________PARA MODULAR CADA CLASE EN UNA ARCHIVO__________________________
def vector_posiciones(dato):
	vector_posiciones=[]
	for i in range (0,96):
		vector_posiciones.append(0)
	# seccion 1
	pos_x= 0
	pos_y= 200
	for i in range(0,3):
		for j in range(0,8):
			vector_posiciones[(click(pos_x,pos_y)-1)]= [pos_x,pos_y]
			pos_x=pos_x+28
		pos_x=0
		pos_y=pos_y+66

	# seccion 4
	pos_x= 200
	pos_y= 0
	for i in range(0,3):
		for j in range(0,8):
			vector_posiciones[(click(pos_x,pos_y)-1)]= [pos_x,pos_y]
			pos_y=pos_y+28
		pos_y=0
		pos_x=pos_x+66

	# seccion 2
	pos_x= 200
	pos_y= 400 ######################## REVISAR LA FUNCION CLICK(MX,MY) pos_y deberia se 400-28
	for i in range(0,3):
		for j in range(0,8):
			vector_posiciones[(click(pos_x,pos_y)-1)]= [pos_x,pos_y]
			pos_y=pos_y+28
		pos_y=400
		pos_x=pos_x+66

	# seccion 3
	pos_x= 400
	pos_y= 200


	for i in range(0,3):
		for j in range(0,8):
			vector_posiciones[(click(pos_x,pos_y)-1)]= [pos_x,pos_y]
			pos_x=pos_x+28
		pos_x=400
		pos_y=pos_y+66

	# print(vector_posiciones)

	#vector_posiciones[42-1]= [332-28,196]
	#vector_posiciones[26-1]= [400,332-28]
	#contador=1
	#print("____________________________")
	#for leo in vector_posiciones:
	#	print(str(contador)+"="+str(leo))
	#	contador+=1

	return(vector_posiciones[dato-1])

def cargartiles(cantidad,lista):
	contador=1
	for x in range(1,cantidad):
		til=Tile()
		til.numerocasilla=x
		if(contador>=1 and contador<=8):
			til.cuadrante=4

		if(contador>=60 and contador<=68):
			til.cuadrante=4

		if(contador>=43 and contador<=59):
			til.cuadrante=1


		if(contador>=26 and contador<=42):
			til.cuadrante=2

		if(contador>=9 and contador<=25):
			til.cuadrante=3

		contador+=1
		lista.append(til)

class tablero(object):

	def __init__(self):
		self.Tiles=[]
		cargartiles(96,self.Tiles)


	def reiniciarespacios(self):
		for x in self.Tiles:
			x.acomodo=0
			x.acomodoy=0

	def dibujarmapa(self):
		fondo=pygame.image.load("fondo.jpg")
		fondo=pygame.transform.scale(fondo,(600,600))
		PANTALLA.blit(fondo,(0,0))
		pygame.display.update()
		pygame.display.flip()

	def ponerjugadores(self,judadore):
		rojo=pygame.image.load("rojo.png")
		azul=pygame.image.load("azul.png")
		verde=pygame.image.load("verde.png")
		amarillo=pygame.image.load("amarilla.png")

		rojo=pygame.transform.scale(rojo,(20,20))
		azul=pygame.transform.scale(azul,(20,20))
		verde=pygame.transform.scale(verde,(20,20))
		amarillo=pygame.transform.scale(amarillo,(20,20))

		for x in judadore:
			contador=1
			contadory=1
			self.reiniciarespacios()
			for y in x.lista_fichas:
				if(y.pos=="carcel"):
					if(x.color=="green"):
						PANTALLA.blit(verde,(60*contador,60*contadory))
						pygame.display.update()

					if(x.color=="red"):
						PANTALLA.blit(rojo,(400+contador*60,60*contadory))
						pygame.display.update()

					if(x.color=="blue"):
						PANTALLA.blit(azul,(400+contador*60,400+60*contadory))
						pygame.display.update()

					if(x.color=="yellow"):
						PANTALLA.blit(amarillo,(contador*60,400+60*contadory))
						pygame.display.update()

					if(contador==2 and contadory != 2):
						contadory=2
						contador=0
					pygame.display.flip()
					contador+=1
					pygame.display.update()
				else:
					#DESDE ACA________________________________________

					cuadrex=0
					cuadrey=0
					#ACOMODAR POR CUADRANTES
					if(self.Tiles[y.pos].cuadrante==1):
						cuadrex=self.Tiles[y.pos].acomodo=self.Tiles[y.pos].acomodo+20
						cuadrey=10

					if(self.Tiles[y.pos].cuadrante==2):
						cuadrex=-20
						cuadrey=self.Tiles[y.pos].acomodoy=self.Tiles[y.pos].acomodoy-20
						cuadrey=cuadrey+60

					if(self.Tiles[y.pos].cuadrante==3):

						cuadrex=self.Tiles[y.pos].acomodo=self.Tiles[y.pos].acomodo+20
						cuadrey=-20

					if(self.Tiles[y.pos].cuadrante==4):
						cuadrex=0
						cuadrey=self.Tiles[y.pos].acomodoy=self.Tiles[y.pos].acomodoy+20

					if(y.pos==59):
						cuadrex=self.Tiles[y.pos].acomodo=self.Tiles[y.pos].acomodo+20
						cuadrey=0

					if(y.pos==25):
						cuadrex=self.Tiles[y.pos].acomodo=self.Tiles[y.pos].acomodo+20
						cuadrey=-20

					if(y.pos==8):
						cuadrex=0
						cuadrey=self.Tiles[y.pos].acomodoy=self.Tiles[y.pos].acomodoy+20

					if(y.pos==42):
						cuadrex=-20
						cuadrey=self.Tiles[y.pos].acomodoy=self.Tiles[y.pos].acomodoy+20

					if(x.color=="green"):

						PANTALLA.blit(verde,(vector_posiciones(y.pos)[0]+cuadrex,vector_posiciones(y.pos)[1]+cuadrey))
						pygame.display.update()

					if(x.color=="red"):


						PANTALLA.blit(rojo,(vector_posiciones(y.pos)[0]+cuadrex,vector_posiciones(y.pos)[1]+cuadrey))
						pygame.display.update()

					if(x.color=="blue"):

						PANTALLA.blit(azul,(vector_posiciones(y.pos)[0]+cuadrex,vector_posiciones(y.pos)[1]+cuadrey))
						pygame.display.update()

					if(x.color=="yellow"):
						PANTALLA.blit(amarillo,(vector_posiciones(y.pos)[0]+cuadrex,vector_posiciones(y.pos)[1]+cuadrey))
						pygame.display.update()

					pygame.display.flip()
					#HASTA ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
	def reload(self,lista_jugadores):
		self.dibujarmapa()
		self.ponerjugadores(lista_jugadores)

	def validarfindejuego(self):
		pass

	def pulir(self):
		self.Tiles[5].seguro=True
		self.Tiles[5].salida=True
		self.Tiles[5].color="yellow"
		self.Tiles[12].seguro=True

		self.Tiles[22].seguro=True
		self.Tiles[22].salida=True
		self.Tiles[22].color="blue"
		self.Tiles[29].seguro=True

		self.Tiles[39].seguro=True
		self.Tiles[39].salida=True
		self.Tiles[39].color="red"
		self.Tiles[46].seguro=True

		self.Tiles[56].seguro=True
		self.Tiles[56].salida=True
		self.Tiles[56].color="green"
		self.Tiles[63].seguro=True
#______________________________________________________________________
class Jugador(object):

	def __init__(self,nombre,color):
		self.lista_fichas=[]
		self.color=color
		self.nombre=nombre
		self.carcel=True
		self.turno=False

	def anexarficha(self,ficha):
		self.lista_fichas.append(ficha)

	def iniciarturno(self):
		self.turno=True

	def terminarturno(self):
		self.turno=False

	def cantidadfichas(self):
		return len(self.lista_fichas)

	def elimininarficha(self,pos):
		iterador=0
		for x in self.lista_fichas:
			if(x.pos==pos):
				self.lista_fichas.pop(iterador)
			iterador+=1

	def carcelon(self):
		for x in self.lista_fichas:
			if(x.pos!="carcel"):
				return False
		return True


	def salircarcel(self):
		pass
#______________________________________________________________________
class ficha(object):
	def __init__(self,color):
		self.pos="carcel"
		self.seleccionada=False
		self.color=color
		self.vuelta=False

class  logicadejuego(object):
	def __init__(self,lista):
		self.puedejugar="Null"
		self.turno=True
		self.listapersonajes=lista

	def quienjuega(self,listapersonajes):
		for x in listapersonajes:
			if(x.turno==True):
				self.puedejugar=x

	def algunafichaencarcel(self,jugador):
			for y in jugador.lista_fichas:
				if(y.pos=="carcel"):
					return True
			return False

	def pasarturnoo(self):
		for x in self.listapersonajes:
			if(x.turno == True):
				x.turno = False
				idx = self.listapersonajes.index(x)
				idx += 1
				if (idx > 3):
					idx = 0
				self.listapersonajes[idx].turno = True
				self.turno = True
				return

	def pasarturnoorepetir(self):
		self.turno=True


	def estalaficha(self,lista,color):
		for x in lista:
			if(x.color==color):
				return True
		return False

	def validarpos(self,mapa,pos):
		if(pos!= "green" and pos!= "yellow" and pos!= "blue" and pos!= "red" and pos != None ):
			if(len(mapa.Tiles[pos].ocupantes)>0):
				if(self.estalaficha(mapa.Tiles[pos].ocupantes,self.puedejugar.color)):
					return True
			else:
				return False
		else:
			return False

	def buclemovimiento(self):
		pass

	def enmovimientodeficha(self,dadosjuego,pos,mapa,lista_jugadores):
		if(dadosjuego.dado1l==True or dadosjuego.dado2l==True):
			if(dadosjuego.dado1l==True):
				dadillos=dadosjuego.dado1
				dadosjuego.dado1l=False
			else:
				if(dadosjuego.dado2l==True):
					dadillos=dadosjuego.dado2
					dadosjuego.dado2l=False


			aux=mapa.Tiles[pos].sacar(self.puedejugar.color)
			#POR ACA PUEDO HACER LA DE COMER :DDDD
			for x in lista_jugadores:
				contadore=0

				for y in x.lista_fichas:
					if(y==aux):
						if(type(y.pos)==int):
							if(y.color=="green" or y.color=="blue" or y.color=="red" ):
								if(y.pos+dadillos>68 and  y.pos+dadillos<76):
									mapa.Tiles[pos+dadillos].comer(y.color)
									mapa.Tiles[y.pos+dadillos-68].anexarocupante(y)
									y.pos=y.pos+dadillos-68
								else:
									if(y.color=="blue" and y.pos+dadillos>17 and pos<=17 and y.vuelta==False):
										y.vuelta=True
										diferencia=(y.pos+dadillos)-y.pos
										y.pos=73+diferencia
										mapa.Tiles[y.pos].anexarocupante(y)

									else:

										if(y.color=="red" and y.pos+dadillos>34 and pos<=34 and y.vuelta==False):
											y.vuelta=True
											diferencia=(y.pos+dadillos)-y.pos
											y.pos=77+diferencia
											mapa.Tiles[y.pos].anexarocupante(y)
										else:
											if(y.color=="green" and y.pos+dadillos>51 and pos<=51 and y.vuelta==False):
												y.vuelta=True
												diferencia=(y.pos+dadillos)-y.pos
												y.pos=83+diferencia
												mapa.Tiles[y.pos].anexarocupante(y)

											else:

												mapa.Tiles[pos+dadillos].comer(y.color)
												y.pos=y.pos+dadillos
												mapa.Tiles[pos+dadillos].anexarocupante(y)
												print(len(mapa.Tiles[pos+dadillos].ocupantes))
							else:
								mapa.Tiles[pos+dadillos].comer(y.color)
								y.pos=y.pos+dadillos
								mapa.Tiles[pos+dadillos].anexarocupante(y)

							if(y.color=="yellow" and y.pos>74):
								x.lista_fichas.pop(contadore)

							if(y.color=="blue" and y.pos>80):
								x.lista_fichas.pop(contadore)

							if(y.color=="red" and y.pos>86):
								x.lista_fichas.pop(contadore)

							if(y.color=="green" and y.pos>92):
								x.lista_fichas.pop(contadore)

				contadore+=1

			mapa.reload(lista_jugadores)
			if(dadosjuego.dado1l==False and dadosjuego.dado2l==False):
				self.turno=False

	def jugar(self,listapersonajes,pos,dadosjuego,mapa):
		self.quienjuega(listapersonajes)

		print("el turno del jugador "+self.puedejugar.color)
		print(pos)
		if(self.puedejugar.color==pos):
			if(dadosjuego.dado1==dadosjuego.dado2 and  self.algunafichaencarcel(self.puedejugar)):
				for x in listapersonajes:
					for y in x.lista_fichas:
						if(y.pos=="carcel"):
							#######COMER AL SALIR DE LA CARCEL
							if(self.puedejugar.color=="red" and x.color=="red"):
								y.pos=39
								mapa.Tiles[39].comerobligado("red")
								mapa.Tiles[39].anexarocupante(y)

							if(self.puedejugar.color=="blue" and x.color=="blue"):
								y.pos=22
								mapa.Tiles[22].comerobligado("blue")
								mapa.Tiles[22].anexarocupante(y)

							if(self.puedejugar.color=="green" and x.color=="green"):
								y.pos=56
								mapa.Tiles[56].comerobligado("green")
								mapa.Tiles[56].anexarocupante(y)

							if(self.puedejugar.color=="yellow"  and x.color=="yellow"):
								y.pos=5
								mapa.Tiles[5].comerobligado("yellow")
								mapa.Tiles[5].anexarocupante(y)
				self.turno=False
				return

		if(self.validarpos(mapa,pos)):
			print("juegando")
			self.enmovimientodeficha(dadosjuego,pos,mapa,listapersonajes)

	def pasarturno(self):
		if(self.turno==True):
			return False
		else:
			return True
#______________________________________________________________________
class  dados(object):

	def __init__(self):
		self.dado1=3
		self.dado2=3
		self.dado1l=True
		self.dado2l=True

	def haypar(self):
		pass

	def tirar(self):
		pass

	def reiniciar(self,dado_1,dado_2):
		print("____________________________________________________")
		print(dado_1)
		print("____________________________________________________")
		self.dado1=dado_1
		self.dado2=dado_2
		self.dado1l=True
		self.dado2l=True

def cargarfichas(cantidad, obj):
    for _ in range(cantidad):
        fich = ficha(obj.color)
        obj.anexarficha(fich)
    return obj

def cargarfichasjugadores(cantidad, lista):
    for jugador in lista:
        cargarfichas(cantidad, jugador)
#______________________________________________________________________

def validaganador(lista):
	return False

def agregarJugador(lista_jugadores, nuevoJugador):
	print ("Jugador entrante: ", nuevoJugador)
	jugador = Jugador(nuevoJugador[0],nuevoJugador[1])
	lista_jugadores.append(jugador)
	jugador.turno == False
	return jugador

def esperarJugadores(lista_jugadores, socket):
	data = socket.recv(4096).decode('utf-8')
	data = data.split("\n")

	for element in data:
		data_element = element.split(":")
		if (len(data_element) < 2):
			continue

		colors_not_available = []

		for player in lista_jugadores:
			colors_not_available.append(player.color)

		if (data_element[1] not in colors_not_available):
			agregarJugador(lista_jugadores, data_element)

def mostrarJugadores(lista_jugadores, PANTALLA, cursor):
	xj = 630; yj = 130
	display_box(PANTALLA, 'Jugadores', cursor, xj, yj)
	for jug in lista_jugadores:
		yj += 40
		display_box(PANTALLA, "%s -> %s" %(jug.color, jug.nombre), cursor, xj, yj)

def organizarTurnos(lista_jugadores,socket):
	turnos = []
	orden = []
	print("RECIBIENDO TURNOS")

	data = socket.recv(4096).decode('utf-8')
	data = data.split("\n")
	print("Turno %s" %(data) )

	for element in data:
		data_element = element.split(":") # usuario:color
		if (not(data_element[0] in turnos) and data_element[0] != ''):
			print("Turno guardado %s" %(data_element[0]))
			turnos.append(data_element[0])

	print("Lista turnos: %s" %(turnos))

	for i in range(4):
		for j in lista_jugadores:
			if j.nombre == turnos[i]:
				orden.append(j)
				break
	return orden

def mostrarTurno(lista_jugadores, PANTALLA, cursor):
	turno = ""
	for j in lista_jugadores:
		if (j.turno):
			turno = j.nombre
			break
	display_box(PANTALLA, "Turno: %s" %turno, cursor, 666, (40*5)+130)


def main():
    #----------------------- Conexión con el servidor -------------------------
    host = "localhost"
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))
    except Exception as e:
        print('No se puede conectar:', e)
        sys.exit()

    print("Conectado por el puerto", port)

    #-------------------------------------------------------------------------

    cursor = Cursor()

    PANTALLA = pygame.display.set_mode([ANCHO_PANTALLA, ALTO])
    cerrar = menu(cursor, PANTALLA)

    error_usuario = ""
    error_color = ""
    lista_jugadores = []  # Lista donde van a ir todos los jugadores

    while not cerrar:
        data_user = main_inputBox(cursor, PANTALLA, error_usuario, error_color)
        s.send(data_user.encode('utf-8'))
        data = s.recv(4096).decode('utf-8')
        print(data)
        if data == "Parques lleno, intentalo mas tarde":
            s.close()
            sys.exit()
        elif data == "Bienvenido":
            data_user = data_user.split(":")
            miJugador = agregarJugador(lista_jugadores, data_user)
            cerrar = True
        elif data == "Nombre de usuario ya ha sido utilizado\n":
            error_usuario = "Nombre de usuario ya ha sido utilizado"
        else:
            error_usuario = ""
        if data == "Color ya ha sido utilizado\n":
            error_color = "Color ya ha sido utilizado"
        else:
            error_color = ""

    PANTALLA = pygame.display.set_mode([800, 600])
    cantidad = 4  # Cantidad de fichas
    table = tablero()  # Tablero
    table.pulir()
    table.dibujarmapa()

    dado_1 = Dados(pygame.image.load("1.JPG"), (600/3)+(int(600/3)*0.25), int(((600/3)+((600/3)*0.4))), int((600/3)*0.2), int((600/3)*0.2))
    dado_2 = Dados(pygame.image.load("2.JPG"), (600/3)+(int(600/3)*0.5), int((600/3)+((600/3)*0.4)), int((600/3)*0.2), int((600/3)*0.2))

    playdados = True
    carce = False
    contador = 0
    cerrar = True
    iniciarJuego = False
    flag = True
    jugando = False
    turnos = []

    while cerrar:
        if len(lista_jugadores) == 4 and flag:
            s.send("Necesito el orden de los turnos".encode('utf-8'))
            order = organizarTurnos(lista_jugadores, s)
            lista_jugadores = order
            for j in lista_jugadores:
                print("%s: %s" % (j.nombre, j.color))

            lista_jugadores[0].turno = True
            flag = False
            iniciarJuego = True

        if iniciarJuego:
            print("Entro a iniciarjuego")
            cargarfichasjugadores(cantidad, lista_jugadores)
            table.ponerjugadores(lista_jugadores)
            logijuego = logicadejuego(lista_jugadores)
            dadosjuego = dados()
            for i in lista_jugadores:
                print("Jugador: %s, fichas: %s" % (i.nombre, str(len(i.lista_fichas))))
            iniciarJuego = False
            jugando = True

        for event in pygame.event.get():
            if event.type == QUIT:
                cerrar = False

            if jugando:
                mxmy = ""  # Contiene la posición en la que otro cliente hizo click
                mx = ""
                my = ""

                if miJugador.turno:
                    print("Es mi turno")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print("Click!")
                        mx, my = pygame.mouse.get_pos()
                        print("mx: ", mx)
                        print("my: ", my)
                        s.send(f"{mx},{my}".encode('utf-8'))

                else:
                    print("No es mi turno")
                    mxmy = s.recv(4096).decode('utf-8')
                    mxmy = mxmy.split(",")
                    print("Posición del cursor del que está jugando: ", mxmy)
                    if len(mxmy) == 2 and mxmy[0].isdigit() and mxmy[1].isdigit():
                        mx, my = int(mxmy[0]), int(mxmy[1])

                if logijuego.puedejugar == "Null":
                    print("No se han tirado los datos por primera vez")
                else:
                    if logijuego.puedejugar.carcelon() and clickdado(mx, my) == "dado":
                        contador += 1
                        for _ in range(1, 10):
                            dado_1.animacion(PANTALLA, 0, True)
                            dado_2.animacion(PANTALLA, 0, True)
                            pygame.display.flip()
                            time.sleep(0.05)
                        if miJugador.turno:
                            dadosjuego.reiniciar(dado_1.valor, dado_2.valor)
                            data = f"Dados:{dado_1.valor}:{dado_2.valor}"
                            s.send(data.encode('utf-8'))
                            print(f"Es mi turno, envío dados: {data}")
                        else:
                            dadosValor = s.recv(4096).decode('utf-8').split(":")
                            if dadosValor[0] == "Dados":
                                print(f"No es mi turno, recibo dados: {dadosValor}")
                                if len(dadosValor) == 3 and dadosValor[1].isdigit() and dadosValor[2].isdigit():
                                    dadosjuego.reiniciar(int(dadosValor[1]), int(dadosValor[2]))
                                    dado_1.animacion(PANTALLA, int(dadosValor[1]), False)
                                    dado_2.animacion(PANTALLA, int(dadosValor[2]), False)

                if contador >= 3:
                    logijuego.pasarturnoo()
                    contador = 0

                if playdados and clickdado(mx, my) == "dado":
                    for _ in range(1, 10):
                        dado_1.animacion(PANTALLA, 0, True)
                        dado_2.animacion(PANTALLA, 0, True)
                        pygame.display.flip()
                        time.sleep(0.05)
                    if miJugador.turno:
                        dadosjuego.reiniciar(dado_1.valor, dado_2.valor)
                        data = f"Dados:{dado_1.valor}:{dado_2.valor}"
                        s.send(data.encode('utf-8'))
                        print(f"Es mi turno, envío dados: {data}")
                    else:
                        dadosValor = s.recv(4096).decode('utf-8').split(":")
                        if dadosValor[0] == "Dados":
                            print(f"No es mi turno, recibo dados: {dadosValor}")
                            if len(dadosValor) == 3 and dadosValor[1].isdigit() and dadosValor[2].isdigit():
                                dadosjuego.reiniciar(int(dadosValor[1]), int(dadosValor[2]))
                                dado_1.animacion(PANTALLA, int(dadosValor[1]), False)
                                dado_2.animacion(PANTALLA, int(dadosValor[2]), False)
                    playdados = False
                else:
                    print("TIRAR DADOS POR FAVOR")

                if not playdados:
                    logijuego.jugar(lista_jugadores, click(mx, my), dadosjuego, table)

                if not logijuego.turno and not playdados:
                    table.dibujarmapa()
                    table.ponerjugadores(lista_jugadores)
                    if dado_1.valor != dado_2.valor:
                        logijuego


main()

##ERROR 41 42
##ERROR EN EL 8
##ERROR EN EL 68
##ERROR 27 28
