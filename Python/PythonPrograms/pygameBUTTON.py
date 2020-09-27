import pygame
from queue import PriorityQueue
pygame.init()

WIDTH = 420
HEIGHT = 420

ROWS = 40
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Button")
font_button = pygame.font.SysFont('ocraextended', 17, bold = 1)

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
CYAN = (64, 224, 250)     #CUSTOM COLOR


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


save_button = Button(BLACK, 156, 310, 115, 40, 'Save Grid')
load_button = Button(BLACK, 285, 310, 115, 40, 'Load Grid')

def redrawbuttons():
    save_button.draw_button(WINDOW)
    load_button.draw_button(WINDOW)

def draw(window, width):
    window.fill(WHITE)
    redrawbuttons()
    pygame.display.update()



def main(window, width):
    run = True
    clicked = False
    while run:
        draw(window, width)

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
                    print("Pressed save button")

                if load_button.isOver(pos):
                    load_button.color = DARKGREY
                    print("Pressed load button")
        
    pygame.quit()

main(WINDOW, WIDTH)