import random

class Character:
    def __init__(self, itemLevelAverage, itemLevelVariance, armorClass):

        self.items = []
        self.armorClass = armorClass

        for i in range(14):

            if itemLevelVariance == 0:
                self.items.append(itemLevelAverage)

            else:
                itemLevel = random.gauss(itemLevelAverage, itemLevelVariance) / 5.
                itemLevel = int(round(itemLevel)) * 5
                self.items.append(Item(itemLevel, i, self.armorClass, False))

    def elligibleItem(self, item):

        return item.armorClass == self.armorClass

    def needsItem(self, item):

        itemSlot = item.itemSlot

        return self.elligibleItem(item) and item > self.items[itemSlot]

    def upgradeSize(self, item):

        itemSlot = item.itemSlot

        if item.armorClass != self.armorClass:
            return 0
        else:
            return max(item.itemLevel - self.items[itemSlot].itemLevel, 0)

    def getAverageItemLevel(self):
        itemLevels = map(lambda x: x.itemLevel, self.items)
        return sum(itemLevels) / float(len(itemLevels))

    def getItemLevelAtSlot(self, itemSlot):
        return self.items[itemSlot].itemLevel

    def equipItem(self, item):

        itemSlot = item.itemSlot

        self.items[itemSlot] = item

class Item:
    def __init__(self, itemLevelBase, itemSlot, armorClass, canBeWarforged=True):

        # Warforged/titanforged not implemented
        # Statistical work in progress

        self.itemLevel = itemLevelBase
        self.itemSlot = itemSlot
        self.armorClass = armorClass

    def __eq__(self, other):
        return self.itemLevel == other.itemLevel

    def __gt__(self, other):
        return self.itemLevel > other.itemLevel

    def __lt__(self, other):
        return self.itemLevel < other.itemLevel

class Raid:
    def __init__(self, itemLevelProgression):

        self.numberOfBosses = len(itemLevelProgression)
        self.itemLevelProgression = itemLevelProgression

    def getLootTables(self):

        lootTables = []

        lootArmorClassScheme = [[6,3,3,4], \
                                [4,6,3,3], \
                                [3,4,6,3], \
                                [3,3,4,6]]

        armorClassSlots = [0,0,0,0]

        lastLootSchemeIndex = self.numberOfBosses / len(lootArmorClassScheme) * 4

        for bossIndex, baseItemLevel in enumerate(self.itemLevelProgression):

            lootTables.append([])
            lootScheme = [4,4,4,4]

            if bossIndex < lastLootSchemeIndex:
                lootScheme = lootArmorClassScheme[bossIndex % len(lootArmorClassScheme)]

            for armorClass, armorClassCount in enumerate(lootScheme):
                for i in range(armorClassCount):
                    lootTables[-1].append(Item(baseItemLevel, armorClassSlots[armorClass], armorClass))
                    armorClassSlots[armorClass] = (armorClassSlots[armorClass] + 1) % 14

        return lootTables