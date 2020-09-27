import pygame
import math
import pickle
import os
from queue import PriorityQueue
pygame.init()


WIDTH = 600
WIDTH_whole = 900
HEIGHT = 660

ROWS = 40
WINDOW = pygame.display.set_mode((WIDTH_whole, HEIGHT))
pygame.display.set_caption("A* Path Finding Visualizer")
font_box = pygame.font.SysFont('ocraextended', 20)
font_screen = pygame.font.SysFont('ocraextended', 13)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTGREEN = (125, 255, 125)
DARKGREEN = (0, 110, 0)
BLUE = (50, 50, 255)
LIGHTBLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
DARKGREY = (40,40,40)
CYAN = (64, 224, 250)	  #CUSTOM COLOR

controls_text1 = 'LEFT MOUSE CLICK: Place Start/End/Barrier'
controls_text2 = 'RIGHT MOUSE CLICK: Remove Start/End/Barrier'
controls_text3 = 'SPACEBAR: Start algorithm'
controls_text4 = 'R: Reset Grid'

class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col
	
	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == CYAN

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = YELLOW

	def make_barrier(self):
		self.color = BLACK
	
	def make_start(self):
		self.color = ORANGE

	def make_end(self):
		self.color = CYAN

	def make_path(self):
		self.color = GREEN


	def draw(self, window):
		pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

	def update_nieghbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():	  #DOWN
			self.neighbors.append(grid[self.row + 1][self.col])
		
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():						#UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():	  #RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():						#LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

	
def h(p1, p2):			 #Heuristic function
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1- x2) + abs(y1 - y2)

def recreate_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

					
		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			recreate_path(came_from, current, draw)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		
		draw()

		if current != start:
			current.make_closed()
		

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid

def draw_gridlines(window, rows, width):
	gap = width // rows
	for i in range(rows + 1):
		pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows + 1):
			pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width, loadboxcolor, saveboxcolor, load_txt_surface, save_txt_surface):
	window.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(window)

	draw_gridlines(window, rows, width)

	pygame.draw.rect(WINDOW, loadboxcolor, load_box, 2)
	pygame.draw.rect(WINDOW, saveboxcolor, save_box, 2)
	WINDOW.blit(load_txt_surface, (load_box.x+5, load_box.y+5))
	WINDOW.blit(save_txt_surface, (save_box.x+5, save_box.y+5))

	message(controls_text1, BLACK, 4, 603)
	message(controls_text2, BLACK, 4, 616)
	message(controls_text3, BLACK, 4, 629)
	message(controls_text4, BLACK, 4, 642)

	pygame.draw.line(window, GREY, (610, 0), (890, 0), 1)        #top
	pygame.draw.line(window, GREY, (610, 47), (890, 47), 1)      #top second
	pygame.draw.line(window, GREY, (610, 603), (890, 603), 1)    #bottom
	pygame.draw.line(window, GREY, (610, 650), (890, 650), 1)    #bottom second
	pygame.draw.line(window, GREY, (610, 0), (610, 650), 1)      #left
	pygame.draw.line(window, GREY, (890, 0), (890, 650), 1)      #right
	

	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	x, y = pos

	row = x // gap
	col = y // gap

	return row, col


def message(msg, color, x, y):
	screen_text = font_screen.render(msg, 1, color)
	WINDOW.blit(screen_text, (x, y))


load_box = pygame.Rect(617, 6, 267, 35)
save_box = pygame.Rect(617, 609, 267, 35)


def main(window, width):
	#print(pygame.font.get_fonts())
	print(os.listdir("C:/Users/Absaar/Documents/CodingStuff"))
	loadboxcolor = pygame.Color('LIGHTGREEN')
	saveboxcolor = pygame.Color('lightskyblue')
	clock = pygame.time.Clock()
	grid = make_grid(ROWS, width)
	start = None
	end = None
	run = True
	loadactive = False
	saveactive = False
	load_text = 'Enter to load grid'
	save_text = 'Enter to save grid'
	load_txt_surface = font_box.render(load_text, True, BLACK)
	save_txt_surface = font_box.render(save_text, True, BLACK)
	while run:
		draw(window, grid, ROWS, width, loadboxcolor, saveboxcolor, load_txt_surface, save_txt_surface)
		for event in pygame.event.get():

			pos = pygame.mouse.get_pos()

			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if load_box.collidepoint(event.pos):
					loadactive = True
					if load_text == 'Enter to load grid':
						load_text = ''
				else:
					loadactive = False
					if load_text == '':
						load_text = 'Enter to load grid'

				if save_box.collidepoint(event.pos):
					saveactive = True
					if save_text == 'Enter to save grid':
						save_text = ''
				else:
					saveactive = False
					if save_text == '':
						save_text = 'Enter to save grid'


			if pygame.mouse.get_pressed()[0]:	 #LEFT MOUSE BUTTON
				pos1 = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos1, ROWS, width)
				try:
					node = grid[row][col]
				except:
					continue
				if not start and node != end:
					start = node
					start.make_start()
				elif not end and node != start:
					end = node
					end.make_end()
				elif node != start and node != end:
					node.make_barrier()


			elif pygame.mouse.get_pressed()[2]:   #RIGHT MOUSE BUTTON
				pos1 = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos1, ROWS, width)
				try:
					node = grid[row][col]
				except:
					continue
				node.reset()
				if node == start:
					start = None
				if node == end:
					end = None
			
			if event.type == pygame.KEYDOWN:
				if loadactive:
					if event.key == pygame.K_RETURN:
						print(load_text)
						try:
							with open(load_text, 'rb') as filehandle:	# read the data as binary data stream
								grid = pickle.load(filehandle)
						except:
							pass
						for row in grid:
							for node in row:
								if node.color == ORANGE:
									start = node
									start.make_start()
								elif node.color == CYAN:
									end = node
									end.make_end()
								elif node.color == BLACK:
									node.make_barrier()
						load_text = ''
					elif event.key == pygame.K_BACKSPACE:
						load_text = load_text[:-1]
					else:
						load_text += event.unicode

				if saveactive:
					if event.key == pygame.K_RETURN:
						print(save_text)
						try:
							with open(save_text, 'wb') as filehandle:	# store the data as binary data stream
								pickle.dump(grid, filehandle)
						except:
							pass
						save_text = ''
					elif event.key == pygame.K_BACKSPACE:
						save_text = save_text[:-1]
					else:
						save_text += event.unicode

				if not loadactive and not saveactive:
					if event.key == pygame.K_SPACE and start and end:	 #SPACEBAR
						for row in grid:
							for node in row:
								node.update_nieghbors(grid)

						algorithm(lambda: draw(window, grid, ROWS, width, loadboxcolor, saveboxcolor, load_txt_surface, save_txt_surface), grid, start, end)


					if event.key == pygame.K_r:		 #KEY 'r'
						start = None
						end = None
						grid = make_grid(ROWS, width)

		if loadactive:
			loadboxcolor = pygame.Color('green')
			load_txt_surface = font_box.render(load_text, True, BLACK)
		else:
			loadboxcolor = pygame.Color('lightgreen')
			load_txt_surface = font_box.render(load_text, True, GREY)


		if saveactive:
			saveboxcolor = pygame.Color('dodgerblue')
			save_txt_surface = font_box.render(save_text, True, BLACK)
		else:
			saveboxcolor = pygame.Color('lightskyblue')
			save_txt_surface = font_box.render(save_text, True, GREY)



	pygame.quit()

main(WINDOW, WIDTH)