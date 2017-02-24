import SimLoot
import matplotlib.pyplot as plt

class Tests:

    def __init__(self, numberOfSimulationRuns, numberOfRaidWeeks):
        self.numberOfSimulationRuns = numberOfSimulationRuns
        self.numberOfRaidWeeks = numberOfRaidWeeks

    def plotResults(self, ML, PL, title):

        plt.subplot(2,1,1)
        plt.title(title + ' - Average item level')
        #plt.plot(range(ML.N), ML.getItemLevelAverages(True), color='blue', label = 'Average ilvl ML')
        plt.errorbar(range(ML.N), ML.getItemLevelAverages(True), yerr=ML.itemLevelAverageError, color='blue', alpha=0.8, label = 'Average ilvl ML')
        plt.errorbar(range(PL.N), PL.getItemLevelAverages(True), yerr=PL.itemLevelAverageError, color='orange', alpha=0.8, label = 'Average ilvl PL')
        plt.xlim(-1, ML.N + 1)
        plt.xlabel('Completed raid weeks')
        plt.ylabel('Average item level')
        plt.legend()

        plt.subplot(2,1,2)
        plt.title(title + ' - Looted items')
        plt.plot(range(1, ML.N), ML.getLooted(True)[1:], color='blue', label = 'Used ML')
        plt.plot(range(1, ML.N), ML.getWastedNoNeed(True)[1:], color='blue', label = 'Disenchanted ML', ls='--')
        plt.plot(range(1, PL.N), PL.getLooted(True)[1:], color='orange', label = 'Used PL')
        plt.plot(range(1, PL.N), PL.getWastedNoNeed(True)[1:], color='orange', label = 'Disenchanted PL', ls='--')
        plt.plot(range(1, PL.N), PL.getWastedNotTradeable(True)[1:], color='orange', label = 'Untradeable PL', ls='-.')
        plt.xlim(-1, ML.N + 1)
        plt.xlabel('Completed raid weeks')
        plt.ylabel('Number of items')
        plt.legend()

        plt.show()

        plt.subplot(2,1,1)
        plt.title(title + ' - boss kills since last loot (ML)')
        n, bins, patches = plt.hist(ML.timeBetweenLoots, 50, normed=1, facecolor='blue', alpha=0.75)
        plt.xlabel('Boss kills since last item equipped')
        plt.ylabel('Probability')
        #plt.axis([40, 160, 0, 0.03])
        plt.grid(True)

        plt.subplot(2,1,2)
        plt.title(title + ' - boss kills since last loot (PL)')
        n, bins, patches = plt.hist(PL.timeBetweenLoots, 50, normed=1, facecolor='green', alpha=0.75)
        plt.xlabel('Boss kills since last item equipped')
        plt.ylabel('Probability')
        #plt.axis([40, 160, 0, 0.03])
        plt.grid(True)

        plt.show()

    def Test_Realistic(self):

        # Parameter initialization

        rosterSize = [6,7,8,15]
        minNumberOfPlayers = 16
        maxNumberOfPlayers = 30
        itemLevelAverage = 875
        raidSchedule = ['Nighthold Heroic']

        # Create simulator and run simulation

        sl = SimLoot.SimLoot(rosterSize, minNumberOfPlayers, maxNumberOfPlayers)
        ML, PL = sl.runRaids(self.numberOfRaidWeeks, raidSchedule, self.numberOfSimulationRuns)

        # Plot results

        self.plotResults(ML, PL, 'Realistic')

    def Test_Realistic_BalancedRoster(self):

        # Parameter initialization

        rosterSize = [9,9,9,9]

        minNumberOfPlayers = 16
        maxNumberOfPlayers = 30
        itemLevelAverage = 875
        raidSchedule = ['Nighthold Heroic']

        # Create simulator and run simulation

        sl = SimLoot.SimLoot(rosterSize, minNumberOfPlayers, maxNumberOfPlayers)
        ML, PL = sl.runRaids(self.numberOfRaidWeeks, raidSchedule, self.numberOfSimulationRuns)

        # Plot results

        self.plotResults(ML, PL, 'Realistic Balanced Roster')

    def Test_PerfectLootCouncil_BalancedRoster(self):

        # Parameter initialization

        rosterSize = [5,5,5,5]

        minNumberOfPlayers = 20
        maxNumberOfPlayers = 20
        itemLevelAverage = 875
        raidSchedule = ['Nighthold Heroic']

        # Create simulator and run simulation

        sl = SimLoot.SimLoot(rosterSize, minNumberOfPlayers, maxNumberOfPlayers, numberConsideredNeedingRaiders = 1)
        ML, PL = sl.runRaids(self.numberOfRaidWeeks, raidSchedule, self.numberOfSimulationRuns)

        # Plot results

        self.plotResults(ML, PL, 'Perfect Loot Council')

    def Test_NoPersonalLootItemTrading(self):

        # Parameter initialization

        rosterSize = [9,9,9,9]

        minNumberOfPlayers = 16
        maxNumberOfPlayers = 30
        itemLevelAverage = 875
        raidSchedule = ['Nighthold Heroic']

        # Create simulator and run simulation

        sl = SimLoot.SimLoot(rosterSize, minNumberOfPlayers, maxNumberOfPlayers, itemTradingChance=0.0)
        ML, PL = sl.runRaids(self.numberOfRaidWeeks, raidSchedule, self.numberOfSimulationRuns)

        # Plot results

        self.plotResults(ML, PL, 'No item trading')