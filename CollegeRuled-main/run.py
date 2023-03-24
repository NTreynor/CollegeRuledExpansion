from backbone_classes import *
from events.events import *
from events.law_events import *
from events.love_events import *
from events.health_events import *
from path_finding import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def getRunableEvents(current_worldstate, possible_events):
    runableEvents = []
    for event in possible_events: # Check to see if an instance of an event is runnable
        preconditions_met, characters, environments = event.checkPreconditions(current_worldstate)
        if preconditions_met: # If so, add all possible instances to the list of runnable events
            for x in range(len(characters)):
                runableEvents.append([event, current_worldstate, characters[x], environments[x]])
    return runableEvents


def runStory(current_worldstate, possible_events, depth_limit, waypoints = None, lookaheadDepth=2, drama_weight=3, dramaVals = None):
    if dramaVals is None:
        currDramaVals = []
        targetDramaVals = []
        deltaDramaVals = []
        dramaVals = [currDramaVals, targetDramaVals, deltaDramaVals]

    if (depth_limit == 0):
        return current_worldstate
    
    runable_events = getRunableEvents(current_worldstate, possible_events)
    if len(runable_events) == 0:
        print("THE END")
        return current_worldstate

    # Setup to get story to pathfind to the first waypoint.
    if (waypoints != None) & (len(waypoints) != 0):
        desired_world_state = waypoints[0]
    else:
        print("No waypoint")
        desired_world_state = copy.deepcopy(current_worldstate) # TODO: Replace this with an actual goal worldstate

    depthToSearch = min(depth_limit, lookaheadDepth)
    print("depthOfSearch: ")
    print(depthToSearch)
    indexValuePair = getBestIndexLookingAhead(depthToSearch, runable_events, desired_world_state, possible_events) #First parameter indicates search depth. Do not exceed 6.
    idx_of_event_to_run = indexValuePair[0]

    event = runable_events[idx_of_event_to_run][0]
    worldstate_to_run = runable_events[idx_of_event_to_run][1]
    chars_to_use = runable_events[idx_of_event_to_run][2]
    environments_to_use = runable_events[idx_of_event_to_run][3]
    next_worldstate = event.doEvent(worldstate_to_run, chars_to_use, environments_to_use)

    # Here we are outputting our current drama-score, our desired drama score at the next waypoint or at this point
    # along the drama curve, and the difference
    print("Dramatic score: ")
    print(next_worldstate.drama_score)
    dramaVals[0].append(next_worldstate.drama_score)
    if next_worldstate.getDramaCurve() != None:
        print("Target dramatic score: ")
        dramaTarget = next_worldstate.getDramaCurve().getDramaTargets()[len(next_worldstate.event_history)]
        print(dramaTarget)
        dramaVals[1].append(dramaTarget)
        print("Delta Drama: ")
        print(next_worldstate.drama_score - dramaTarget)
        dramaVals[2].append(next_worldstate.drama_score - dramaTarget)
    else:
        print("Target dramatic score: ")
        dramaTarget = desired_world_state.drama_score
        print(dramaTarget)
        print("Delta Drama: ")
        dramaVals[1].append(dramaTarget)
        print(next_worldstate.drama_score - dramaTarget)
        dramaVals[2].append(next_worldstate.drama_score - dramaTarget)



    if desired_world_state.radius == None:
        desired_world_state.radius = 0
    if (distanceBetweenWorldstates(next_worldstate, desired_world_state) < desired_world_state.radius):
        print(". . .")
        print("(Waypoint hit)")
        print(". . .")
        waypoints.pop(0)

    if depth_limit == 1:
        print(". . .")
        print("(Story terminating, hit depth limit)")
        print(". . .")
        print("Distance to final waypoint: ")
        print(distanceBetweenWorldstates(next_worldstate, desired_world_state))

        print(dramaVals)
        lenOfGraph = len(dramaVals[1])
        xVals = np.arange(start=0, stop=lenOfGraph)
        """
        plt.title("Drama Vals")
        plt.plot(xVals, dramaVals[0], color="red")
        plt.plot(xVals, dramaVals[1], color="blue")
        plt.plot(xVals, dramaVals[2], color="green")
        plt.show()
        """
        return dramaVals

    return runStory(next_worldstate, possible_events, depth_limit - 1, waypoints, lookaheadDepth, dramaVals=dramaVals)

