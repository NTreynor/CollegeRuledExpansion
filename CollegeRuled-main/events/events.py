from backbone_classes import *
import copy

class GetMiningJob(PlotFragment):
    def __init__(self):
        self.drama = 4

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 5):
            return False, None, environments
        for character in worldstate.characters:
            if not (character.has_job or character.fugitive):
                valid_characters.append([character])
                environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("After visiting the open market every day and getting increasingly desperate", \
                "{} got a mining job.".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(3)
        char.has_job = True
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)



class GetSpaceShuttleJob(PlotFragment):
    def __init__(self):
        self.drama = 4

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            if not character.has_job:
                valid_characters.append([character])
                environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("{} got a job flying transport shuttles for interplanet exports.".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(5)
        char.has_job = True
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class LoseJob(PlotFragment):
    def __init__(self):
        self.drama = 11

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            if character.has_job:
                valid_characters.append([character])
                environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("The empire decreases exports from Higgins and the economy takes a hit. {} loses their job".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(-5)
        char.has_job = False
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)



class CoffeeSpill(PlotFragment):
    def __init__(self):
        self.drama = 3

    def checkPreconditions(self, worldstate):
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, []
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            for character2 in character.relationships:
                if character.sameLoc(character2):
                    valid_characters.append([character, character2])
                    environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("{} is walking along with a fresh cup of hydrozine, and loses their footing right as they would pass by {}, spilling their drink all over them! \"Oh goodness, sorry about that!\" says {}.".format(characters[0].name, characters[1].name, characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char = reachable_worldstate.characters[char_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char.updateRelationship(char_two, 5)
        char_two.updateRelationship(char, -5)
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class DoNothing(PlotFragment):
    def __init__(self):
        self.drama = 0

    def checkPreconditions(self, worldstate):
        if self.withinRecentHistoryLimit(worldstate, [], [], 3):
            return True, [[]], [[]]
        return False, [[]], [[]]

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event == True:
            print(".")
        return self.updateEventHistory(reachable_worldstate, characters, environment)

