import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 10 # 11 seems to be the biggest these can be without changing the screen size and 10 is biggest it can be while retaining space for the messages
GAME_HEIGHT = 10
game_running = True


#### Put class definitions here ####
class Character(GameElement):
    IMAGE = "Zelda" # sets class attribute so your player is a girl
    def __init__(self): # initializer that sets up object with initial values
        GameElement.__init__(self) # tells Character class to call parent class' initializer so that it uses the behaviors of board interactions set
        # self.inventory = []
        self.inventory = {
            "Potion":0,
            "Rocks":0,
            "Hearts":0,
            "Keys":0,
            "Torches":0,
            "Lightings":0,
            "Badguy":True
            } # this instance's inventory starts as an empty list

    def next_pos(self, direction): # when called, takes character and direction set by keyboard handler
        if direction == "up": 
            return (self.x, self.y-1) # returns proper new x and y location for the keyboard_handler's decided direction
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        elif direction == "upright":
            return (self.x+1, self.y-1)
        elif direction == "upleft":
            return (self.x-1, self.y-1)
        elif direction == "downright":
            return (self.x+1, self.y+1)
        elif direction == "downleft":
            return (self.x-1, self.y+1)
        return None

class BadGuy(GameElement):
    IMAGE = "Horns"
    SOLID = False
    
    # when zelda is in 4 specific spaces, bad guy needs to jump on top of you and replace your image (already kind of being worked on).
    # otherwise, when interacted with, if player has a rock, rock image replaces player image
    def interact(self, player):
        if player.inventory["Rocks"] > 0:
            GAME_BOARD.draw_msg("You threw your rock at Ganandorf, and he was like 'Aah!' and got squished. You can now steal his heart!")
            player.inventory["Badguy"] = False
            deadguy = [self.x, self.y]
            GAME_BOARD.del_el(deadguy[0], deadguy[1])
            self.SOLID = True
            deathrock = Rock()
            GAME_BOARD.register(deathrock)
            GAME_BOARD.set_el(deadguy[0], deadguy[1], deathrock)
        else:
            GAME_BOARD.draw_msg("Yeah, running straight at a bad guy with no plan isn't the BEST of ideas. You dead.")
            deathspot = [self.x, self.y]
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            self.SOLID = True
            death = DeathImage()
            GAME_BOARD.register(death)
            GAME_BOARD.set_el(deathspot[0], deathspot[1], death)
            global game_running
            game_running = False

class Link(GameElement):
    IMAGE = "DoorOpen"
    SOLID = False

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Tree(GameElement):
    IMAGE = "BestTree"
    SOLID = True
    def interact(self, player):
        if self.SOLID == False:
            GAME_BOARD.draw_msg("This part of the forest is thinner! You chop it away with your mighty sword, mentally naming yourself 'Zelda Warrior Princess' with a grin.")

class Rock(GameElement):
    IMAGE = "Rock" # sets class attribute so that every rock's image is a rock
    SOLID = True # sets class attribute so that every rock is solid (unless otherwise set)
    def interact(self, player):
        if self.SOLID == False:
            player.inventory["Rocks"] += 1
            GAME_BOARD.draw_msg("You picked up a rock! I bet that can kill mean things or whatever with the %d that you now have."%(player.inventory["Rocks"])) 
"""
class Water(GameElement):
    IMAGE = "Water"
    SOLID = True
    # will this work? it's supposed to be "base" tiles, so it might render funky
"""


class LitLamp(GameElement):
    IMAGE = "LitTorch"
    SOLID = True


class Lamp(GameElement):
    IMAGE = "UnlitTorch"
    SOLID = True

    def interact(self, player):
        if player.inventory["Torches"] > 0:
            player.inventory["Lightings"] += 1
            GAME_BOARD.draw_msg("Ahh, I knew you were carrying that torch around for a reason. Lamp lit! S'mores now?")
            lampspot = [self.x, self.y]
            GAME_BOARD.del_el(lampspot[0], lampspot[1])
            litlamp = LitLamp()
            GAME_BOARD.register(litlamp)
            GAME_BOARD.set_el(lampspot[0], lampspot[1], litlamp)
            # replace unlit lamp image with lit lamp image
        else:
            GAME_BOARD.draw_msg("What's this torch interesting you for when it isn't on FIRE? Off with ye!")
        # FIX SO THAT DOESN'T RE-RENDER!!


class Torch(GameElement):
    IMAGE = "LitTorch"
    SOLID = False
    
    def interact(self, player):
        player.inventory["Torches"] += 1
        GAME_BOARD.draw_msg("Ahh, a torch. Time to play with fire?")



class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
    def interact(self, player):
        if player.inventory["Lightings"] == 2: 
            GAME_BOARD.draw_msg("You saved Link! What a Man-sel in distress, amirite?")
            winspot = [9, 9]
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            link = Link()
            GAME_BOARD.register(link)
            GAME_BOARD.set_el(9, 9, link)
            # WHY IS ALL THE ABOVE FINE BUT DOESN'T RUN IF THE BELOW IS UNCOMMENTED OUT
            #game_end()
        else:
            GAME_BOARD.draw_msg("Hmm...we're at the door, but not even hitting it with your head will open it. Hurry, I think Link is crying!")
        


