import pygame, sys
import math
from pygame.locals import *

from warna import COLORS
from font_teks import FontText


# Rumus GLBB
def glbb(velocity, acc, dt):
	s = velocity * dt + (acc * 0.5) * (dt * dt)
	return s

# Rumus GLBB set velocity akhir
def set_velocity_end(velocity_awal, acc, dt):
	velocity_akhir = velocity_awal + (acc * dt)
	return velocity_akhir

# Rumus rotasi
def rotasi(x, y, sudut):
	# Radian kecepatan sudut
	sudut = math.radians(sudut)

	# Cos Sin
	cos = math.cos(sudut)
	sin = math.sin(sudut)

	# Rumusnya
	x_baru = (x * cos) - (y * sin)
	y_baru = (x * sin) + (y * cos)

	return (x_baru, y_baru)




# Window
class Window:
	def __init__(self, screen_size):
		self.size = screen_size

		pygame.display.set_caption("GLBB")
		self.surface = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

		self.clock = pygame.time.Clock()
		self.run = True
		self.fps = 60

	def update(self):
		self.size = self.surface.get_size()
		self.surface.fill(COLORS.black)

# Bola
class Bola:
	def __init__(self, x, y, radius=50):
		# atribut bolanya
		self.x = x
		self.y = y
		self.radius = radius

		# atribut geraknya
		self.velocity_x = 0
		self.velocity_y = 0
		self.acc_x = 0
		self.acc_y = 0
		self.speed = 500
		self.bolax = 300
		self.bolay = 300
		self.size = 25

		# atribut lainnya
		self.tinggi_tanah = 450
		self.gesek = -1.2
		self.gravitasi = 100 * 9.8
		self.koefisien = 0.9
		self.sudut = 0

		self.titik = [
			(0, -self.radius),
			(0, self.radius),
		]

		self.titik_akhir = [
			(0, -self.radius),
			(0, self.radius),
		]

		# atribut boolean
		self.kanan = False
		self.kiri = False
		self.di_udara = False
		self.pantul = False
		self.perbesar = False
		self.perkecil = False
	

	def gambar(self, surface):
		pygame.draw.circle(surface, COLORS.white, (self.x, self.y), self.radius)

		titik_1 = (self.titik_akhir[0][0] + self.x,  self.titik_akhir[0][1] + self.y )
		titik_2 = (self.titik_akhir[1][0] + self.x,  self.titik_akhir[1][1] + self.y )
		
		pygame.draw.line(surface, COLORS.light_green, titik_1, titik_2, 5)


	def proses(self, dt, size):
		
		# perbesar/perkecil
		self.ubah_radius()

		# Movement horizontal (x)
		self.gerak_x(dt, size)

		# Movement vertical (y)
		self.gerak_y(dt)
		
		# Rotasi
		self.rotasi_titik()

	def mantul(self):
		jarak = self.tinggi_tanah - self.y + self.radius
		if jarak < 0:
			self.y -= 2 * jarak



	def gerak_x(self, dt, size):
		self.acc_x = 0
		
		# Setting akselerasi dari input user
		if self.kanan:
			self.acc_x += self.speed
		if self.kiri:
			self.acc_x -= self.speed

		# Hitung gesekannya
		self.acc_x += self.velocity_x * self.gesek

		# hitung perpindahannya
		s = glbb(self.velocity_x, self.acc_x, dt)
		# setting kecepatan akhir
		self.velocity_x = set_velocity_end(self.velocity_x, self.acc_x, dt)

		# masukin ke posisinya
		self.x += s

		# kasi batas biar berhenti
		if abs(self.velocity_x) < 0.1:
			self.velocity_x = 0

		# ==============================================

		# Menghitung sudut
		teta = s / self.radius
		teta = math.degrees(teta)
		self.sudut = (self.sudut + teta) % 360

		# 1. pas gerak ke kanan, bolanya mutar ke kanan
		# 2. untuk mutar, berarti ada penambahan di sudutnya
		# 3. sudutnya ditambah sama perubahan posisi benda / radiusnya

		# ==============================================

		# Batas kiri dan kanan
		if self.x < self.radius:
			self.x = self.radius
		elif self.x > size[0] - self.radius:
			self.x = size[0] - self.radius


	def gerak_y(self, dt):
		# Setting akselerasinya (cuman ada dari gravitasi)
		self.acc_y = 0
		self.acc_y += self.gravitasi

		# Cari perpindahannya
		s = glbb(self.velocity_y, self.acc_y, dt)
		# Setting kecepatan akhirnya
		self.velocity_y = set_velocity_end(self.velocity_y, self.acc_y, dt)

		# Tambahkan ke posisi bolanya
		self.y += s

		# ==============================================

		# Sentuh tanah
		if self.y > self.tinggi_tanah - self.size:
			if self.pantul:
				mantul()
				self.velocity_y = -1 * self.koefisien * self.velocity_y
				if abs(self.velocity_y) < 200: self.pantul = False
			else:
				self.velocity_y = 0
				self.di_udara = False
			self.bolay = self.tinggi_tanah - self.size


	def ubah_radius(self):

		if self.perbesar:
			self.radius += 1
		if self.perkecil:
			self.radius -= 1
		
		if self.radius < 10:
			self.radius = 10

		self.titik = [
			(0, -self.radius),
			(0, self.radius),
		]


	def rotasi_titik(self):
		for i in range(len(self.titik)):
			# titik x dan y = rotasi
			x = self.titik[i][0]
			y = self.titik[i][1]

			self.titik_akhir[i] = rotasi(x, y, self.sudut)





	def jump(self):
		if not self.di_udara:
			self.velocity_y -= 500
			self.di_udara = True
			self.pantul = True




	def ambil_input(self, events):

		for event in events:
			if event.type == KEYDOWN:
				if event.key == K_a:
					self.kiri = True
				if event.key == K_d:
					self.kanan = True
				if event.key == K_w:
					self.jump()
				if event.key == K_q:
					self.perbesar = True
				if event.key == K_e:
					self.perkecil = True


			if event.type == KEYUP:
				if event.key == K_a:
					self.kiri = False
				if event.key == K_d:
					self.kanan = False
				if event.key == K_q:
					self.perbesar = False
				if event.key == K_e:
					self.perkecil = False




def main():
	pygame.init()

	# Objek window
	window = Window((1000, 640))

	# Objek bola
	bola = Bola(400, 200)

	FontText.update()

	while window.run:
		events = pygame.event.get()

		# delta time
		dt = window.clock.tick(window.fps) * 0.001

		# update window
		window.update()

		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()


		# ===========  Proses
		# ambil input dulu
		bola.ambil_input(events)
		# baru di proses
		bola.proses(dt, window.size)


		# ===========  Gambar
		# bola
		bola.gambar(window.surface)
		# tanah
		pygame.draw.line(window.surface, COLORS.white, (0, bola.tinggi_tanah), (window.size[0], bola.tinggi_tanah))

		text = FontText.font_normal.render(f"Velocity x = {bola.velocity_x:.2F}", False, COLORS.white)
		window.surface.blit(text, (20, 20))
		text = FontText.font_normal.render(f"Velocity y = {bola.velocity_y:.2F}", False, COLORS.white)
		window.surface.blit(text, (20, 40))
		text = FontText.font_normal.render(f"sudut = {bola.sudut:.2F}", False, COLORS.white)
		window.surface.blit(text, (20, 60))

		pygame.display.flip()


if __name__ == "__main__":
	main()



