import random

class Character:
    def __init__(self, itemLevelAverage, itemLevelVariance):

        self.items = []

        for i in range(14):

            if itemLevelVariance == 0:
                self.items.append(itemLevelAverage)

            else:
                itemLevel = random.gauss(itemLevelAverage, itemLevelVariance) / 5.
                itemLevel = int(round(itemLevel)) * 5
                self.items.append(itemLevel)

