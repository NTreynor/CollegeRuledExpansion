from backbone_classes import *
import copy

class FallInLove(PlotFragment):
    def __init__(self):
        self.drama = 7


    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 6):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    character.updateRelationship(character2, 0) # if no relationship, add to relationship table
                    if (character.relationships[character2] >= 0):
                        if self.withinRecentHistoryLimit(worldstate, [character, character2], [], 3):
                            if self.withinInstanceLimit(worldstate, [character, character2], [], 2):
                                valid_characters.append([character, character2])
                                environments.append([])
                        

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        if print_event:
            print("{} looks at {} and realizes their feelings for them have been growing stronger as they have spent time together.".format(characters[0].name, characters[1].name), \
                "They find themselves thinking about {} more and more.".format(characters[1].name))
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 25)
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class Befriend(PlotFragment):
    def __init__(self):
        self.drama = 3


    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 6):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    character.updateRelationship(character2, 0) # if no relationship, add to relationship table
                    if (character.relationships[character2] >= 0):
                        if self.withinRecentHistoryLimit(worldstate, [character, character2], [], 3):
                            if self.withinInstanceLimit(worldstate, [character, character2], [], 2):
                                valid_characters.append([character, character2])
                                environments.append([])
                        

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
            

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        if print_event:
            print("{} and {} go for drinks at the Leaky Engine and make each other laugh a lot".format(characters[0].name, characters[1].name), \
                '"We should do this again," {} says.'.format(characters[1].name))
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 10)
        char_two.updateRelationship(char_one, 10)
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class Irritate(PlotFragment):
    def __init__(self):
        self.drama = 3


    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 6):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if self.withinRecentHistoryLimit(worldstate, [character, character2], [], 3):
                        valid_characters.append([character, character2])
                        environments.append([])

                        

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        if print_event:
            print("{} makes a rude 'your mom' joke. {} doesn't laugh".format(characters[0].name, characters[1].name))
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_two.updateRelationship(char_one, -5)
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class AskOnDate(PlotFragment):
    def __init__(self):
        self.drama = 11

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 4):
            return False, None, environments
        for character in worldstate.characters:
                for character2 in character.relationships:
                    if (character.relationships[character2] > 50) & (character.romantic_partner == None or character.romantic_partner == False):
                        if self.withinInstanceLimit(worldstate, [character, character2], [], 1):
                            valid_characters.append([character, character2])
                            environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        if print_event:
            print("{} asks {} to go on a picnic with them at the Rocket Wreck Hills. Their heart is racing.".format(characters[0].name, characters[1].name))
        if characters[1]. relationships[characters[0]] < 50 or (characters[1].romantic_partner != None and characters[1].romantic_partner != False):
            return self.getRejected(worldstate, characters, environment, print_event)
        else:
            return self.goOnDate(worldstate, characters, environment, print_event)
    
    def getRejected(self, worldstate, characters, environment, print_event):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        if print_event:
            print("{} declines {}'s invitation.".format(char_two.name, char_one.name))
        char_one.relationships[char_two] -= 5
        char_two.relationships[char_one] += 10
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)
    
    def goOnDate(self, worldstate, characters, environment, print_event):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        if print_event:
            print("{} blushes and says they would love to go on a date with {}.".format(char_two.name, char_one.name))
        char_one.relationships[char_two] += 20
        char_two.relationships[char_one] += 30
        char_one.romantic_partner = char_two
        char_two.romantic_partner = char_one
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class Cheat(PlotFragment):
    def __init__(self):
        self.drama = 17
    
    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, environments
        for character in worldstate.characters:
                for character2 in character.relationships:
                    if character.romantic_partner != None and character.romantic_partner != False:
                        if character.romantic_partner != character2:
                            valid_characters.append([character, character2])
                            environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        prev_partner_idx = worldstate.characters.index(characters[0].romantic_partner)
        cheater_idx = worldstate.characters.index(characters[0])
        new_state = AskOnDate().doEvent(worldstate, characters, environment, print_event)
        cheater = new_state.characters[cheater_idx]
        prev_partner = new_state.characters[prev_partner_idx]
        if print_event:
            print("{} finds out what {} did and is devastated. They break up with {}.".format(prev_partner.name, cheater.name, cheater.name))
        if cheater.romantic_partner == prev_partner:
            cheater.romantic_partner = False
        prev_partner.romantic_partner = False
        prev_partner.relationships[cheater] -= 30
        prev_partner.updateHappiness(-5)
        new_state.drama_score += self.drama
        return self.updateEventHistory(new_state, characters, environment)

        