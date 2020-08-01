# set up of the screen
import turtle
import time
import random

delay = 0.10

score = 0
hscore = 0
d = 42

window = turtle.Screen()
window.title("Snake Game")
window.bgcolor("black")
window.setup(width = 540,height = 580)
border = turtle.Turtle()
border.speed()
border.shape("square")
border.color("white")
border.hideturtle()
border.penup()
border.setposition(-253,-253)
border.pendown()
border.pensize(5)
for side in range(4):
	border.fd(506)
	border.lt(90)
	border.fillcolor("green")
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("Lime green")
pen.penup()
pen.goto(-250,258)
pen.hideturtle()
pen.write("Score: 0 ", align = "left", font = ("Comic Sans", 19, "normal"))
pen1 = turtle.Turtle()
pen1.speed(0)
pen1.shape("square")
pen1.color("Lime green")
pen1.penup()
pen1.goto(260,258)
pen1.hideturtle()
pen1.write("High Score: 0 ", align = "right", font = ("Comic Sans", 19, "normal"))

window.tracer(0) # turns off animation on the screen

# set up of turtle head
head = turtle.Turtle()
head.speed(0) # animation speed of head
head.shape("square")
head.color("green")
head.penup() # to prevent head from drawing a line
head.goto(0,0) # turtle starts at 0,0 by default
head.direction = "stop"

# turtle food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
# food.goto(1000,1000)
x = random.randrange(-240,240,20)
y = random.randrange(-240,240,20)
food.goto(x,y)

body = []

# functions
def go_up():
	if head.direction != "down" and d != 1:
		head.direction = "up"
		print(d, "go")
def go_down():
	if head.direction != "up" and d != 0:
		head.direction = "down"
		print(d, "go")
def go_left():
	if head.direction != "right" and d != 3:
		head.direction = "left"
		print(d, "go")
def go_right():
	if head.direction != "left" and d != 2:
		head.direction = "right"
		print(d, "go")
def stop():
	head.direction = "stop"


def move():
	
	global d

	if head.direction == "up":
		print(d, "move")
		d = 0
		print(d, "move")
		y = head.ycor()
		head.sety(y+20)
	if head.direction == "down":
		print(d, "move")
		d = 1
		print(d, "move")
		y = head.ycor()
		head.sety(y-20)
	if head.direction == "left":
		print(d, "move")
		d = 2
		print(d, "move")
		x = head.xcor()
		head.setx(x-20)
	if head.direction == "right":
		print(d, "move")
		d = 3
		print(d, "move")
		x = head.xcor()
		head.setx(x+20)

# key bindings
window.listen()
window.onkeypress(go_up,"w")
window.onkeypress(go_down,"s")
window.onkeypress(go_left,"a")
window.onkeypress(go_right,"d")
window.onkeypress(stop,"p")

# main game loop
while True:
	window.update()
	if head.direction != "stop":
		if head.xcor() > 240 or head.xcor() < -240 or head.ycor() > 240 or head.ycor() < -240:
			time.sleep(0.5)
			head.goto(0,0)
			head.direction = "stop"
			score = 0
			pen.clear()
			pen1.clear()
			pen.write(f"Score: {score} ", align = "left", font = ("Comic Sans", 19, "normal"))
			pen1.write(f"High Score: {hscore} ", align = "right", font = ("Comic Sans", 19, "normal"))
			for segment in body:
				segment.goto(1000,1000)
			body.clear()

		# here

		if head.distance(food)<20:
			x = random.randrange(-240,240,20)
			y = random.randrange(-240,240,20)
			#  x = random.randint(-240,240)
			#  y = random.randint(-240,240)
			food.goto(x,y)

			# adding body
			segment = turtle.Turtle()
			segment.speed(0)
			segment.shape("square")
			segment.color("lime green")
			segment.penup()
			body.append(segment)

			score+=1
			if score>hscore:
				hscore=score
			pen.clear()
			pen1.clear()
			pen.write("Score: {} ".format(score), align = "left", font = ("Comic Sans", 19, "normal"))
			pen1.write("High Score: {} ".format(hscore), align = "right", font = ("Comic Sans", 19, "normal"))
		# move the end body in reverse
		for i in range(len(body)-1, 0, -1):
			x = body[i-1].xcor()
			y = body[i-1].ycor()
			body[i].goto(x,y)
		# move 0 segment to head's coords
		if len(body)>0:
			x = head.xcor()
			y = head.ycor()
			body[0].goto(x,y)
		move()
		for segment in body:
			if segment.distance(head) < 20:
				time.sleep(0.5)
				head.goto(0,0)
				head.direction = "stop"
				for segment in body:
					segment.goto(1000,1000)
				body.clear()
				score = 0
				pen.clear()
				pen1.clear()
				pen.write("Score: {} ".format(score), align = "left", font = ("Comic Sans", 19, "normal"))
				pen1.write("High Score: {} ".format(hscore), align = "right", font = ("Comic Sans", 19, "normal"))

		time.sleep(delay)
window.mainloop()

'''r = random.randrange(1,20)
if r == 1:
	head.direction = "up"
elif r == 2:
	head.direction = "down"
elif r == 3:
	head.direction = "left"
elif r == 4:
	head.direction = "right"
else:
	head.direction = "stop"'''