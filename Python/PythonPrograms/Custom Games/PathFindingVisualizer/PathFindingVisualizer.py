import pygame
import math
import pickle
import os
from queue import PriorityQueue
pygame.init()


WIDTH = 600
WIDTH_whole = 890
HEIGHT = 610

ROWS = 40
WINDOW = pygame.display.set_mode((WIDTH_whole, HEIGHT))
pygame.display.set_caption("Path Finding Visualizer")
font_box = pygame.font.SysFont('ocraextended', 20)
font_button = pygame.font.SysFont('ocraextended', 18, bold = 1)
font_screen = pygame.font.SysFont('ocraextended', 13)
font_screen_2 = pygame.font.SysFont('ocraextended', 20)
font_screen_list = pygame.font.SysFont('ocraextended', 17)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTGREEN = (51, 255, 51)
LIGHTERGREEN = (102, 255, 102)
DARKGREEN = (0, 200, 0)
BLUE = (50, 50, 255)
LIGHTBLUE = (90, 90, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
LIGHTGREY = (180, 180, 180)
DARKGREY = (40,40,40)
CYAN = (64, 224, 250)	  #CUSTOM COLOR

controls_text1 = 'LEFT MOUSE CLICK: Place Start/End/Barrier'
controls_text2 = 'RIGHT MOUSE CLICK: Remove Start/End/Barrier'
controls_text3 = 'SPACEBAR: Start algorithm'
controls_text4 = 'R: Reset Grid'
list_heading = 'SAVED GRIDS'
saved_list = []
for file in os.listdir("."):
	if "." in file or os.path.isdir(file):
		continue
	saved_list.append(file)

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


def draw(window, grid, rows, width, loadboxcolor, saveboxcolor, deleteboxcolor, load_txt_surface, save_txt_surface, delete_txt_surface):
	window.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(window)

	draw_gridlines(window, rows, width)

	redrawbutton()

	pygame.draw.rect(WINDOW, loadboxcolor, load_box, 2)
	pygame.draw.rect(WINDOW, saveboxcolor, save_box, 2)
	pygame.draw.rect(WINDOW, deleteboxcolor, delete_box, 2)
	WINDOW.blit(load_txt_surface, (load_box.x+7, load_box.y+6))
	WINDOW.blit(save_txt_surface, (save_box.x+7, save_box.y+6))
	WINDOW.blit(delete_txt_surface, (delete_box.x+7, delete_box.y+6))

	# message(controls_text1, BLACK, 4, 603)
	# message(controls_text2, BLACK, 4, 616)
	# message(controls_text3, BLACK, 4, 629)
	# message(controls_text4, BLACK, 4, 642)
	#message2(list_heading, CYAN, 684, 98)
	message2(list_heading, BLACK, 680, 138)

	messagelist(str(saved_list), PURPLE, 616, 166)

	#pygame.draw.line(window, GREY, (610, 0), (890, 0), 1)		#top
	#pygame.draw.line(window, GREY, (610, 47), (890, 47), 1)	  #top second
	pygame.draw.line(window, GREY, (610, 135), (880, 135), 1)	  #top third
	pygame.draw.line(window, GREY, (610, 163), (880, 163), 1)	  #top fourth
	pygame.draw.line(window, GREY, (610, 555), (880, 555), 1)	#bottom
	#pygame.draw.line(window, GREY, (0, 655), (600, 655), 1)	#bottom second
	pygame.draw.line(window, GREY, (610, 135), (610, 555), 1)	  #left
	pygame.draw.line(window, GREY, (880, 135), (880, 555), 1)	  #right
	# pygame.draw.line(window, GREY, (300, 600), (300, 655), 1)   #save/delete separation
	# pygame.draw.line(window, GREY, (600, 600), (600, 655), 1)   #right wall of delete
	# pygame.draw.line(window, GREY, (0, 600), (0, 655), 1)   #left wall of save

	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	x, y = pos

	row = x // gap
	col = y // gap

	return row, col

#BUTTON


class Button():
	def __init__(self, color, x, y, width, height, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text

	def draw_button(self,WINDOW,outline=GREY):
		#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(WINDOW, outline, (self.x-1,self.y-1,self.width+2,self.height+2),0)
			
		pygame.draw.rect(WINDOW, self.color, (self.x,self.y,self.width,self.height),0)
		
		if self.text != '':
			text = font_button.render(self.text, 1, BLACK)
			WINDOW.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

	def isOver(self, pos):
		#Pos is the mouse position or a tuple of (x,y) coordinates
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
			
		return False


ins_button = Button(BLACK, 611, 565, 269, 35, 'INSTRUCTIONS')

def redrawbutton():
	ins_button.draw_button(WINDOW)

def message(msg, color, x, y): 
	screen_text = font_screen.render(msg, 1, color)
	WINDOW.blit(screen_text, (x, y))

def message2(msg, color, x, y): 
	screen_text_2 = font_screen_2.render(msg, 1, color)
	WINDOW.blit(screen_text_2, (x, y))

def messagelist(msg, color, x, y):
	for word in saved_list:
		screen_text_list = font_screen_list.render(word, 1, color)
		WINDOW.blit(screen_text_list, (x, y))
		y += 17

load_box = pygame.Rect(610, 45, 270, 35)
save_box = pygame.Rect(610, 0, 270, 35)
delete_box = pygame.Rect(610, 90, 270, 35)


def main(window, width):
	#print(pygame.font.get_fonts())
	#print(os.listdir("."))
	print(saved_list)
	loadboxcolor = pygame.Color('lightgreen')
	saveboxcolor = pygame.Color('lightskyblue')
	deleteboxcolor = pygame.Color(255, 125, 125)
	grid = make_grid(ROWS, width)
	start = None
	end = None
	run = True
	loadactive = False
	saveactive = False
	deleteactive = False
	clicked = False
	instructions = False
	load_text = 'Enter to load grid'
	save_text = 'Enter to save grid'
	delete_text = 'Enter to delete grid'
	load_txt_surface = font_box.render(load_text, True, BLACK)
	save_txt_surface = font_box.render(save_text, True, BLACK)
	delete_txt_surface = font_box.render(delete_text, True, BLACK)
	while run:
		draw(window, grid, ROWS, width, loadboxcolor, saveboxcolor, deleteboxcolor, load_txt_surface, save_txt_surface, delete_txt_surface)
		for event in pygame.event.get():

			pos = pygame.mouse.get_pos()

			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.MOUSEMOTION and clicked == False:
				if ins_button.isOver(pos):
					ins_button.color = LIGHTERGREEN
				else:
					ins_button.color = LIGHTGREEN

			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
				if ins_button.isOver(pos):
					ins_button.color = DARKGREEN

			if event.type == pygame.MOUSEBUTTONUP:
				clicked = False
				if ins_button.isOver(pos):
					ins_button.color = LIGHTERGREEN
					print("Pressed ins button")
					if instructions == False:
						instructions = True
						pygame.display.set_mode((1190, HEIGHT))
					else:
						instructions = False
						pygame.display.set_mode((WIDTH_whole, HEIGHT))

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

				if delete_box.collidepoint(event.pos):
					deleteactive = True
					if delete_text == 'Enter to delete grid':
						delete_text = ''
				else:
					deleteactive = False
					if delete_text == '':
						delete_text = 'Enter to delete grid'


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
						#print(load_text)
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
						#print(save_text)
						try:
							with open(save_text, 'wb') as filehandle:	# store the data as binary data stream
								pickle.dump(grid, filehandle)
						except:
							pass
							
						saved_list.append(save_text)
						print(saved_list)
						save_text = ''
					elif event.key == pygame.K_BACKSPACE:
						save_text = save_text[:-1]
					else:
						save_text += event.unicode

				if deleteactive:
					if event.key == pygame.K_RETURN:
						#print(delete_text)
						try:
							os.remove(delete_text)
						except:
							pass

						saved_list.remove(delete_text)
						print(saved_list)
						delete_text = ''
					elif event.key == pygame.K_BACKSPACE:
						delete_text = delete_text[:-1]
					else:
						delete_text += event.unicode

				if not loadactive and not saveactive:
					if event.key == pygame.K_SPACE and start and end:	 #SPACEBAR
						for row in grid:
							for node in row:
								node.update_nieghbors(grid)

						algorithm(lambda: draw(window, grid, ROWS, width, loadboxcolor, saveboxcolor, deleteboxcolor, load_txt_surface, save_txt_surface, delete_txt_surface), grid, start, end)


					if event.key == pygame.K_r:		 #KEY 'r'
						start = None
						end = None
						grid = make_grid(ROWS, width)

		if loadactive:
			loadboxcolor = pygame.Color(0, 220, 0)
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


		if deleteactive:
			deleteboxcolor = pygame.Color(255, 40, 40)
			delete_txt_surface = font_box.render(delete_text, True, (255, 40, 40))
		else:
			deleteboxcolor = pygame.Color(255, 125, 125)
			delete_txt_surface = font_box.render(delete_text, True, (255, 125, 125))



	pygame.quit()

main(WINDOW, WIDTH)