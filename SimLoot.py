import Objects
import random
import numpy as np
from copy import deepcopy

class SimLootResult:
    def __init__(self, N):
        self.N = N
        self.itemLevelAverages = [0 for i in range(N)]
        self.looted = [0 for i in range(N)]
        self.wastedNoNeed = [0 for i in range(N)]
        self.wastedNotTradeable = [0 for i in range(N)]

    def normalize(self):
        self.itemLevelAverages = map(lambda x: x/float(N), self.itemLevelAverages)
        self.looted = map(lambda x: x/float(N), self.looted)
        self.wastedNoNeed = map(lambda x: x/float(N), self.wastedNoNeed)
        self.wastedNotTradeable = map(lambda x: x/float(N), self.wastedNotTradeable)

class SimLoot:
    def __init__(self, rosterSize, minNumberOfPlayers, maxNumberOfPlayers, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance):

        # Init constants
        self.minNumberOfPlayers = minNumberOfPlayers
        self.maxNumberOfPlayers = maxNumberOfPlayers
        self.dropChance_ML = 0.20
        self.dropChance_PL = 0.27

        # Generate a constant base roster
        self.baseRoster = self._generateRoster(rosterSize, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance)

    def runRaids(self, numberOfRaidWeeks, raidSchedule, numberOfSimulationRuns=1):

        results_ML = SimLootResult(numberOfRaidWeeks + 1)
        results_PL = SimLootResult(numberOfRaidWeeks + 1)

        for i in range(numberOfSimulationRuns):
            # Copy the constant base roster every time a new group of raids is run
            roster_ML = deepcopy(self.baseRoster)
            roster_PL = deepcopy(self.baseRoster)

            results_ML.itemLevelAverages[0] += self._averageItemLevel(self.baseRoster)
            results_PL.itemLevelAverages[0] += self._averageItemLevel(self.baseRoster)

            nightholdNormalRaid = Objects.Raid([870, 870, 870, 875, 875, 875, 875, 875, 875, 880])
            nightholdHeroicRaid = Objects.Raid([885, 885, 885, 890, 890, 890, 890, 890, 890, 895])

            nightholdNormalLootTables = nightholdNormalRaid.getLootTables()
            nightholdHeroicLootTables = nightholdHeroicRaid.getLootTables()

            raidSchedule = map(lambda x: x.lower(), raidSchedule)

            # Run the raids
            for j in range(numberOfRaidWeeks):
                raidGroup_ML, raidGroup_PL = self._pickRaidGroup(roster_ML, roster_PL)

                if 'nighthold normal' in raidSchedule:
                    looted_ML, wastedNoNeed_ML = self._distributeMasterLoot(raidGroup_ML, nightholdNormalLootTables)
                    looted_PL, wastedNoNeed_PL, wastedNotTradeable_PL = self._distributePersonalLoot(raidGroup_PL, nightholdNormalLootTables)
                    results_ML.looted[j+1] += looted_ML
                    results_ML.wastedNoNeed[j+1] += wastedNoNeed_ML
                    results_PL.looted[j+1] += looted_PL
                    results_PL.wastedNoNeed[j+1] += wastedNoNeed_PL
                    results_PL.wastedNotTradeable[j+1] += wastedNotTradeable_PL

                if 'nighthold heroic' in raidSchedule:
                    looted_ML, wastedNoNeed_ML = self._distributeMasterLoot(raidGroup_ML, nightholdHeroicLootTables)
                    looted_PL, wastedNoNeed_PL, wastedNotTradeable_PL = self._distributePersonalLoot(raidGroup_PL, nightholdHeroicLootTables)
                    results_ML.looted[j+1] += looted_ML
                    results_ML.wastedNoNeed[j+1] += wastedNoNeed_ML
                    results_PL.looted[j+1] += looted_PL
                    results_PL.wastedNoNeed[j+1] += wastedNoNeed_PL
                    results_PL.wastedNotTradeable[j+1] += wastedNotTradeable_PL

                results_PL.itemLevelAverages[j+1] += self._averageItemLevel(roster_PL)
                results_ML.itemLevelAverages[j+1] += self._averageItemLevel(roster_ML)

        results_ML.normalize()
        results_PL.normalize()

        return results_ML, results_PL

    def _pickRaidGroup(self, roster_PL, roster_ML):

        raidSize = random.randint(self.minNumberOfPlayers, self.maxNumberOfPlayers)
        indices = range(raidSize)
        indices = np.random.permutation(indices)[:raidSize]

        raidGroup_ML = []
        raidGroup_PL = []

        for i in indices:
            raidGroup_ML.append(roster_ML[i])
            raidGroup_PL.append(roster_PL[i])

        return raidGroup_PL, raidGroup_ML

    def _distributeMasterLoot(self, raidGroup, lootTables):

        raidSize = len(raidGroup)
        for lootTable in lootTables:

            totalDropChance = raidSize * self.dropChance_ML

            numberOfDroppedItems = int(totalDropChance)

            extraItemRoll = random.uniform(0,1)
            extraItemRollDropChance = totalDropChance % 1

            if extraItemRoll < extraItemRollDropChance:
                numberOfDroppedItems += 1

            # Pick dropped items randomly from the loot table
            droppedItems = np.random.permutation(lootTable)[:numberOfDroppedItems]

            for item in droppedItems:
                itemLevelUpgradeSizes = map(lambda x: x.upgradeSize(item), raidGroup)

                # Sort raiders from most to least needing
                needingRaiders = [x for (y,x) in sorted(zip(itemLevelUpgradeSizes, raidGroup), key=lambda pair: pair[0])][::-1]

                # Find the 5 most needed raiders
                needingRaiders = needingRaiders[:5]

                # Filter any raiders that don't need the item
                needingRaiders = filter(lambda x: x.needsItem(item), raidGroup)

                if len(needingRaiders) > 0:
                    luckyRaiderIndex = random.randint(0,len(needingRaiders) - 1)
                    needingRaiders[luckyRaiderIndex].equipItem(item)
                else:
                    # Wasted item
                    pass

    def _distributePersonalLoot(self, raidGroup, lootTables):
        raidSize = len(raidGroup)
        for lootTable in lootTables:

            totalDropChance = raidSize * self.dropChance_PL

            numberOfDroppedItems = int(totalDropChance)

            extraItemRoll = random.uniform(0,1)
            extraItemRollDropChance = totalDropChance % 1

            if extraItemRoll < extraItemRollDropChance:
                numberOfDroppedItems += 1

            # Pick lucky raiders to get item
            luckyRaiders = np.random.permutation(raidGroup)[:numberOfDroppedItems]

            for raider in luckyRaiders:

                elligibleLoot = filter(lambda x: raider.elligibleItem(x), lootTable)
                item = elligibleLoot[random.randint(0,len(elligibleLoot) - 1)]

                if raider.needsItem(item):
                    # Raider needs item
                    raider.equipItem(item)
                elif item.itemLevel <= raider.getItemLevelAtSlot(item.itemSlot):
                    # The item is tradable

                    # Filter any raiders that don't need the item
                    needingRaiders = filter(lambda x: x.needsItem(item), raidGroup)

                    if len(needingRaiders) > 0:
                        luckyRaiderIndex = random.randint(0,len(needingRaiders) - 1)
                        needingRaiders[luckyRaiderIndex].equipItem(item)
                    else:
                        # Wasted item - no one needs it
                        pass
                else:
                    # Wasted item - not tradeable
                    pass


    def _generateRoster(self, rosterSize, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance):

        roster = []

        for armorClass, armorClassCount in enumerate(rosterSize):

            for i in range(armorClassCount):

                parCharacterItemLevelAverage = random.gauss(itemLevelAverage, itemLevelVariance) / 5.
                parCharacterItemLevelAverage = int(round(parCharacterItemLevelAverage)) * 5
                character = Objects.Character(parCharacterItemLevelAverage, perCharacterItemLevelVariance, armorClass)
                roster.append(character)

        return roster

    def _averageItemLevel(self, roster):
        n = len(roster)
        perCharacterItemLevelAverages = map(lambda x: x.getAverageItemLevel(), roster)
        return sum(perCharacterItemLevelAverages) / float(n)


