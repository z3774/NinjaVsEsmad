#######################################################################

# This file is part of NinjaVsEsmad.

# NinjaVsEsmad is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# NinjaVsEsmad is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with NinjaVsEsmad.  If not, see <http://www.gnu.org/licenses/>.

#######################################################################

import pygame
from pygame.locals import *
from spritesheet import SpriteSheet

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)


# Initialize the game engine
pygame.init()

SCREEN_WIDHT	= 800
SCREEN_HEIGHT 	= 600

SCREEN_SIZE = [SCREEN_WIDHT,SCREEN_HEIGHT]
screen =  pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("NinjaVsEsmad")
clock = pygame.time.Clock()

class Ninja( pygame.sprite.Sprite ):
	vel_x = 0
	vel_y = 0

	walking_frames_l = []
	walking_frames_r = []

	direction = "R"

	nivel = None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		ancho = 40
		alto = 60

		self.image = pygame.Surface([ancho,alto])
		self.image.fill(RED)

		self.rect = self.image.get_rect()


		sprite_sheet = SpriteSheet("img/ninja.png")
		# Load all the right facing images into a list
		image = sprite_sheet.get_image(0, 0, 66, 90)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(66, 0, 66, 90)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(132, 0, 67, 90)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(0, 93, 66, 90)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(66, 93, 66, 90)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(132, 93, 72, 90)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(0, 186, 70, 90)
		self.walking_frames_r.append(image)

		# Load all the right facing images, then flip them
		# to face left.
		image = sprite_sheet.get_image(0, 0, 66, 90)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(66, 0, 66, 90)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(132, 0, 67, 90)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(0, 93, 66, 90)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(66, 93, 66, 90)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(132, 93, 72, 90)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(0, 186, 70, 90)
		image = pygame.transform.flip(image, True, False)
		self.walking_frames_l.append(image)

		# Set the image the player starts with
		self.image = self.walking_frames_r[0]

		# Set a referance to the image rect.
		self.rect = self.image.get_rect()

	def update(self):
		self.calc_grav()

		#mov izq der
		self.rect.x += self.vel_x
		pos = self.rect.x + self.nivel.mov_fondo
		if self.direction == "R":
			frame = (pos // 30) % len(self.walking_frames_r)
			self.image = self.walking_frames_r[frame]
		else:
			frame = (pos // 30) % len(self.walking_frames_l)
			self.image = self.walking_frames_l[frame]

		#revisar colision
		bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)

		for bloque in bloque_col_list:
				if self.vel_x > 0:
					self.rect.right = bloque.rect.left
				elif self.vel_x < 0:
					self.rect.left = bloque.rect.right

		#mov arriba y abajo

		self.rect.y += self.vel_y

		#se revisa el choque
		bloque_col_list = pygame.sprite.spritecollide(self,self.nivel.plataforma_lista,False)

		for bloque in bloque_col_list:
				if self.vel_y > 0:
					self.rect.bottom = bloque.rect.top
				elif self.vel_y < 0:
					self.rect.top = bloque.rect.bottom

				self.vel_y = 0


	def calc_grav(self):
		if self.vel_y == 0:
			self.vel_y = 1
		else:
			self.vel_y += 0.35

		#esta en el suelo
		if self.rect.y >= (SCREEN_HEIGHT - 70) - self.rect.height and self.vel_y >= 0:
			self.vel_y = 0
			self.rect.y = (SCREEN_HEIGHT - 70) - self.rect.height

	def salto(self):
		self.rect.y += 2
		plataforma_col_lista = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)
		self.rect.y -= 2

		#si se puede salta

		if len(plataforma_col_lista) > 0 or self.rect.bottom >= (SCREEN_HEIGHT - 70):
			self.vel_y = -9
			#self.vel_x = 6

	def ir_izq(self):
		self.vel_x = -3
		self.direction = "L"

	def ir_der(self):
		self.vel_x = 3
		self.direction = "R"

	def no_mover(self):
		self.vel_x = 0

class Plataforma(pygame.sprite.Sprite):
	def __init__ (self, ancho, alto):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([ancho,alto])
		self.image.fill(GREEN)

		self.rect = self.image.get_rect()

