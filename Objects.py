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

        self.statWeights = []
        for i in range(4):
            self.statWeights.append(random.uniform(0.5, 1.05))

    def elligibleItem(self, item):

        return item.armorClass == self.armorClass

    def needsItem(self, item):

        itemSlot = item.itemSlot

        return self.elligibleItem(item) and (self.upgradeSize(item) > 0)

    def upgradeSize(self, item):

        itemSlot = item.itemSlot

        if item.armorClass != self.armorClass:
            return 0
        else:
            newItemWeight = self.calculateStatWeight(item)
            ownItemWeight = self.calculateStatWeight(self.items[itemSlot])
            return max(newItemWeight - ownItemWeight, 0)

    def getAverageItemLevel(self):
        itemLevels = map(lambda x: x.itemLevel, self.items)
        return sum(itemLevels) / float(len(itemLevels))

    def getItemLevelAtSlot(self, itemSlot):
        return self.items[itemSlot].itemLevel

    def equipItem(self, item):

        itemSlot = item.itemSlot

        self.items[itemSlot] = item

    def calculateStatWeight(self, item):
        return item.baseStat + sum([x*y for (x,y) in zip(item.secondaryStats, self.statWeights)])

class Item:

    def __init__(self, itemLevelBase, itemSlot, armorClass, canBeWarforged=True):

        # Warforged/titanforged not implemented
        # Statistical work in progress

        self.itemSlot = itemSlot
        self.armorClass = armorClass

        wfChances = [45,18,3,3,2,2,1,1,1,1,1,1]
        wfChances = map(lambda x: float(x)/sum(wfChances), wfChances)

        self.itemLevel = itemLevelBase

        if canBeWarforged:

            roll = random.uniform(0,1)

            for wfChance in wfChances:
                if roll < wfChance:
                    break
                self.itemLevel += 5
                roll -= wfChance

        self.baseStat = round(15.5 * self.itemLevel - 11800)
        self.secondaryStats = [0, 0, 0, 0]

        totalSecondaryStat = round(5.5 * self.itemLevel - 3350)

        secondaryIndices = random.sample(range(4), 2)
        statSplit = random.uniform(0.3, 0.7)

        self.secondaryStats[secondaryIndices[0]] += round(statSplit * totalSecondaryStat)
        self.secondaryStats[secondaryIndices[1]] += round((1. - statSplit) * totalSecondaryStat)

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