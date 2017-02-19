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
                self.items.append(itemLevel)

class Item:
    def __init__(self, itemLevelBase, armorClass, canBeWarforged=True):
        # Warforged/titanforged not implemented
        self.itemLevel = itemLevelBase
        self.armorClass = armorClass

class Raid:
    def __init__(self, numberOfBosses, itemLevelProgression, raidGroup):

        self.numberOfBosses = numberOfBosses
        self.itemLevelProgression = itemLevelProgression
        self.numberOfPlayers = len(raidGroup)
        self.raidGroup = raidGroup

    def getLootTable(self):

        lootTables = []

        lootArmorClassScheme = [[6,3,3,4], \
                                [4,6,3,3], \
                                [3,4,6,3], \
                                [3,3,4,6]]

        lastLootSchemeIndex = self.numberOfBosses / len(lootArmorClassScheme) * 4

        for bossIndex, baseItemLevel in enumerate(itemLevelProgression):

            lootTables.append([])
            lootScheme = [4,4,4,4]

            if bossIndex < lastLootSchemeIndex:
                lootScheme = lootArmorClassScheme[bossIndex]

            for armorClass, armorClassCount in enumerate(lootScheme):
                for i in range(armorClassCount):
                    lootTables[-1].append(Objects.Item(baseItemLevel, armorClass))

        return lootTables