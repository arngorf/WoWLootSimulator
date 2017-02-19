import SimLoot

if __name__ == '__main__':
    print "WoWLootSimulator::Begin"

    rosterSize = [9,9,9,9]
    minNumberOfPlayers = 20
    maxNumberOfPlayers = 30
    numberOfRaids = 1
    itemLevelAverage = 870
    itemLevelVariance = 10
    perCharacterItemLevelVariance = 10
    sl = SimLoot.SimLoot(rosterSize, minNumberOfPlayers, maxNumberOfPlayers, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance)
    sl.runRaids(numberOfRaids)

    for i, char in enumerate(sl.roster):
        print i, char.armorClass, char.items

    print sl._averageItemLevel(sl.roster)

    print "WoWLootSimulator::End"