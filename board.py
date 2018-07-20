import pygame
import random
import readchar
import keyboard
import time
from box import Box
from player import Player

#Initialize the game engine
pygame.init()

#Define the colors we will use in RGB format
BLACK = (  0,   0,   0) #For edges between boxes
WHITE = (255, 255, 255) #Default background color
BLUE =  (  0,   0, 255) #For visited box
GREEN =  (  0,   255, 0) #For current box
RED = (255, 0, 0) #For end block
YELLOW = (255, 255, 0) #For point block

#Set the height and width of the screen
size = [600, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze")

# Variables
score = 0
cols = 20 #The number of columns of the maze
stop = False #Loop maze generator until made
done = False #Loop until the user clicks the close button.
width = int(size[0]/cols) #The width of each box
stack = [] #The stack of cells used for backtracking
bottomright = cols - 1 # Used for end block
grid = [ [ Box() for x in range(cols) ] for y in range(cols) ] #A grid of boxes ie rectangular boxes
grid[0][0].visited = True # start point for maze generator
grid[bottomright][bottomright].end = True # Creates end block
currentX = 0
currentY = 0
player = Player()
clock = pygame.time.Clock()

# 3 random blocks you must get before completing
grid[random.randint(0, cols - 2)][random.randint (0, cols - 2)].value = True
grid[random.randint(0, cols - 2)][random.randint (0, cols - 2)].value = True
grid[random.randint(0, cols - 2)][random.randint (0, cols - 2)].value = True

#Remove an edge between current and next box
def removeEdge(currentX,currentY,nextX,nextY):
    xDiff = int( currentX - nextX )
    if xDiff == 1:
        #Remove current's left and next's right
        grid[currentX][currentY].draw[3] = False
        grid[nextX][nextY].draw[2] = False
    elif xDiff == -1:
        #Remove current's right and next's left
        grid[currentX][currentY].draw[2] = False
        grid[nextX][nextY].draw[3] = False

    yDiff = int( currentY - nextY )
    if yDiff == 1:
        #Remove current's bottom and next's top
        grid[currentX][currentY].draw[0] = False
        grid[nextX][nextY].draw[1] = False
    elif yDiff == -1:
        #Remove current's top and next's bottom
        grid[currentX][currentY].draw[1] = False
        grid[nextX][nextY].draw[0] = False

#Draw the grid based on which boxes are visited and which edges of each box are to be drawn
def confgGrid():
    global stop
    while not stop:
        global currentX,currentY
        #Set current box as visited
        grid[currentX][currentY].visited = True
        #Choose a next neighbour that has not yet been visited and set it as the current box
        nextX,nextY = selectNeighbour(currentX,currentY)
        if nextX != -1:
            #Push current cell to stack
            stack.append([ currentX,currentY ])
            #Remove wall between current and next box and update currentX and currentY
            removeEdge(currentX,currentY,nextX,nextY)
            currentX = nextX
            currentY = nextY
        elif len(stack):
            #Remove a cell from stack and make it the current cell
            currentX,currentY = stack.pop()
            if stack == []:
                print("complete")
                stop = True
            else:
                pass

def selectNeighbour(x,y):
    #Select a random neighbour out of TBRL that has not been visited and return it
    neighbours = []
    #Top neighbour
    if y>0 and not grid[x][y-1].visited:
        neighbours.append( [x,y-1] )
    #Bottom neighbour
    if y<cols-1 and not grid[x][y+1].visited:
        neighbours.append( [x,y+1] )
    #Left neighbour
    if x>0 and not grid[x-1][y].visited:
        neighbours.append( [x-1,y] )
    #Right neighbour
    if x<cols-1 and not grid[x+1][y].visited:
        neighbours.append( [x+1,y] )

    if not len(neighbours):
        return( [ -1,-1 ] )
    n = neighbours[ random.randint(0,len(neighbours)-1) ]
    return n

def drawGrid():
    for x in range(cols):
        for y in range(cols):
            if grid[x][y].visited:
                pygame.draw.rect(screen, BLUE, [(x)*width, (y)*width, width, width])
            if grid[x][y].end:
                pygame.draw.rect(screen, RED, [(x)*width, (y)*width, width, width])
            if grid[x][y].value:
                pygame.draw.rect(screen, YELLOW, [(x)*width, (y)*width, width, width])
            #TBRL
            if grid[x][y].draw[0]:
                pygame.draw.line(screen, BLACK, [(x)*width,(y)*width], [(x+1)*width,(y)*width], 5)
            if grid[x][y].draw[1]:
                pygame.draw.line(screen, BLACK, [(x)*width,(y+1)*width], [(x+1)*width,(y+1)*width], 5)
            if grid[x][y].draw[2]:
                pygame.draw.line(screen, BLACK, [(x+1)*width,(y)*width], [(x+1)*width,(y+1)*width], 5)
            if grid[x][y].draw[3]:
                pygame.draw.line(screen, BLACK, [(x)*width,(y)*width], [(x)*width,(y+1)*width], 5)

def drawPlayer():
    pygame.draw.rect(screen, GREEN, [(player.x)*width + 6, (player.y)*width + 5, width - 10 , width - 10])

while not done:
    #Exit when user clicks close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    #Clear the screen and set the screen background
    screen.fill(WHITE)
    confgGrid()
    drawGrid()
    key_pressed = pygame.key.get_pressed()
    if player.x == cols - 1: # Blocks moving out of screen right
        pass
    else:
        if key_pressed[pygame.K_RIGHT]:
            if grid[player.x + 1][player.y].draw[3]:
                pass
            else:
                if grid[player.x + 1][player.y].value:
                    score = score + 1
                    grid[player.x + 1][player.y].value = False
                player.x = player.x + 1
                time.sleep(.25)
    if key_pressed[pygame.K_LEFT]:
        if grid[player.x - 1][player.y].draw[2]:
            pass
        else:
            if grid[player.x - 1][player.y].value:
                score = score + 1
                grid[player.x - 1][player.y].value = False
            player.x = player.x - 1
            time.sleep(.25)
    elif key_pressed[pygame.K_UP]:
        if grid[player.x][player.y - 1].draw[1]:
            pass
        else:
            if grid[player.x][player.y - 1].value:
                score = score + 1
                grid[player.x][player.y - 1].value = False
            player.y = player.y - 1
            time.sleep(.25)
    if player.y == cols - 1: # Blocks moving out of screen down
        pass
    else:
        if key_pressed[pygame.K_DOWN]:
            if grid[player.x][player.y + 1].draw[0]:
                pass
            else:
                if grid[player.x][player.y + 1].value:
                    score = score + 1
                    grid[player.x][player.y + 1].value = False
                player.y = player.y + 1
                time.sleep(.25)
    drawPlayer()
    if player.x == bottomright and player.y == bottomright and score == 3:
        done = True
    pygame.display.flip()
