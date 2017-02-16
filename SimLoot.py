import Objects
import random

class SimLoot:
    def __init__(self, rosterSize, minNumberOfPlayers, maxNumberOfPlayers, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance):

        self.minNumberOfPlayers = minNumberOfPlayers
        self.maxNumberOfPlayers = maxNumberOfPlayers

        self.roster = self._generateRoster(rosterSize, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance)

    def runRaids(self, numberOfRaids):

        raidGroup = self._pickRaidGroup()

        for i in range(numberOfRaids):
            self._runRaid(raidGroup)

    def _runRaid(self, raidGroup):
        pass

    def _pickRaidGroup(self):
        pass

    def _generateRoster(self, rosterSize, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance):

        roster = []

        for j, armorType in enumerate(rosterSize):

            for i in range(rosterSize[j]):

                parCharacterItemLevelAverage = random.gauss(itemLevelAverage, itemLevelVariance) / 5.
                parCharacterItemLevelAverage = int(round(parCharacterItemLevelAverage)) * 5
                character = Objects.Character(parCharacterItemLevelAverage, perCharacterItemLevelVariance)
                roster.append(character)