def waypointTestEnvironment():
    # Environment Initialization
    wp_serenity = Environment("Serenity", 25, False, True)
    wp_space = Environment("Space", -100, True, False)
    wp_serenity.setDistance(wp_space, 0)
    wp_space.setDistance(wp_serenity, 0)

    # Character & Relationship Initialization
    wp_jess = Character("Jess", health=6, happiness=8, location=wp_serenity, romantic_partner=False)
    wp_mal = Character("Mal", health=6, happiness=7, location=wp_serenity, romantic_partner=False)
    wp_inara = Character("Inara", health=7, happiness=5, location=wp_serenity, romantic_partner=False, murderer=False)

    wp_jess.updateRelationship(wp_mal, 45)
    wp_jess.updateRelationship(wp_inara, 0)
    wp_mal.updateRelationship(wp_jess, 45)
    wp_mal.updateRelationship(wp_inara, 35)
    wp_inara.updateRelationship(wp_jess, -5)
    wp_inara.updateRelationship(wp_mal, 35)

    wp_environments = [wp_serenity, wp_space]
    wp_chars = [wp_jess, wp_mal, wp_inara]
    wp_curr_worldstate = WorldState(0, wp_chars, wp_environments)

    wp_init_worldstate = copy.deepcopy(wp_curr_worldstate) # Save FIRST worldstate

    # Update characters for second waypoint

    wp_jess.health = None
    wp_mal.health = None
    wp_inara.health = None
    wp_jess.happiness = None
    wp_mal.happiness = None
    wp_inara.happiness = None
    wp_jess.updateRelationship(wp_mal, 30)
    wp_mal.updateRelationship(wp_jess, 40)
    wp_jess.romantic_partner = wp_mal
    wp_mal.romantic_partner = wp_jess
    wp_chars = [wp_jess, wp_mal, wp_inara]

    wp_curr_worldstate = WorldState(0, wp_chars, wp_environments, 10)
    wp_2_worldstate = copy.deepcopy(wp_curr_worldstate) # Save second waypoint
    wp_2_worldstate.drama_score = 15

    #wp_jess = Character("Jess", health=None, happiness=None, location=wp_serenity, romantic_partner=None)
    wp_mal.updateRelationship(wp_jess, -30)
    wp_inara.relationships.pop(wp_jess)
    wp_mal.updateRelationship(wp_inara, 30)
    wp_inara.updateRelationship(wp_mal, 45)
    wp_mal.romantic_partner = wp_inara
    wp_inara.romantic_partner = wp_mal
    wp_inara.fugitive = True
    wp_inara.murderer = True
    wp_mal.has_job = True
    wp_chars = [wp_mal, wp_inara]


    wp_curr_worldstate = WorldState(0, wp_chars, wp_environments, 40)
    wp_3_worldstate = copy.deepcopy(wp_curr_worldstate) # Save third waypoint
    wp_3_worldstate.drama_score = 100

    waypoints = [wp_2_worldstate, wp_3_worldstate]
    starting_point = wp_init_worldstate

    return [starting_point, waypoints]


def waypointTestEnvironmentAlt():

    # Drama curve Initialization
    params = [[2.6, 6], [2, 13]]
    testCurve = DramaCurve(2, params, 16, 100)


    # Environment Initialization
    wp_serenity = Environment("Serenity", 25, False, True)
    wp_space = Environment("Space", -100, True, False)
    wp_serenity.setDistance(wp_space, 0)
    wp_space.setDistance(wp_serenity, 0)

    # Character & Relationship Initialization
    wp_jess = Character("Jess", health=7, happiness=8, location=wp_serenity, romantic_partner=False, murderer=False, fugitive=False, in_jail=False, stole=False, has_job=False, exploited=False)
    wp_mal = Character("Mal", health=7, happiness=5, location=wp_serenity, romantic_partner=False, murderer=False, fugitive=False, in_jail=False, stole=False, has_job=False, exploited=False)
    wp_inara = Character("Inara", health=5, happiness=5, location=wp_serenity, romantic_partner=False, murderer=False, fugitive=False, in_jail=False, stole=False, has_job=False, exploited=False)

    wp_environments = [wp_serenity, wp_space]
    wp_chars = [wp_jess, wp_mal, wp_inara]
    wp_curr_worldstate = WorldState(0, wp_chars, wp_environments, None, testCurve)

    wp_init_worldstate = copy.deepcopy(wp_curr_worldstate) # Save FIRST worldstate

    # Update characters for second waypoint

    wp_jess2 = Character("Jess", health=None, happiness=None, romantic_partner=None, murderer=None, fugitive=None, in_jail=None, stole=None, has_job=None, exploited=None)
    wp_mal2 = Character("Mal", health=None, happiness=None, romantic_partner=None, murderer=None, fugitive=None, in_jail=None, stole=None, has_job=None, exploited=None)
    wp_jess2.murderer = True
    wp_mal2.stole = True
    wp_jess2.updateRelationship(wp_mal2, 40)
    wp_mal2.updateRelationship(wp_jess2, 40)
    wp_mal2.romantic_partner = wp_jess2
    wp_jess2.romantic_partner = wp_mal2

    wp_chars2 = [wp_jess2, wp_mal2]

    wp_curr_worldstate2 = WorldState(0, wp_chars2, wp_environments, 10, testCurve)
    wp_2_worldstate = copy.deepcopy(wp_curr_worldstate2) # Save second waypoint
    wp_2_worldstate.drama_score = 100


    waypoints = [wp_2_worldstate]
    starting_point = wp_init_worldstate

    return [starting_point, waypoints]

