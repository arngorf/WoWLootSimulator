import Objects
import random
import numpy as np
from copy import deepcopy

class SimLoot:
    def __init__(self, rosterSize, minNumberOfPlayers, maxNumberOfPlayers, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance):

        self.minNumberOfPlayers = minNumberOfPlayers
        self.maxNumberOfPlayers = maxNumberOfPlayers
        self.dropChance_ML = 0.20
        self.dropChance_PL = 0.27

        self.baseRoster = self._generateRoster(rosterSize, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance)

    def runRaids(self, numberOfRaids):

        roster_PL = deepcopy(self.roster)
        roster_ML = deepcopy(self.roster)

        for i in range(numberOfRaids):
            raidGroup_PL = self._pickRaidGroup(roster_PL)
            raidGroup_PL = self._pickRaidGroup(roster_PL)
            self._runRaid(raidGroup_PL)

        rosterItemLevelAverages = []

        return rosterItemLevelAverages

    def _runRaid(self, raidGroup, lootSystem):
        raid = Objects.Raid(10, [870, 870, 870, 875, 875, 875, 875, 875, 875, 880], len(raidGroup))

    def _pickRaidGroup(self, roster):
        raidSize = random.randint(self.minNumberOfPlayers, maxNumberOfPlayers)
        return np.random.permutation(roster)[:raidSize]

    def distributeMasterLoot(self):
        pass

    def distributePersonalLoot(self):
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
        rosterItems = map(lambda x: x.items, roster)
        rosterPerCharacterItemLevelSum = map(sum, rosterItems)
        rosterPerCharacterItemLevelAverage = map(lambda x: x/14., rosterPerCharacterItemLevelSum)
        return sum(rosterPerCharacterItemLevelAverage)/n


