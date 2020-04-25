# !/usr/bin/python
import threading

from Window import Window
from Gameplay import Gameplay
from SnakeAI import SnakeAI


gameplay = Gameplay(840, 560)

window = Window(gameplay)

window.setTickValue(0.08)

threads = []

for obj in [window]:
    threads.append(threading.Thread(target=obj.run))
    threads[-1].start()
    threads[-1].setName(obj.__str__())


for thread in threads:
    thread.join()
    print("joined: {}".format(thread.getName()))

print("completed")