class Nivel(object):
	#lista sprite todos los niveles

	plataforma_lista = None
	enemigos_lista = None

	fondo = None
	mov_fondo = 0
    #limite = -1000

	def __init__(self,jugador):
		self.plataforma_lista = pygame.sprite.Group()
		self.enemigos_lista = pygame.sprite.Group()
		self.jugador = jugador

	def update(self):
		self.plataforma_lista.update()
		self.enemigos_lista.update()

	def draw(self, pantalla):
		pantalla.fill(BLUE)
		pantalla.blit(self.fondo,(self.mov_fondo // 2,0))

		self.plataforma_lista.draw(pantalla)
		self.enemigos_lista.draw(pantalla)

	def Mover_fondo(self, mov_x):
		self.mov_fondo += mov_x

		for platforma in self.plataforma_lista:
			platforma.rect.x += mov_x

		for enemigos in self.enemigos_lista:
			enemigos.rect.x += mov_x

class Nivel_01(Nivel):
	def __init__(self, jugador):
		Nivel.__init__(self, jugador)

		self.fondo = pygame.image.load("img/NinjaVsEsmad_back01.png").convert()
		self.limite = -4000

		nivel = [ 	[50,100,100,500],[50,10,300,500],[50,100,500,500],[50,10,700,500],[50,200,850,350],[50,10,1000,500],

		[50,100,200,400],[50,100,600,400],

		[50,10,300,300],[50,100,500,300],[50,10,700,300],
		]

		for plataforma in nivel:
			bloque = Plataforma(plataforma[0], plataforma[1])
			bloque.rect.x = plataforma[2]
			bloque.rect.y = plataforma[3]
			bloque.jugador = self.jugador
			self.plataforma_lista.add(bloque)


class Nivel_02(Nivel):
	def __init__(self,jugador):
		Nivel.__init__(self,jugador)

		self.fondo = pygame.image.load("img/NinjaVsEsmad_back01.png").convert()
		self.limite = -6000

		nivel = [ 	[50,10,100,300],[50,10,300,300],[50,10,500,300],[50,10,700,300],[50,10,900,300],[50,10,1100,300],

					[50,10,200,400],[50,10,600,400],

					[50,10,300,500],[50,10,500,500],[50,10,700,500],
				]

		for plataforma in nivel:
			bloque = Plataforma(plataforma[0], plataforma[1])
			bloque.rect.x = plataforma[2]
			bloque.rect.y = plataforma[3]
			bloque.jugador = self.jugador
			self.plataforma_lista.add(bloque)


def texto(text, font, color = BLACK):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()

def boton(msg,x,y,w,h,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	smallText = pygame.font.SysFont("impact",20)

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(screen, BLACK,(x,y,w,h))
		textSurf, textRect = texto(msg, smallText, WHITE)
		if click[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(screen, WHITE,(x,y,w,h))
		textSurf, textRect = texto(msg, smallText)

	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	screen.blit(textSurf, textRect)

def salir():
	pygame.quit()
	quit()

def intro():
    listo = False
    ver_inst = True
    pag = 1
    while listo == False and ver_inst:
    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			listo = True
    		if event.type == pygame.MOUSEBUTTONDOWN:
    			pag += 1
    			if pag == 3:
    				ver_inst = False

    	screen.fill(BLACK)

    	if pag == 1:
    		image = pygame.image.load("img/0_intro.png")
    		screen.blit(image,(0,0))

    	if pag == 2:
    		image = pygame.image.load("img/1_declaracion.png")
    		screen.blit(image,(0,0))

    	pygame.display.update()
        clock.tick(20)


def instrucciones():
	instrucciones = True
	while instrucciones:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(WHITE)

		image = pygame.image.load("img/3_instrucciones.png")
		screen.blit(image,(0,0))

		boton("Volver",300,520,200,50,menu)

		pygame.display.update()
		clock.tick(15)

def creditos():
	creditos = True
	while creditos:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(BLACK)

		#image = pygame.image.load("img/3_instrucciones.png")
		#screen.blit(image,(0,0))

		boton("Volver",10,10,100,30,menu)

		pygame.display.update()
		clock.tick(15)

def menu():
	menu = True
	while menu:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(WHITE)

		image = pygame.image.load("img/2_menu.png")
		screen.blit(image,(0,0))

		boton("Jugar",300,250,200,50,main)
		boton("Instrucciones",300,310,200,50,instrucciones)
		boton("Creditos",300,370,200,50,creditos)
		boton("Salir",300,440,200,50,salir)

		pygame.display.update()
		clock.tick(15)


def main():
	jugador = Ninja()

	nivel_lista = []
	nivel_lista.append( Nivel_01(jugador) )
	nivel_lista.append( Nivel_02(jugador) )
	nivel_lista.append( Nivel_01(jugador) )


	nivel_actual_no = 0
	nivel_actual = nivel_lista[nivel_actual_no]

	activos_sp_lista = pygame.sprite.Group()
	jugador.nivel = nivel_actual

	jugador.rect.x = 340
	jugador.rect.y = (SCREEN_HEIGHT - 70) - jugador.rect.height
	activos_sp_lista.add(jugador)

	fin = False
	reloj = pygame.time.Clock()

	while not fin:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				fin = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					jugador.ir_izq()
				if event.key == pygame.K_RIGHT:
					jugador.ir_der()
				if event.key == pygame.K_UP:
					jugador.salto()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and jugador.vel_x < 0:
					jugador.no_mover()
				if event.key == pygame.K_RIGHT and jugador.vel_x > 0:
					jugador.no_mover()

		activos_sp_lista.update()
		nivel_actual.update()

		#avanza a la derecha
		if jugador.rect.right >= 400:
			dif = jugador.rect.x - 400
			jugador.rect.x = 400
			nivel_actual.Mover_fondo(-dif)

		#avanza a la izquierda
		if jugador.rect.right <= 120:
			dif = 120 - jugador.rect.x
			jugador.rect.x = 120
			nivel_actual.Mover_fondo(dif)

		#final del nivel
		pos_actual = jugador.rect.x + nivel_actual.mov_fondo
		print pos_actual
		if (pos_actual < nivel_actual.limite):
			jugador.rect.x = 120
			if (nivel_actual_no < len(nivel_lista)-1):
				nivel_actual_no += 1
				nivel_actual = nivel_lista[nivel_actual_no]
				jugador.nivel = nivel_actual

		if jugador.rect.left < 0:
			jugador.rect.left = 0

		nivel_actual.draw(screen)
		activos_sp_lista.draw(screen)
		reloj.tick(60)
		pygame.display.flip()

if __name__ == "__main__":
		intro()
		menu()
		main()
