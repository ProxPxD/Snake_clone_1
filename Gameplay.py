import pygame
from Block import Block
from Snake import Snake
from SnakeAI import SnakeAI
import random
import threading

class Gameplay:

    ended = False
    pause = False
    gameOver = False

    cols = 40
    rows = 40

    boardSize = 0
    gapSize = 0
    blockSize = 0

    WHITE = [255, 255, 255]
    GRAY = [122, 122, 122]
    BLACK = [0, 0, 0]
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]

    SNAKE_COLOR = WHITE
    HEAD_COLOR = WHITE
    BACKGROUND_COLOR = BLACK
    FIELD_COLOR = [10, 10, 10]
    EDGE_COLOR = WHITE
    GRID_COLOR = [40, 40, 40]
    FOOD_COLOR = GREEN
    TEXT_COLOR = WHITE

    startX = 0
    startY = 0

    score = -1

    tick = 0

    snake = None
    food = None
    grid = None

    def __init__(self, width, height):
        self.boardSize = min(width, height) - 30
        self.gapSize = 0
        self.blockSize = self.boardSize // self.cols - self.gapSize

        self.startX = 1.5*self.blockSize
        self.startY = 1.5*self.blockSize

        self.areWalls = True

        self.windowEvent = threading.Event()
        self.aiEvent = threading.Event()

        self.aiIsOn = False

        self.setGame()

    def setGame(self):

        self.makeGrid()
        self.snake = Snake(self.cols // 2, self.rows // 2, self)
        self.randomFood()

        self.setColors()
        self.setPause(False)
        self.setGameOver(False)

    def endGame(self):
        self.ended = True

    def setPause(self, state):
        self.pause = state
        if state:
            self.SNAKE_COLOR = self.GRAY
            self.HEAD_COLOR = self.GRAY
            self.EDGE_COLOR = self.GRAY
        else:
            self.SNAKE_COLOR = self.WHITE
            self.HEAD_COLOR = self.WHITE
            self.EDGE_COLOR = self.WHITE

        self.setColors()

    def getPause(self):
        return self.pause

    def setGameOver(self, state):
        self.gameOver = state
        if state:
            self.SNAKE_COLOR = self.RED
            self.HEAD_COLOR = self.RED
            self.EDGE_COLOR = self.RED
        else:
            self.SNAKE_COLOR = self.WHITE
            self.HEAD_COLOR = self.WHITE
            self.EDGE_COLOR = self.WHITE

        self.setColors()

    def getTick(self):
        return self.tick

    def setTickValue(self, val):
        self.tick = val

    def makeTick(self):
        self.tick -= 1

    def isGameOver(self):
        return self.gameOver

    def hasQuitted(self):
        return self.ended

    def quit(self):

        self.ended = True

    def setEvents(self):
        self.windowEvent.set()
        self.aiEvent.set()

    def isAiOn(self):
        return self.aiIsOn

    def turnOnAi(self):
        ai = SnakeAI(self)
        self.ai = threading.Thread(target=ai.run)
        self.aiIsOn = True
        self.ai.start()

    def turnOffAi(self):
        self.aiIsOn = False

    def randomFood(self):
        x = random.randint(1, self.cols-2)
        y = random.randint(1, self.rows-2)
        block = self.grid[x][y]

        while self.snake.contains(block):
            x = random.randint(1, self.cols-2)
            y = random.randint(1, self.rows-2)
            block = self.grid[x][y]

        block.setColor(self.FOOD_COLOR)

        self.food = block

    def makeGrid(self):

        newGrid = []
        for i in range(self.cols):
            newGrid.append([])
            for j in range(self.rows):

                newGrid[i].append(Block(i, j, self))

        self.grid = newGrid

    def setColors(self):

        for i in range(self.cols):
            for j in range(self.rows):
                if i == 0 or i == self.cols - 1 or j == 0 or j == self.rows - 1:
                    if self.areWalls:
                        color = self.EDGE_COLOR
                    else:
                        color = self.FIELD_COLOR
                else:
                    color = self.FIELD_COLOR

                self.grid[i][j].setColor(color)

        self.snake.setColor()
        self.food.setColor(self.FOOD_COLOR)


    def onPress(self, event):

        key_pressed = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if key_pressed[pygame.K_LEFT] and not self.pause:
                self.snake.turnLeft()
            elif key_pressed[pygame.K_RIGHT] and not self.pause:
                self.snake.turnRight()

            if key_pressed[pygame.K_p]:
                self.setPause(not self.pause)
            elif key_pressed[pygame.K_r]:
                self.setGame()
                self.setGameOver(False)
            elif key_pressed[pygame.K_0]:
                if self.aiIsOn:
                    self.turnOffAi()
                else:
                    self.turnOnAi()

            if key_pressed[pygame.K_1]:
                self.gapSize = 0
                self.blockSize = self.boardSize // self.cols - self.gapSize
            elif key_pressed[pygame.K_2]:
                self.gapSize = 1
                self.blockSize = self.boardSize // self.cols - self.gapSize
            elif key_pressed[pygame.K_3]:
                self.gapSize = 4
                self.blockSize = self.boardSize // self.cols - self.gapSize

            if key_pressed[pygame.K_e]:
                self.areWalls = not self.areWalls
                self.setColors()

    def lock(self):
        self.gameplayLock.acquire()

    def unlock(self):
        self.gameplayLock.release()

    def play(self):
        if not self.pause and not self.gameOver:
            self.snake.move()


    def draw(self, screen):

        if self.score != self.snake.getScore() or self.pause or self.gameOver:
            self.drawBackground(screen)
            self.drawGrid(screen)

            self.food.draw(screen)

            self.score = self.snake.getScore()
            self.drawInfo(screen)
        else:
            self.drawGrid(screen)
            self.food.draw(screen)

    def drawBackground(self, screen):
        screen.fill(self.BLACK)

    def drawGrid(self, screen):
        for i in range(self.cols):
            for j in range(self.rows):
                x = self.startX + i * (self.blockSize + self.gapSize)
                y = self.startY + j * (self.blockSize + self.gapSize)
                pygame.draw.rect(screen, self.GRID_COLOR,
                                [x - self.gapSize, y - self.gapSize, self.blockSize + 2 * self.gapSize,
                                self.blockSize + 2 * self.gapSize])


                self.grid[i][j].draw(screen)


    def drawInfo(self, screen):

        font1 = pygame.font.SysFont("comicsansms", 42)
        font2 = pygame.font.SysFont("comicsansms", 24)

        info1 = "SNAKE!"
        info2 = "by Piotr Maliszewski"
        info3 = "Score: {}".format(self.score)

        text1 = font1.render(info1, True, self.TEXT_COLOR)
        text2 = font2.render(info2, True, self.TEXT_COLOR)
        text3 = font1.render(info3, True, self.TEXT_COLOR)

        screen.blit(text1, (self.boardSize + 3*(self.blockSize + self.gapSize), self.startY) )
        screen.blit(text2, (self.boardSize + 4*(self.blockSize + self.gapSize), self.startY + 4*(self.blockSize + self.gapSize)))
        screen.blit(text3, (self.boardSize + 3*(self.blockSize + self.gapSize), self.startY + 6*(self.blockSize + self.gapSize)))

        if self.gameOver:
            overText1 = font1.render("Game Over!", True, self.TEXT_COLOR)
            overText2 = font1.render("press r to restart", True, self.TEXT_COLOR)
            screen.blit(overText1, ((self.boardSize -overText1.get_width())//3, self.boardSize//3))
            screen.blit(overText2, ((self.boardSize -overText1.get_width())//3, self.boardSize//3 + 4*(self.blockSize + self.gapSize)))
        elif self.pause:
            pauseText1 = font1.render("Pause", True, self.TEXT_COLOR)
            pauseText2 = font1.render("press p to unpause", True, self.TEXT_COLOR)
            screen.blit(pauseText1, ((self.boardSize - pauseText1.get_width())//3, self.boardSize//3))
            screen.blit(pauseText2, ((self.boardSize - pauseText1.get_width())//3, self.boardSize//3 + 4*(self.blockSize + self.gapSize)))