import pygame, sys
from pygame.locals import *
import math

#from warna import COLORS
#from font_teks import FontText

GOLD = (255,215,0)
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
bg = pygame.image.load('Background.PNG')

# Window
class Window:
	def __init__(self, screen_size):
		self.size = screen_size

		pygame.display.set_caption("Gerak Lurus Berubah Beraturan")
		self.surface = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

		self.clock = pygame.time.Clock()
		self.run = True
		self.fps = 60

	def update(self):
		self.size = self.surface.get_size()
		self.surface.fill(BLACK)
	

def proses(dt):
	global Bola_y, vel_y, Bola_x, vel_x, kiri, kanan, di_udara, bounce

	# Jalan
	acc_x = 0
	if kiri:
		acc_x -= speed
	if kanan:
		acc_x += speed
	
	acc_x += vel_x * gesek
	
	# Hitung glbbnya
	# s = Jarak
	s_x = vel_x * dt + (acc_x * 0.5) * (dt * dt)
	vel_x = vel_x + (acc_x * dt)

	Bola_x += s_x

	if abs(vel_x) < 0.1: vel_x = 0



	# Gravitasi
	acc_y = 0
	acc_y += gravitasi

	s_y = vel_y * dt + (acc_y * 0.5) * (dt * dt)
	vel_y += (acc_y * dt)

	Bola_y += s_y

	# sentuh tanah
	if Bola_y > tinggi_tanah - Bola_size:
		# Kalau mantul
		if bounce:
			mantul()
			vel_y = -1 * koefisien * vel_y
			if abs(vel_y) < 200: bounce = False
		else:
			vel_y = 0
			di_udara = False
		Bola_y = tinggi_tanah - Bola_size


# Lompat
def lompat():
	global vel_y, di_udara, bounce
	vel_y -= 500
	di_udara = True
	bounce = True

# benerin posisi
def mantul():
	global Bola_y, tinggi_tanah, vel_y, koefisien
	jarak = tinggi_tanah - Bola_y + Bola_size
	if jarak < 0:
		Bola_y -= 2 * jarak

#rumus glbb
def glbb(velocity,acc,dt):
	s = velocity * dt + (acc * 0,5) *(dt + dt)
	return s

#Rumus GLBB set velocity akhir
def KecepatanA(velocity_awal,acc,dt):
	velocityA =velocity_awal + (acc * dt)
	return velocityA

def rotate(x,y,teta):
	teta = math.radians(teta)

	#cos sin
	cos = math.cos(teta)
	sin = math.sin(teta)

	new_x = (x * cos) - (y * sin)
	new_y = (y * sin) + (y * cos)
	#return new_x



tinggi_tanah = 450

# Bola
Bola_x, Bola_y = 300, 300
Bola_size = 25

vel_x = vel_y = 0
speed = 200
gesek = -1.2
koefisien = 0.9

garis_bola = [
	(0, Bola_size),
	(0, -Bola_size),
]

kiri, kanan = False, False
di_udara = False
bounce = True


# World
gravitasi = 100 * 9.8





def main():
	global kiri, kanan, di_udara, Bola_x, Bola_y
	pygame.init()

	window = Window((1000, 640))
	#window.blit(bg, (0, 0))

	while window.run:
		events = pygame.event.get()
		dt = window.clock.tick(window.fps) * 0.001
		window.update()

		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					Bola_x = event.pos[0]
					Bola_y = event.pos[1]

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_LEFT:
					kiri = True
				if event.key == K_RIGHT:
					kanan = True
				if event.key == K_SPACE:
					if not di_udara:
						lompat()

			if event.type == KEYUP:
				if event.key == K_LEFT:
					kiri = False
				if event.key == K_RIGHT:
					kanan = False

		# Proses

		proses(dt)


		# ===========  Gambar
		# Bola
		pygame.draw.circle(window.surface, GOLD, (Bola_x, Bola_y), Bola_size)

		# Garis bola
		xy1 = garis_bola[0][0] + Bola_x, garis_bola[0][1] + Bola_y
		xy2 = garis_bola[1][0] + Bola_x, garis_bola[1][1] + Bola_y
		pygame.draw.line(window.surface, RED, xy1, xy2, 5)

		# Tanah
		pygame.draw.line(window.surface, WHITE, (0, tinggi_tanah), (window.size[0], tinggi_tanah))

		pygame.display.flip()


if __name__ == "__main__":
	main()

