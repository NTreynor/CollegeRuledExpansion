import copy
import math

class Character:
    def __init__(self, name, health=None, happiness=None, has_job=None, exploited=None, \
        murderer=None, stole=None, in_jail=None, fugitive=None, relationships = None, \
            romantic_partner=None, location=None):
        self.name = name  # string
        self.health = health # scale of 0 to 10
        self.happiness = happiness # scale of 0 to 10
        self.has_job = has_job  # boolean
        self.exploited = exploited  # boolean
        self.murderer = murderer  # boolean
        self.stole = stole  # boolean
        self.in_jail = in_jail # boolean
        self.fugitive = fugitive  # boolean
        self.relationships = relationships # key: other character, val: [-100, 100]
        if relationships == None:
            self.relationships = {}
        self.romantic_partner = romantic_partner  # will be the name of the romantic interest
        self.location = location  # Environment type
        # self.in_spacesuit = False
    
    def getAttributes(self):
        """ for waypointing """
        return [self.health, self.happiness, self.has_job, self.exploited, self.murderer, \
            self.stole, self.in_jail, self.fugitive, self.relationships, self.romantic_partner, self.location]

    def getAttributeDistance(self, attribute_idx, attribute_value):
        if attribute_value == None: # Don't do a comparison if one doesn't need to be made.
            return 0
        if attribute_idx in [0, 1]:  # health or happiness
            dist = (self.getAttributes()[attribute_idx] - attribute_value) * 5 
            dist = abs(dist)
        elif attribute_idx in range(2, 8):  # booleans
            dist = 50
            if self.getAttributes()[attribute_idx] == attribute_value:
                dist = 0
        elif attribute_idx == 8:  #  relationships
            dist = 0
            for character in attribute_value:
                charFound = False
                for character2 in self.relationships:
                    if character.name == character2.name:
                        char_dist = (self.relationships[character2] - attribute_value[character]) * 1/4
                        dist += abs(char_dist)
                        charFound = True
                if charFound == False: # No match found. Increment attribute.
                    char_dist = attribute_value[character] * 1/4  # initialize relationship as 0
                    dist += abs(char_dist)
        elif attribute_idx == 9:  # romantic interest
            if self.romantic_partner != False and self.romantic_partner != None: # If there is a current romantic partner..
                if attribute_value == False: # But no desired future partner, set distance to 50
                    dist = 50
                elif self.romantic_partner.name == attribute_value.name: # The correct partner, distance = 0!
                    dist = 0
                else: # Means there is a romantic partner mismatch. Distance = 50
                    dist = 50
            elif self.romantic_partner == False: 
                if attribute_value == False:
                    dist = 0
                else: # We want a partner that we do not have.
                    dist = 50
            elif self.romantic_partner == None:
                print("Romantic partner set to None. Bug present.")
                return
        elif attribute_idx == 10:  # location
            dist = 0
        return dist
    
    def getDistanceToFutureState(self, future_state_attributes):
        """ returns distance between current state of character
        and future state of character"""
        distance = 0
        for idx, attribute in enumerate(future_state_attributes):
            if attribute:
                distanceInc = self.getAttributeDistance(idx, attribute)
                distance += distanceInc
        return distance

    def updateRelationship(self, other_character, relationship_change):
        """ 
        change relationship between characters by decreasing
        or increasing value
        @relationship_change: int amount to change relationship by, positive or negative"""
        if other_character in self.relationships.keys():
            current_relationship =  self.relationships[other_character]
            new_relationship = current_relationship + relationship_change
            if abs(new_relationship) > 100:
                new_relationship = 100 * new_relationship/abs(new_relationship)

            self.relationships[other_character] = int(new_relationship)
        else:
            current_relationship =  0
            new_relationship = current_relationship + relationship_change
            if abs(new_relationship) > 100:
                new_relationship = 100 * new_relationship/abs(new_relationship)

            self.relationships[other_character] = int(new_relationship)

    
    def updateHealth(self, health_change):
        """ 
        change health of character
        @health_change: int amount to change health by, positive or negative"""
        new_health = self.health + health_change
        if new_health > 10:
            new_health = 10
        elif new_health < 0:
            new_health = 0
        self.health = new_health
    
    def updateHappiness(self, happiness_change):
        """ 
        change happiness of character
        @happiness_change: int amount to change happiness by, positive or negative"""
        new_happiness = self.happiness + happiness_change
        if new_happiness > 10:
            new_happiness = 10
        elif new_happiness < 0:
            new_happiness = 0
        self.happiness = new_happiness
    
    def isDead(self):
        if self.health == 0:
            return True
        return False

    def sameLoc(self, other_character):
        # TODO: if we want location implementation, change this
        # return self.location == other_character.location
        return True

    def __str__(self):
        return "Character name is %s. Relationship matrix is: %s." % (self.name, str(self.relationships))


