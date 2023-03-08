from backbone_classes import *
from events.events import *
from events.law_events import *
from events.love_events import *
from events.health_events import *
import random

from run import getRunableEvents


def selectEventIndex(eventList, desiredWorldState):
    if len(eventList) == 0: # TODO: Handle this before calling it, rather than after.
        print("No events left in this tree!")
        return 0, float('inf')

    currEventMinDistance = float('inf')
    equallyValubleIndexes = []
    for x in range (len(eventList)):
        reachable_worldstate = eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3])
        currEventValue = distanceBetweenWorldstates(reachable_worldstate, desiredWorldState)

        if (currEventValue < currEventMinDistance):
            equallyValubleIndexes = []
            currEventMinDistance = currEventValue
        if (currEventValue == currEventMinDistance):
            equallyValubleIndexes.append(x)


    if len(equallyValubleIndexes) >= 1:
        return random.choice(equallyValubleIndexes), currEventMinDistance # Return the index of the event with the lowest distance to the desiredWorldState
    else:
        return 0, float('inf')

def getBestIndexLookingAhead(depth, eventList, desiredWorldState, possible_events):
    if depth == 1:
        return selectEventIndex(eventList, desiredWorldState)

    if depth >= 2:
        currEventMinDistance = float('inf')
        equallyValubleIndexes = []

        for x in range (len(eventList)):
            reachable_worldstate = eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3])
            runable_events = getRunableEvents(reachable_worldstate, possible_events)
            currWorldStateValue = getBestIndexLookingAhead(depth-1, runable_events, desiredWorldState, possible_events)

            if (currWorldStateValue[1] < currEventMinDistance):
                equallyValubleIndexes = []
                currEventMinDistance = currWorldStateValue[1]
                equallyValubleIndexes.append(x)

            if (currWorldStateValue[1] == currEventMinDistance):
                equallyValubleIndexes.append(x)

        return random.choice(equallyValubleIndexes), currEventMinDistance



def distanceBetweenWorldstates(currWorldState, newWorldState):
    distance = 0
    drama_weight = 2
    if currWorldState.characters:
        for character in currWorldState.characters:
            for future_character in newWorldState.characters:
                if future_character.name == character.name:
                    distanceBetweenVersions = character.getDistanceToFutureState(future_character.getAttributes())
                    distance += distanceBetweenVersions

    if len(currWorldState.characters) != len(newWorldState.characters):
        deadCharacterPenalty = abs(len(currWorldState.characters)-len(newWorldState.characters)) * 50 # Change this value to change weight of undesired deaths.
        distance += deadCharacterPenalty

    # Drama scores using drama curve methodology
    if newWorldState.getDramaCurve() != None:
        #print("DramaCurveTargetFound")
        plotSteps = len(currWorldState.event_history)
        #print(plotSteps)
        dramaTarget = newWorldState.getDramaCurve().getDramaTargets()[plotSteps]
        drama_distance = abs(currWorldState.drama_score - dramaTarget) * drama_weight
        distance += drama_distance
        #print(drama_distance)
        return distance

    # Drama scoring using arbitrary assigned target for a waypoint
    if newWorldState.drama_score != None:
        #drama_distance = abs(currWorldState.drama_score - newWorldState.drama_score) * 5/2
        drama_distance = abs(currWorldState.drama_score - newWorldState.drama_score) * drama_weight
        distance += drama_distance
        #print(drama_distance)
    return distance
