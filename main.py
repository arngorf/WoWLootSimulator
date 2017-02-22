import SimLoot
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print "WoWLootSimulator::Begin"

    # Parameter initialization

    rosterSize = [9,9,9,9]
    #rosterSize = [6,7,8,15]
    minNumberOfPlayers = 16
    maxNumberOfPlayers = 30
    numberOfRaidWeeks = 100
    numberOfSimulationRuns = 150
    itemLevelAverage = 875
    itemLevelVariance = 0
    perCharacterItemLevelVariance = 1
    raidSchedule = ['Nighthold Heroic']

    # Create simulator and run simulation

    sl = SimLoot.SimLoot(rosterSize, minNumberOfPlayers, maxNumberOfPlayers, itemLevelAverage, itemLevelVariance, perCharacterItemLevelVariance)
    ML, PL = sl.runRaids(numberOfRaidWeeks, raidSchedule, numberOfSimulationRuns)

    # Plot results

    plt.subplot(2,1,1)
    plt.plot(range(ML.N), ML.itemLevelAverages, color='blue', label = 'Average ilvl ML')
    plt.plot(range(PL.N), PL.itemLevelAverages, color='orange', label = 'Average ilvl PL')
    plt.xlim(-1, ML.N + 1)
    plt.xlabel('Completed raid weeks')
    plt.ylabel('Average item level')
    plt.legend()

    plt.subplot(2,1,2)
    plt.plot(range(1, ML.N), ML.looted[1:], color='blue', label = 'Used ML')
    plt.plot(range(1, ML.N), ML.wastedNoNeed[1:], color='blue', label = 'Disenchanted ML', ls='--')
    plt.plot(range(1, PL.N), PL.looted[1:], color='orange', label = 'Used PL')
    plt.plot(range(1, PL.N), PL.wastedNoNeed[1:], color='orange', label = 'Disenchanted PL', ls='--')
    plt.plot(range(1, PL.N), PL.wastedNotTradeable[1:], color='orange', label = 'Untradeable PL', ls='-.')
    plt.xlim(-1, ML.N + 1)
    plt.xlabel('Completed raid weeks')
    plt.ylabel('Number of items')
    plt.legend()
    plt.show()

    print "WoWLootSimulator::End"