class Environment:
    def __init__(self, name, quality, spacesuit_needed, has_airlock):
        self.name = name
        self.quality = quality
        self.distances = {}
        self.spacesuit_needed = spacesuit_needed
        self.has_airlock = has_airlock

    def setDistance(self, other_environment, distance_index):
        self.distances[other_environment] = distance_index

    def __str__(self):
        return "Environment name is %s. Distance matrix is: %s." % (self.name, str(self.distances))


# World state should consist of a list of characters and environments.
class WorldState:
    def __init__(self, index, characters, environments, radius = None, desiredDramaCurve = None):
        self.index = index
        self.characters = characters
        self.environments = environments
        self.drama_score = 0
        self.event_history = []  # list of 3D tuples (event, characters involved, environments involved)
        self.radius = radius
        self.drama_curve = desiredDramaCurve
    
    def removeCharacter(self, character):
        for other_character in self.characters:
                if character in other_character.relationships:
                    del other_character.relationships[character]
                if other_character.romantic_partner == character:
                    other_character.romantic_partner = False
        self.characters.remove(character)

    def getDramaCurve(self):
        return self.drama_curve

    def __str__(self):
        return ""


class PlotFragment:
    def __init__(self):
        self.drama = 0  # -20 to 20
        return

    def checkPreconditions(self, worldstate):
        """ return a boolean if the event can happen,
        the characters involved, environments, and the updated drama score"""
        return

    def doEvent(self, worldstate, characters, environment, print_event=True):
        return

    def getNewWorldState(self, worldstate, characters, environment):
        return self.doEvent(worldstate, characters, environment, print_event=False)
    
    def updateEventHistory(self, worldstate, characters, environment):
        updated_state = copy.deepcopy(worldstate)

        charStr = ""
        for char in characters:
            charStr += char.name

        envStr = ""
        for env in environment:
            charStr += char.name

        updated_state.event_history.append((type(self), charStr, envStr))
        return updated_state
    
    def withinInstanceLimit(self, worldstate, characters, environment, repeat_limit):
        """
        checks that a specific instance of this event has not occurred repeat_limit times
        """

        charStr = ""
        for char in characters:
            charStr += char.name
        envStr = ""
        for env in environment:
            charStr += char.name

        numOccurances = (worldstate.event_history.count((type(self), charStr, envStr)))
        return (numOccurances < repeat_limit)
    
    def withinRepeatLimit(self, worldstate, repeat_limit):
        """
        checks that any instance of this event has not occurred repeat_limit times
        """
        count = 0
        for event in worldstate.event_history:
            if event[0] == type(self):
                count += 1
        return count < repeat_limit

    def withinRecentHistoryLimit(self, worldstate, characters, environment, num_recent_events):
        """
        checks that a specific instance of this event hasn't occurred within
        num_recent_events in the worldstate's history
        """

        charStr = ""
        for char in characters:
            charStr += char.name
        envStr = ""
        for env in environment:
            charStr += char.name

        bool = not ((type(self), charStr, envStr) in worldstate.event_history[-1 * num_recent_events:])
        return bool

class DramaCurve:
    def __init__(self, numDistributions, parameters, xrange, desiredPeakDrama):
        """
        NumDistributions is the number of normal distributions we sum to get the drama curve.
        Parameters is a list of touples containing pairs of standard deviations and means for the graph
        Range indicates the range on which we wish to produce numeric drama targets for using the curves.
        desiredPeakDrama is used to calculate an appropriate scaling factor
        """
        self.numDistributions = numDistributions
        self.parameters = parameters
        self.xrange = xrange
        self.drama_targets = []
        self.desiredPeakDrama = desiredPeakDrama

        maxDrama = 0
        for x in range(xrange):
            yVal = 0
            for i in range(numDistributions):
                distStdDev = parameters[i][0]
                distMean = parameters[i][1]
                yVal += self.normpdf(x, distMean, distStdDev)
            if yVal > maxDrama:
                maxDrama = yVal
            self.drama_targets.append(yVal)

        """
        Now that we have populated our dramaCurveTargets, we scale it appropriately.
        """
        scalingFactor = self.desiredPeakDrama / maxDrama
        scaled_drama_targets = []
        for x in range(xrange):
            scaled_drama_targets.append(self.drama_targets[x]*scalingFactor)
        self.drama_targets = scaled_drama_targets

        return

    def normpdf(self, x, mean, sd):
        var = float(sd) ** 2
        denom = (2 * math.pi * var) ** .5
        num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
        return num / denom

    def getDramaTargets(self):
        return self.drama_targets
