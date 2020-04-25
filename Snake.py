import pygame
from Block import Block

class Snake:

    body = []
    gameplay = None
    grid = None

    dirX = -1
    dirY = 0

    toAdd = 0

    def __init__(self, x, y, gameplay):

        self.gameplay = gameplay
        self.grid = gameplay.grid

        self.body = []
        for i in range(3, 0, -1):
            self.body.append(self.grid[x + i][y])
            self.body[-1].setColor(gameplay.SNAKE_COLOR)

        self.body.append(self.grid[x][y])
        self.body[-1].setColor(gameplay.HEAD_COLOR)

        self.dirX = -1
        self.dirY = 0

        self.moved = True

    def turnRight(self):
        if self.moved:
            x = self.dirX
            y = self.dirY

            self.dirX = -y
            self.dirY = x

            self.moved = False


    def turnLeft(self):
        if self.moved:
            x = self.dirX
            y = self.dirY

            self.dirX = y
            self.dirY = -x

            self.moved = False

    def getHead(self):
        return self.body[-1]

    def getX(self):
        return self.body[-1].getX()

    def getY(self):
        return self.body[-1].getY()

    def contains(self, block):

        for part in self.body:
            if part == block:
                return True

        return False

    def setColor(self):

        for part in self.body:
            part.setColor(self.gameplay.SNAKE_COLOR)

        self.body[-1].setColor(self.gameplay.HEAD_COLOR)

    def getScore(self):
        points = len(self.body) - 4
        if self.gameplay.gameOver:
            points += 1
        return points

    def move(self):

        if self.toAdd > 0:
            self.toAdd -= 1
        else:
            self.body[0].setColor(self.gameplay.FIELD_COLOR)
            self.body = self.body[1:]

        head = self.body[-1]
        head.setColor(self.gameplay.SNAKE_COLOR)
        newX = head.x + self.dirX
        newY = head.y + self.dirY

        if newX == len(self.grid):
            newX = 0
        if newY == len(self.grid[newX]):
            newY = 0

        newHead = self.grid[newX][newY]

        if newHead.getColor() == self.gameplay.SNAKE_COLOR or newHead.getColor() == self.gameplay.EDGE_COLOR:
            self.gameplay.setGameOver(True)

        elif newHead.getColor() == self.gameplay.FOOD_COLOR:
            self.toAdd = 4
            self.gameplay.randomFood()
            newHead.setColor(self.gameplay.FIELD_COLOR)

        if newHead.getColor() == self.gameplay.FIELD_COLOR:
            newHead.setColor(self.gameplay.HEAD_COLOR)
            self.body.append(newHead)

        self.moved = True


