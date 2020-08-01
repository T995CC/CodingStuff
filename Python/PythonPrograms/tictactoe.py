print("\t\t\t\t\t\tWELCOME TO TIC TAC TOE")
print("\nTIC TAC TOE is a classic two player game. One player represents 'X' and the other represents 'O'.")
print("\nRULES:\n\t1. The game is played on a 3x3 grid.\n\t2. Player 'X' always plays first.\n\t3. First player to complete one row,column or diagonal with their mark wins the game.")
print("\nEXAMPLE GRID:\n\t\t1|2|3\n\t\t-----\n\t\t4|5|6\n\t\t-----\n\t\t7|8|9")
print("\nHOW TO PLAY:\n\tEnter the coordinate in which you'd like to place your mark. Refer to the EXAMPLE GRID for position of each coordinate.")
print("\nSCORING:\n\tWinner is granted 1 point.\n\t")
tie=0
def game(p, q):
	global tie
	xs = p
	os = q
	g=[[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
	j=0
	while True:
		for i in range(0,3):
			if g[i][0]==g[i][1]==g[i][2] and g[i][0]!=" ":
				if g[i][0]=='X':
					print("\nPLAYER X WINS!")
					xs+=1
					score(xs,os)
				else:
					print("\nPLAYER O WINS!")
					os+=1
					score(xs,os)
			elif g[0][i]==g[1][i]==g[2][i] and g[0][i]!=" ":
				if g[0][i]=='X':
					print("\nPLAYER X WINS!")
					xs+=1
					score(xs,os)
				else:
					print("\nPLAYER O WINS!")
					os+=1
					score(xs,os)
			elif g[0][0]==g[1][1]==g[2][2] and g[0][0]!=" ":
				if g[0][0]=='X':
					print("\nPLAYER X WINS!")
					xs+=1
					score(xs,os)
				else:
					print("\nPLAYER O WINS!")
					os+=1
					score(xs,os)
			elif g[0][2]==g[1][1]==g[2][0] and g[0][2]!=" ":
				if g[0][2]=='X':
					print("\nPLAYER X WINS!")
					xs+=1
					score(xs,os)
				else:
					print("\nPLAYER O WINS!")
					os+=1
					score(xs,os)
			elif j==9:
				print("\nIT'S A TIE!")
				tie+=1
				score(xs,os)
		if j%2==0:
			print("\nPlayer X's turn: ",end="")
		else:
			print("\nPlayer O's turn: ",end="")
		try:
			p=int(input(""))
			skip=False
			if 0 < p < 10:
				if g[(p-1)//3][(p-1)%3]!=" ":
					print("\nPlease enter a coordinate that has no mark")
					j-=1
					skip=True
				if j%2==0:
					if skip==False:
						g[(p-1)//3][(p-1)%3]='X'
				else:
					if skip==False:
						g[(p-1)//3][(p-1)%3]='O'
				j+=1
			else:
				print("\nPlease enter a numeric value ranging from 1 to 9")
		except:
			print("\nPlease enter a numeric value ranging from 1 to 9")
		row1p="|".join(g[0])
		row2p="|".join(g[1])
		row3p="|".join(g[2])
		print()
		print(row1p)
		print("-----")
		print(row2p)
		print("-----")
		print(row3p)

def score(a,b):
	print("\nX Score =",a,"\nO Score =",b,"\nTie counter =",tie)
	while True:
		c=input("\nWould you like to play again?(Y/N)\n")
		if c.lower()=='y' or c.lower()=='yes':
			print ("New game started... \n")
			game(a, b)
		elif c.lower()=='n' or c.lower()=='no':
			exit()
		else:	
			print("Please enter Yes or No")
def start():
	while True:
		start=input("\nWould you like to start the game?(Y/N)\n")
		if start.lower()=='y' or start.lower()=='yes':
			print("The game has started...")
			print("\n | | \n-----\n | | \n-----\n | | ")
			game(0, 0)
		elif start.lower()=='n' or start.lower()=='no':
			exit()
		else:	
			print("Please enter Yes or No")
start()

