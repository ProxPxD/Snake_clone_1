import threading
import time


class SnakeAI:

    gameplay = None
    memory = None

    def __init__(self, gameplay):
        self.gameplay = gameplay
        self.memory = []

    def run(self):
        quitted = False
        flag = False
        while not quitted:

            self.gameplay.aiEvent.wait()
            self.gameplay.aiEvent.clear()

            if flag:
                self.gameplay.snake.turnRight()
                flag = False
            else:
                flag = True

            self.gameplay.play()

            self.gameplay.windowEvent.set()

            quitted = self.gameplay.hasQuitted() or not self.gameplay.isAiOn()

        print("joined: <SnakeAI>")