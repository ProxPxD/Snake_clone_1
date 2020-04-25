import pygame

class Block:
    x = 0
    y = 0
    color = None


    def __init__(self, x, y, gameplay):
        self.x = x
        self.y = y
        self.gameplay = gameplay
        self.color = gameplay.SNAKE_COLOR

    def draw(self, screen):
        size = self.gameplay.blockSize
        gap = self.gameplay.gapSize
        startX = self.gameplay.startX
        startY = self.gameplay.startY

        pygame.draw.rect(screen, self.color, [startX + self.x * (size + gap), startY  + self.y * (size + gap), size, size])

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def __eq__(self, block):
        if self.x == block.x and self.y == block.y:
            return True

        return False