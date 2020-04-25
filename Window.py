import time

import pygame
from Gameplay import Gameplay
import threading


class Window:

    def __init__(self, gameplay):
        self.height = 560
        self.width = 840

        self.tickValue = 800

        pygame.init()

        pygame.display.set_caption("Snake 1.0")

        self.screen = pygame.display.set_mode((self.width, self.height))

        #self.clock = pygame.time.Clock()

        self.gameplay = gameplay


    def setTickValue(self, val):
        self.tickValue = val

    def handleEvents(self):
        quitted = False

        while not quitted:
            for event in pygame.event.get():

                self.gameplay.onPress(event)

                if event.type == pygame.QUIT or self.gameplay.hasQuitted() == True:
                    self.gameplay.quit()
                    quitted = True

        print("joined: <Event handling>")

    def run(self):

        quitted = False

        threading.Thread(target=self.handleEvents).start()

        #tick = 0
        while not quitted:

            if self.gameplay.isAiOn():

                self.gameplay.draw(self.screen)

                self.gameplay.aiEvent.set()

                self.gameplay.windowEvent.wait()
                self.gameplay.windowEvent.clear()
            else:
                time.sleep(self.tickValue)
                self.gameplay.draw(self.screen)
                self.gameplay.play()

            quitted = self.gameplay.hasQuitted()


            pygame.display.flip()
