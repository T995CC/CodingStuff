import pygame
import math
import time
from queue import PriorityQueue
pygame.init()

WIDTH = 600
HEIGHT = 660
ROWS = 40
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Visualizer")
font_button = pygame.font.SysFont('ocraextended', 17, bold = 1)
font_screen = pygame.font.SysFont('ocraextended', 13)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 110, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
DARKGREY = (77, 77, 77)
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
		for j in range(rows):
			pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))

def draw(window, grid, rows, width):
	window.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(window)

	draw_gridlines(window, rows, width)
	redrawbuttons()
	message(controls_text1, BLACK, 4, 603)
	message(controls_text2, BLACK, 4, 616)
	message(controls_text3, BLACK, 4, 629)
	message(controls_text4, BLACK, 4, 642)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	x, y = pos

	row = x // gap
	col = y // gap

	return row, col


#BUTTONS


class Button():
	def __init__(self, color, x,y,width,height, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text

	def draw_button(self,WINDOW,outline=GREY):
		#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(WINDOW, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
			
		pygame.draw.rect(WINDOW, self.color, (self.x,self.y,self.width,self.height),0)
		
		if self.text != '':
			text = font_button.render(self.text, 1, WHITE)
			WINDOW.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

	def isOver(self, pos):
		#Pos is the mouse position or a tuple of (x,y) coordinates
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
			
		return False


save_button = Button(BLACK, 354, 610, 115, 40, 'Save Grid')
load_button = Button(BLACK, 477, 610, 115, 40, 'Load Grid')

def redrawbuttons():
	save_button.draw_button(WINDOW)
	load_button.draw_button(WINDOW)

def message(msg, color, x, y):
	screen_text = font_screen.render(msg, 1, color)
	WINDOW.blit(screen_text, (x, y))


def main(window, width):
	#print(pygame.font.get_fonts())
	grid = make_grid(ROWS, width)
	start = None
	end = None
	run = True
	clicked = False
	while run:
		draw(window, grid, ROWS, width)
		for event in pygame.event.get():

			pos = pygame.mouse.get_pos()

			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEMOTION and clicked == False:
				if save_button.isOver(pos):
					save_button.color = DARKGREY
				else:
					save_button.color = BLACK

				if load_button.isOver(pos):
					load_button.color = DARKGREY
				else:
					load_button.color = BLACK

			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
				if save_button.isOver(pos):
					save_button.color = DARKGREEN
				if load_button.isOver(pos):
					load_button.color = DARKGREEN

			if event.type == pygame.MOUSEBUTTONUP:
				clicked = False
				if save_button.isOver(pos):
					save_button.color = DARKGREY
					print("lol")
				if load_button.isOver(pos):
					load_button.color = DARKGREY
					print("hola")


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
				if event.key == pygame.K_SPACE and start and end:	 #SPACEBAR
					for row in grid:
						for node in row:
							node.update_nieghbors(grid)

					algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)


				if event.key == pygame.K_r:		 #KEY 'r'
					start = None
					end = None
					grid = make_grid(ROWS, width)


	pygame.quit()

main(WINDOW, WIDTH)