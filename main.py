import Tests

if __name__ == '__main__':
    print "WoWLootSimulator::Begin"

    numberOfFreshGearingRuns = 10000
    numberOfRaidWeeks = 40
    lootSimulationTest = Tests.Tests(numberOfFreshGearingRuns, numberOfRaidWeeks)

    #lootSimulationTest.Test_Realistic()
    lootSimulationTest.Test_Realistic_BalancedRoster()
    #lootSimulationTest.Test_PerfectLootCouncil_BalancedRoster()
    #lootSimulationTest.Test_NoPersonalLootItemTrading()

    print "WoWLootSimulator::End"