class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    def interact(self, player):
        player.inventory["Keys"] += 1
        GAME_BOARD.draw_msg("You found a key!! I bet it's edible. With this, think outside the bo--JUST KIDDING DON'T EAT IT.")

class OpenChest(GameElement):
    IMAGE = "OpenChest"
    SOLID = True

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True
    def interact(self, player):
        if player.inventory["Keys"] > 0:
            player.inventory["Keys"] -= 1
            player.inventory["Potion"] += 1
            GAME_BOARD.draw_msg("WHAT? THE KEY OPENED THE LOCK?! Crazy. Inside was a potion which makes your total %d." % (player.inventory["Potion"]))
            chestspot = [self.x, self.y]
            self.SOLID = True
            openchest = OpenChest()
            GAME_BOARD.register(openchest)
            GAME_BOARD.set_el(chestspot[0], chestspot[1], openchest)
            
class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False
    def interact(self, player):
        # player.inventory.append(self.IMAGE)
        player.inventory["Hearts"] += 1
        GAME_BOARD.draw_msg("You now have %d extra lives! %d more and you'll practically be a cat. Use them wisely."%(player.inventory["Hearts"],(8-player.inventory["Hearts"])))

class GreenPotion(GameElement):
    IMAGE = "Potion" 
    SOLID = False

    def interact(self, player):
        player.inventory["Potion"] += 1
        GAME_BOARD.draw_msg("You just got a potion to be bomb-immune! You have %d potions! Go you!"%(player.inventory["Potion"]))
        
        # player.bluecount(self) += 1
        print player.inventory

class DeathImage(GameElement):
    IMAGE = "SkullBones"
    SOLID = True

class Bomb(GameElement):
    IMAGE = "Bomb"
    SOLID = False
    def interact(self, player):
        if player.inventory["Potion"] > 0:
            player.inventory["Potion"] -= 1
            GAME_BOARD.draw_msg("Oh THANK THE HEAVENS you had a blue gem! You would have died. You now have %d potions."%(player.inventory["Potion"]))
        elif player.inventory["Hearts"] > 0:
            player.inventory["Hearts"] -= 1
            GAME_BOARD.draw_msg("EXPLOSION. Close call, but you had an extra life! Be careful with bombs when you're potion-less, silly. You now have %d extra lives."%(player.inventory["Hearts"]))
        else:
            GAME_BOARD.draw_msg("You're super dead now. Sploded. :(")
            deathspot = [self.x, self.y]
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            self.SOLID = True
            death = DeathImage()
            GAME_BOARD.register(death)
            GAME_BOARD.set_el(deathspot[0], deathspot[1], death)
            global game_running
            game_running = False
           
        
####   End class definitions    ####

# define keyboard handler for reading keystrokes and moving character
def keyboard_handler():
    if not game_running:
        return
    # initialize direction to None at start of game
    direction = ""
    # read keystroke and set direction variable
    if KEYBOARD[key.UP]:
        direction += "up"
    elif KEYBOARD[key.DOWN]:
        direction += "down"
    if KEYBOARD[key.LEFT]:
        direction += "left"
    elif KEYBOARD[key.RIGHT]:
        direction += "right"
    """
    # this would be for if arrows turned the direction you were looking so that the program could look at what was in front of you.
    if KEYBOARD[key.SPACE]:
        direction += "use"
    """

    # if a direction is set by keystroke, call next_pos function on Character
    if direction:
        next_location = PLAYER.next_pos(direction) 
        # here we are using the returned tuple from next_pos to find character's new location
        #print next_location
        global PLAYER
        if next_location == (8,5):
            next_location = (3,7)
        elif next_location == (3,7):
            next_location = (8,5)
        elif next_location == (0,9):
            next_location = (4,4)
        elif next_location == (4,4):
            next_location = (0,9)
        elif PLAYER.inventory["Badguy"] == False and (next_location == (7, 0) or next_location == (7,1) or next_location == (8,2) or next_location == (9,2)):
            # delete player
            lastplayer = (PLAYER.x, PLAYER.y)
            GAME_BOARD.del_el(lastplayer[0], lastplayer[1])
            GAME_BOARD.del_el(BADGUY.x, BADGUY.y)
            # add badguy to where you were and give message
            badguywin = BadGuy()
            GAME_BOARD.register(badguywin)
            GAME_BOARD.set_el(lastplayer[0], lastplayer[1], badguywin)
            GAME_BOARD.draw_msg("Just because he's a bad guy doesn't mean he doesn't care about his heart. He had to kill you to save it!!!")
            global game_running
            game_running = False
        

        next_x = next_location[0]
        next_y = next_location[1]

        # check to see if there's anything already in the spot to which you're goin
        # set it to existing_el, existing_el will be false if nothing is there
        """
        global GAME_WIDTH
        global GAME_HEIGHT
        if not (0 <= next.x < GAME_WIDTH) or not (0 <= next.y < GAME_HEIGHT):
            next_x = PLAYER.x
            next_y = PLAYER.y
        """   
        """
        if not (0 <= x < self.width):
            raise IndexError("%r is out of bounds of the board width: %d"%(x, self.width))
        if not (0 <= y < self.height):
            raise IndexError("%r is out of bounds of the board height: %d"%(y, self.width))
        """

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        # check to see if existing element is solid (can I walk through it?)
        
        # if there's nothing in the next spot OR the thing in the next spot isn't solid
        if existing_el is None or not existing_el.SOLID:
            # if there IS something there, and it's a solid BOMB (death)
            if existing_el and existing_el.SOLID and existing_el.IMAGE == "Bomb": 
                game_end()
            # if the thing there is a solid door (end of game)
            elif existing_el and existing_el.SOLID and existing_el.IMAGE == "Door":
                game_end()
            else:
                try:
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)
                except IndexError:
                    print "Forget about it! That's the abyss."
        #if 

