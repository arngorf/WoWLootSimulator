import SimLoot
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print "WoWLootSimulator::Begin"

    rosterSize = [9,9,9,9]
    #rosterSize = [6,7,8,15]
    minNumberOfPlayers = 20
    maxNumberOfPlayers = 30
    numberOfRaidWeeks = 25
    numberOfSimulationRuns = 5
    itemLevelAverage = 870
    itemLevelVariance = 10
    perCharacterItemLevelVariance = 10

    sl = SimLoot.SimLoot(rosterSize, minNumberOfPlayers, maxNumberOfPlayers, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance)

    raidSchedule = ['Nighthold Normal', 'Nighthold Heroic']

    ML, PL = sl.runRaids(numberOfRaidWeeks, raidSchedule, numberOfSimulationRuns)

    plt.subplot(2,1,1)
    plt.plot(range(0, ML.N), ML.itemLevelAverages, color='blue', label = 'Master loot')
    plt.plot(range(0, PL.N), PL.itemLevelAverages, color='orange', label = 'Personal loot')
    plt.legend()
    plt.show()

    print "WoWLootSimulator::End"