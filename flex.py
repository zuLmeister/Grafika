import pygame
from pygame import gfxdraw

pygame.init()
# Bikin window
SCREEN = pygame.display.set_mode((1000, 640), pygame.RESIZABLE)
# Buat title
pygame.display.set_caption("Lensa Cembung")

# Color
WHITE = (255,255,255)
BLACK = (0,0,0)

RED = (200, 0, 0)
GREEN = (0, 200, 0)
GOLD = (217, 175, 55)


# Konfersi kordinat titik
def cv_coor(x, y):
	# Kuadran ke 2
	x = SCREEN.get_width()//2 + x * -1
	y = SCREEN.get_height()//2 + y * -1
	return x, y



def DDA(xy1, xy2, color):
	# Variabel lokal [0, 1] (x, y)
	x = xy1[0]
	y = xy1[1]

	# Ambil Panjangnya kordinat
	dx = xy2[0] - xy1[0]
	dy = xy2[1] - xy1[1]

	# Ambil kordinat ter-panjang
	step = max(abs(dx), abs(dy))

	# Ambil butuh brapa increment untuk x dan y
	xinc = dx/step
	yinc = dy/step

	# Gambar garisnya
	for i in range(step):
		x += xinc
		y += yinc
		gfxdraw.pixel(SCREEN, round(x), round(y), color)

FONT = pygame.font.Font(None, 24)

def draw_text(teks, x, y):
	text = FONT.render(teks, False, WHITE)
	text_pos = text.get_rect(centerx=x, centery=y - 15)
	SCREEN.blit(text, text_pos)

