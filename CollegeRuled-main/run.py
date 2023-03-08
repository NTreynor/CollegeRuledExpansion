from backbone_classes import *
from events.events import *
from events.law_events import *
from events.love_events import *
from events.health_events import *
from path_finding import *

def getRunableEvents(current_worldstate, possible_events):
    runableEvents = []
    for event in possible_events: # Check to see if an instance of an event is runnable
        preconditions_met, characters, environments = event.checkPreconditions(current_worldstate)
        if preconditions_met: # If so, add all possible instances to the list of runnable events
            for x in range(len(characters)):
                runableEvents.append([event, current_worldstate, characters[x], environments[x]])
    return runableEvents


def runStory(current_worldstate, possible_events, depth_limit, waypoints = None, lookaheadDepth=2):
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
    indexValuePair = getBestIndexLookingAhead(depthToSearch, runable_events, desired_world_state, possible_events) #First parameter indicates search depth. Do not exceed 6.
    idx_of_event_to_run = indexValuePair[0]

    event = runable_events[idx_of_event_to_run][0]
    worldstate_to_run = runable_events[idx_of_event_to_run][1]
    chars_to_use = runable_events[idx_of_event_to_run][2]
    environments_to_use = runable_events[idx_of_event_to_run][3]
    next_worldstate = event.doEvent(worldstate_to_run, chars_to_use, environments_to_use)
    print("Dramatic score: ")
    print(next_worldstate.drama_score)
    if next_worldstate.getDramaCurve() != None:
        print("Target dramatic score: ")
        dramaTarget = next_worldstate.getDramaCurve().getDramaTargets()[len(next_worldstate.event_history)]
        print(dramaTarget)


    if desired_world_state.radius == None:
        desired_world_state.radius = 0
    if (distanceBetweenWorldstates(next_worldstate, desired_world_state) < desired_world_state.radius):
        print(". . .")
        waypoints.pop(0)

    if depth_limit == 1:
        print(distanceBetweenWorldstates(next_worldstate, desired_world_state))
    return runStory(next_worldstate, possible_events, depth_limit - 1, waypoints)

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
    params = [[1.8, 9], [1, 15]]
    testCurve = DramaCurve(2, params, 20, 200)


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
                        AssistedJailBreak(), SabotagedJailBreak(), DoNothing()]

    # First demo story
    initWorldState, waypoints = waypointTestEnvironment()
    runStory(initWorldState, possibleEvents, 15, waypoints, lookaheadDepth=3)

    print("")
    print("Second Story:")
    print("")

    # Second demo story
    # Using drama curve system
    initWorldState, waypoints = waypointTestEnvironmentAlt()
    runStory(initWorldState, possibleEvents, 15, waypoints, lookaheadDepth=3)