# initialize function of game
def initialize():
    #initialize player and location
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(6, 9, PLAYER)
    print PLAYER

    #initialize badguy and location
    global BADGUY
    BADGUY = BadGuy()
    GAME_BOARD.register(BADGUY)
    GAME_BOARD.set_el(7, 2, BADGUY)
    print BADGUY

    # set rock positions
    rock_positions = [
            (4,1), # this movable one is in the middle of nothing at the top of the screen
            (9,4), # this movable one is by the orange gem minefield
            (5,6),
            (5,0),
            (1,9),
            (5,1),
            (3,1)
            ]
    rocks = []

    # initialize and set all rocks from rock_position list
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)
    
    rocks[0].SOLID = False # sets the last rock in the last to NOT solid
    rocks[1].SOLID = False

    for rock in rocks:
        print rock

    potion_positions = [
            (4,0)
        ]
    
    potions = []
    
    for position in potion_positions:
        potion = GreenPotion()
        GAME_BOARD.register(potion)
        GAME_BOARD.set_el(position[0], position[1], potion)
        potions.append(potion)

    bomb_positions = [
            (9,7),
            (9,8),
            (8,7),
            (8,8),
            (8,9),
            (7,7),
            (7,8),
            (7,9),
            (8,4),
            (7,5)
        ]
    
    bombs = []
    
    for position in bomb_positions:
        bomb = Bomb()
        GAME_BOARD.register(bomb)
        GAME_BOARD.set_el(position[0], position[1], bomb)
        bombs.append(bomb)

    wall_positions = [
        (0,6),
        (1,6),
        (2,6),
        (3,6),
        (4,6),
        (4,7),
        (4,8),
        (4,9),
        (3,3),
        (3,4),
        (3,5),
        (3,3),
        (4,3),
        (5,3),
        (5,4),
        (5,5),
        (4,6),
        (2,9),
        (3,9),
    ]
    
    walls = []
    
    for posi in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(posi[0], posi[1], wall)
        walls.append(wall)

    tree_positions = [
            (0,5),
            (1,5),
            (1,4),
            (0,7),
            (1,7),
            (2,0),
            (2,1),
            (1,1),
            (2,7),
            (0,2),
            (1,2),
            (0,8),
            (0,9)
        ]
    
    trees = []
    
    for posit in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(posit[0], posit[1], tree)
        trees.append(tree)
    trees[-1].SOLID = False 
    trees[-2].SOLID = False 
    trees[-3].SOLID = False 
    trees[-4].SOLID = False 

    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(9, 9, door)

    heart_positions = [
            (4,5),
            (8,1)
        ]
        
    hearts = []
        
    for positi in heart_positions:
        heart = Heart()
        GAME_BOARD.register(heart)
        GAME_BOARD.set_el(positi[0], positi[1], heart)
        hearts.append(heart)

    lamp_positions = [
            (0,1),
            (3,0),
        ]
    
    lamps = []
    
    for positi in lamp_positions:
        lamp = Lamp()
        GAME_BOARD.register(lamp)
        GAME_BOARD.set_el(positi[0], positi[1], lamp)
        lamps.append(lamp)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(0, 4, chest)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(1, 8, key)

    torch = Torch()
    GAME_BOARD.register(torch)
    GAME_BOARD.set_el(9, 5, torch)


    GAME_BOARD.draw_msg("Hurry, Zelda! Save Link by opening and reaching the door.")

"""
def game_again():
    answer = raw_input("Would you like to play again? Type 'yes' or 'no'. > ")
    if answer.lower() == "yes":
        initialize()
        global game_running
        game_running = True
    elif answer.lower() == "no":
        print "Awwh, hope you had fun at least."
    else:
        "What? Type 'yes' or 'no', foo."
"""