if __name__ == "__main__":

    """
    __init__(self, numDistributions, parameters, range):
    params = [[1.8, 9], [1, 15]]
    testCurve = DramaCurve(2, params, 20, 200)
    dramaTargets = testCurve.getDramaTargets()
    print(dramaTargets)
    """

    possibleEvents = [FallInLove(), AskOnDate(),  HitBySpaceCar(), GetMiningJob(),
                        GetSpaceShuttleJob(), GoToSpaceJail(), SoloJailbreak(), CoffeeSpill(),
                        HospitalVisit(), Cheat(), Steal(), Irritate(), Befriend(), LoseJob(),
                        AssistedJailBreak(), SabotagedJailBreak(), DoNothing(), MoneyProblems(), GetRejectedFromJob()]

    """
    "# First demo story
    initWorldState, waypoints = waypointTestEnvironment()
    runStory(initWorldState, possibleEvents, 15, waypoints, lookaheadDepth=2)
    """

    print("")
    print("Second Story:")
    print("")

    # Second demo story
    # Using drama curve system
    """
    initWorldState, waypoints = waypointTestEnvironmentAlt()
    runStory(initWorldState, possibleEvents, 15, waypoints, lookaheadDepth=2)
    """

    numStories = 10
    dramaValList = []
    for z in range(numStories):
        initWorldState, waypoints = waypointTestEnvironmentAlt()
        dramaValuesInstance = runStory(initWorldState, possibleEvents, 15, waypoints, lookaheadDepth=3)
        dramaValList.append(dramaValuesInstance)

    dramaVals = dramaValList[0]
    lenOfGraph = len(dramaVals[1])

    currDramaMean = [0] * lenOfGraph
    currDramaMin = [9999] * lenOfGraph
    currDramaMax = [0] * lenOfGraph
    for x in range(numStories):
        for y in range(lenOfGraph):
            currDramaMean[y] += dramaValList[x][0][y]
            if currDramaMax[y] < dramaValList[x][0][y]:
                currDramaMax[y] = dramaValList[x][0][y]
            if currDramaMin[y] > dramaValList[x][0][y]:
                currDramaMin[y] = dramaValList[x][0][y]

    for index in range(lenOfGraph):
        currDramaMean[index] = currDramaMean[index] / numStories # adjust mean appropriately

    # Now generating data for box and whisker plot
    currDramaData = [[0 for i in range(numStories)] for j in range(lenOfGraph)]
    for x in range(numStories):
        for y in range(lenOfGraph):
            currDramaData[y][x] = dramaValList[x][0][y]

    fig = plt.figure(figsize=(12, 10))

    # Creating axes instance
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    # Creating plot
    bp = ax.boxplot(currDramaData, notch=False, vert=True, patch_artist=True)

    ax.yaxis.grid(True)

    colors = ['red']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    xVals = np.arange(start=1, stop=lenOfGraph+1)
    plt.plot(xVals, dramaVals[1], color="red", label='Target Drama Curve') #Target

    ax.set_xlabel('Plot Fragment Index')
    ax.set_ylabel('Drama Level')

    legend_elements = [Line2D([0], [0], color='red', lw=4, label='Target Drama Values'),
                       Patch(facecolor=sns.desaturate('blue', .5), edgecolor='grey', linewidth=1.5,
                             label='Produced Drama Values')]
    ax.legend(handles=legend_elements, fontsize='xx-large')

    # show plot
    plt.show()


    xVals = np.arange(start=0, stop=lenOfGraph)
    plt.title("Drama Vals")
    plt.plot(xVals, currDramaMean, color="red") #current
    plt.plot(xVals, currDramaMax, color="blue") #upper bound
    plt.plot(xVals, currDramaMin, color="blue") #Lower bound
    plt.plot(xVals, dramaVals[1], color="green") #Target
    plt.show()