# atur gerakan
def atur_gerakan():
	global jarak_benda, tinggi_benda, fokus

	# Buat ngambil key yang ditekan
	keys = pygame.key.get_pressed()

	# Buat ngambil mouse yang ditekan
	mouse = pygame.mouse.get_pressed()
	mouse_pos = pygame.mouse.get_pos()

	if keys[pygame.K_RIGHT]:
		jarak_benda -= 1
	if keys[pygame.K_LEFT]:
		jarak_benda += 1
	if keys[pygame.K_UP]:
		tinggi_benda += 1
	if keys[pygame.K_DOWN]:
		tinggi_benda -= 1

	if keys[pygame.K_a]:
		fokus -= 1
	if keys[pygame.K_d]:
		fokus += 1

	if mouse[0] and not InputBox.check_mouse_col():
		jarak_benda = (mouse_pos[0] - SCREEN.get_width()//2) * -1
		tinggi_benda = (mouse_pos[1] - SCREEN.get_height()//2) * -1

class InputBox:
	all_input_box = []

	def __init__(self, x, y, w, h, value):
		self.rect = pygame.Rect(x, y, w, h)
		self.value = value
		self.text = str(value)
		self.active = False
		self.change = False
		self.all_input_box.append(self)

	def handle_event(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.rect.collidepoint(event.pos):
					self.active = not self.active
				else:
					self.active = False

			if event.type == pygame.KEYDOWN:
				if self.active:
					if event.key == pygame.K_RETURN:
						try:
							self.value = int(self.text)
						except:
							self.value = 100
						self.active = False
						self.change = True
					elif event.key == pygame.K_BACKSPACE:
						self.text = self.text[:-1]
					else:
						self.text += event.unicode

	def draw(self):
		if self.active:
			text_obj = FONT.render(str(self.text), False, GREEN)
		else:
			self.text = str(self.value)
			text_obj = FONT.render(str(self.text), False, WHITE)
		SCREEN.blit(text_obj, (self.rect.x, self.rect.y))

	def check_collisions(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			return True

	@classmethod
	def check_mouse_col(cls):
		if cls.all_input_box:
			for box in cls.all_input_box:
				if box.check_collisions():
					return True

jarak_benda = 180
tinggi_benda = 100
fokus = 100

jaraknya = InputBox(0, 0, 100, 24, jarak_benda)
tingginya = InputBox(0, 0, 100, 24, tinggi_benda)
fokusnya = InputBox(0, 0, 100, 24, fokus)


# Awal
def main():
	global jarak_benda, tinggi_benda, fokus
	# global input_jarak, input_tinggi, input_fokus
	run = True

	while run:
		# Gambar Background
		SCREEN.fill(BLACK)

		events = pygame.event.get()

		jaraknya.handle_event(events)
		tingginya.handle_event(events)
		fokusnya.handle_event(events)

		# Jarak benda
		if jaraknya.change:
			jarak_benda = jaraknya.value
			jaraknya.change = False
		else:
			jaraknya.value = abs(jarak_benda)

		# Tinggi Benda
		if tingginya.change:
			tinggi_benda = tingginya.value
			tingginya.change = False
		else:
			tingginya.value = tinggi_benda

		# Fokus
		if fokusnya.change:
			fokus = fokusnya.value
			fokusnya.change = False
		else:
			fokusnya.value = fokus


		# Buat bayangan
		try:
			jarak_bayangan = ((fokus * jarak_benda) / (jarak_benda - fokus)) * -1
		except:
			jarak_bayangan = 0
		else:
			try:
				tinggi_bayangan = (jarak_bayangan / jarak_benda) * tinggi_benda
			except:
				tinggi_bayangan = 0

		# Garis x
		x1, y1 = 0, SCREEN.get_height()//2
		x2, y2 = SCREEN.get_width(), SCREEN.get_height()//2
		DDA((x1, y1), (x2, y2), RED)

		# Garis y
		x1, y1 = SCREEN.get_width()//2, 0
		x2, y2 = SCREEN.get_width()//2, SCREEN.get_height()
		DDA((x1, y1), (x2,y2), RED)

		# Buat benda
		x1, y1 = cv_coor(jarak_benda, 0)
		x2, y2 = cv_coor(jarak_benda, tinggi_benda)
		pygame.draw.line(SCREEN, RED, (x1, y1), (x2, y2))


		# Buat titik fokus 1 kiri
		x1, y1 = cv_coor(fokus, 0)
		x2, y2 = cv_coor(fokus, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))
		draw_text("F", x2, y2)

		# titik fokus 2 kiri
		x1, y1 = cv_coor(fokus * 2, 0)
		x2, y2 = cv_coor(fokus * 2, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))
		draw_text("2F", x2, y2)

		# Buat titik fokus 1 kanan
		x1, y1 = cv_coor(fokus * -1, 0)
		x2, y2 = cv_coor(fokus * -1, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))
		draw_text("F", x2, y2)

		# titik fokus 2 kanan
		x1, y1 = cv_coor(fokus * 2 * -1, 0)
		x2, y2 = cv_coor(fokus * 2 * -1, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))
		draw_text("2F", x2, y2)

		# Box info
		teks = [
			f"Jarak Benda = ",
			f"Tinggi Benda = ",
			f"Titik Fokus = ",
			f"Jarak Bayangan = ",
			f"Tinggi Bayangan = ",
		]
		value = [
			jaraknya,
			tingginya,
			fokusnya,
			(int(jarak_bayangan)*-1),
			(int(tinggi_bayangan)*-1),
		]
		x1 = SCREEN.get_width() - 100
		y1 = 10
		# Mengambil 2 list
		for txt, val in zip(teks, value):
			# Eksekusi teksnya
			teks_obj = FONT.render(txt, False, WHITE)
			teks_rect = teks_obj.get_rect(topright=(x1, y1))
			SCREEN.blit(teks_obj, teks_rect)

			# eksekusi valuenya
			if type(val) == int:
				value_obj = FONT.render(str(val), False, WHITE)
				SCREEN.blit(value_obj, (x1, y1))
			else:
				# Ubah posisi rectangle
				val.rect.x, val.rect.y = x1, y1
				val.draw()

				# val["rect"].x = x1
				# val["rect"].y = y1

				# # Jika aktif, berubah warna hijau
				# if val["active"]:
				# 	value_obj = FONT.render(val["text"], False, (0,255,0))
				# else:
				# 	value_obj = FONT.render(val["text"], False, WHITE)

				# SCREEN.blit(value_obj, (x1, y1))
			y1 += 24

		# Benda
		# Buat sinar 1 ke tengah
		x1, y1 = cv_coor(jarak_benda * fokus, tinggi_benda)
		x2, y2 = cv_coor(0, tinggi_benda)
		pygame.draw.line(SCREEN, GOLD, (x1, y1), (x2,y2))

		# Buat sinar 1 ke fokus
		x1, y1 = cv_coor(0, tinggi_benda)
		x2, y2 = cv_coor(fokus * -1, 0)
		pygame.draw.line(SCREEN, GOLD, (x1, y1), (x2,y2))

		# Buat sinar 1 ke bayangan
		x1, y1 = cv_coor(fokus * -1, 0)
		x2, y2 = cv_coor(jarak_bayangan, tinggi_bayangan)
		pygame.draw.line(SCREEN, GOLD, (x1, y1), (x2,y2))


		# Buat bayangan
		x1, y1 = cv_coor(jarak_bayangan, 0)
		x2, y2 = cv_coor(jarak_bayangan, tinggi_bayangan)
		pygame.draw.line(SCREEN, RED, (x1, y1), (x2,y2))

		# Buat sinar 2 ke tengah
		x1, y1 = cv_coor(jarak_bayangan, tinggi_bayangan)
		x2, y2 = cv_coor(0, tinggi_bayangan)
		pygame.draw.line(SCREEN, GREEN, (x1, y1), (x2,y2))

		# Buat sinar 2 ke fokus
		x1, y1 = cv_coor(0, tinggi_bayangan)
		x2, y2 = cv_coor(fokus, 0)
		pygame.draw.line(SCREEN, GREEN, (x1, y1), (x2,y2))

		# Buat sinar 2 ke benda
		x1, y1 = cv_coor(fokus, 0)
		x2, y2 = cv_coor(jarak_benda, tinggi_benda)
		pygame.draw.line(SCREEN, GREEN, (x1, y1), (x2,y2))

		#buat sinar 1 benda ke benda 2
		x1, y1 = cv_coor(jarak_benda, tinggi_benda)
		x2, y2 = cv_coor(jarak_bayangan,tinggi_bayangan)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2, y2))


		atur_gerakan()

		# nampilin apa yg sudah di gambar
		pygame.display.flip()

		# event handler
		for event in events:
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False

if __name__ == "__main__":
	main()
	pygame.quit()
