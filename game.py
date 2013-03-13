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
class Rock(GameElement):
    IMAGE = "Rock" # sets class attribute so that every rock's image is a rock
    SOLID = True # sets class attribute so that every rock is solid (unless otherwise set)
    def interact(self, player):
        if self.SOLID == False:
            player.inventory["Rocks"] += 1
            GAME_BOARD.draw_msg("You picked up a rock! I bet that can kill things or whatever.") 

class Character(GameElement):
    IMAGE = "Girl" # sets class attribute so your player is a girl
    def __init__(self): # initializer that sets up object with initial values
        GameElement.__init__(self) # tells Character class to call parent class' initializer so that it uses the behaviors of board interactions set
        # self.inventory = []
        self.inventory = {
            "BlueGem":0,
            "Rocks":0,
            "Hearts":0,
            "Keys":0
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
    SOLID = True
    #def interact(self, player)

class Link(GameElement):
    IMAGE = "DoorOpen"
    SOLID = False

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = False
    def interact(self, player):
        GAME_BOARD.draw_msg("You saved Link!")
        winspot = [self.x, self.y]
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        self.SOLID = True
        link = Link()
        GAME_BOARD.register(link)
        GAME_BOARD.set_el(winspot[0], winspot[1], link)
        global game_running 
        game_running = False

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    def interact(self, player):
        # player.inventory.append(self.IMAGE)
        player.inventory["Keys"] += 1
        GAME_BOARD.draw_msg("You found a key!! Try opening something!")

class Tree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True
    def interact(self, player):
        if player.inventory["Keys"] > 0:
            player.inventory["Keys"] -= 1
            player.inventory["BlueGem"] += 1
            GAME_BOARD.draw_msg("Hooray! It opens!! You got a blue gem which makes your total %d" % (player.inventory["BlueGem"]))


class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False
    def interact(self, player):
        # player.inventory.append(self.IMAGE)
        player.inventory["Hearts"] += 1
        GAME_BOARD.draw_msg("You now have %d extra lives! Use them wisely."%(player.inventory["Hearts"]))

class BlueGem(GameElement):
    IMAGE = "BlueGem" # sets attribute to be blue gem
    SOLID = False
    def interact(self, player):
        # player.inventory.append(self.IMAGE)
        player.inventory["BlueGem"] += 1
        GAME_BOARD.draw_msg("You just got a gem! You have %d items! Go you!"%(player.inventory["BlueGem"]))
        
        # player.bluecount(self) += 1
        print player.inventory

class DeathImage(GameElement):
    IMAGE = "SkullBones"
    SOLID = True

class OrangeGem(GameElement):
    IMAGE = "OrangeGem"
    SOLID = False
    def interact(self, player):
        if player.inventory["BlueGem"] > 0:
            player.inventory["BlueGem"] -= 1
            GAME_BOARD.draw_msg("Oh THANK THE HEAVENS you had a blue gem! You would have died. You now have %d blue gems."%(player.inventory["BlueGem"]))
        elif player.inventory["Hearts"] > 0:
            player.inventory["Hearts"] -= 1
            GAME_BOARD.draw_msg("Oh THANK THE HEAVENS you had an extra life! You would have died. You now have %d extra lives."%(player.inventory["Hearts"]))
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
           
            """
            deathorange = OrangeGem()
            self.SOLID = True
            #deathorange.SOLID = True # sets the last rock in the last to NOT solid
            print deathorange
            GAME_BOARD.register(deathorange)
            GAME_BOARD.set_el(deathspot[0], deathspot[1], deathorange)
            print deathorange
            """
        
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
    # elif KEYBOARD[key.RIGHT] and KEYBOARD[key.UP]:
        # direction = "right up"

    # if a direction is set by keystroke, call next_pos function on Character
    if direction:
        next_location = PLAYER.next_pos(direction) 
        # here we are using the returned tuple from next_pos to find character's new location
        #print next_location

        if next_location == (6,2):
            next_location = (1,6)
        elif next_location == (1,6):
            next_location = (6,2)
        elif (next_location == (6, 1) or next_location == (5,0)) and (BADGUY.x, BADGUY.y) == (5,1):
            # delete player
            lastplayer = (PLAYER.x, PLAYER.y)
            GAME_BOARD.del_el(lastplayer[0], lastplayer[1])
            GAME_BOARD.del_el(BADGUY.x, BADGUY.y)
            # add badguy to where you were and give message
            badguywin = BadGuy()
            GAME_BOARD.register(badguywin)
            GAME_BOARD.set_el(lastplayer[0], lastplayer[1], badguywin)
            GAME_BOARD.draw_msg("Just because he's a bad guy doesn't mean he doesn't care about his heart. He had to kill you to save it!!!")
            global running_game
            running_game = False

        next_x = next_location[0]
        next_y = next_location[1]

        # check to see if there's anything already there
        existing_el = GAME_BOARD.get_el(next_x, next_y)
       
        if existing_el:
            existing_el.interact(PLAYER)

        # check to see if existing element is solid (can I walk through it?)
        

        if existing_el is None or not existing_el.SOLID:
            # if there's nothing there, or if the el's not solid, walk through
            
            if existing_el and existing_el.SOLID and existing_el.IMAGE == "OrangeGem": # is an orange and is solid 
                pass
            elif existing_el and existing_el.SOLID and existing_el.IMAGE == "Door":
                pass
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
    GAME_BOARD.set_el(3, 6, PLAYER)
    print PLAYER

    #initialize badguy and location
    global BADGUY
    BADGUY = BadGuy()
    GAME_BOARD.register(BADGUY)
    GAME_BOARD.set_el(5, 1, BADGUY)
    print BADGUY

    # set rock positions
    rock_positions = [
            (0, 0), 
            (3, 2),
            (2, 3)
            ]
    rocks = []

    # initialize and set all rocks from rock_position list
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)
    
    rocks[0].SOLID = False # sets the last rock in the last to NOT solid

    for rock in rocks:
        print rock

    
    
        """
    for position in bluegem_positions:
        bluegem = BlueGem()
        GAME_BOARD.register(bluegem)
        GAME_BOARD.set_el(position[0], position[1], bluegem)
        blues.append(bluegem)
"""
    orangegem_positions = [
            (6, 5),
            (5, 5),
            (5, 6),
            (5, 4),
            (6, 4),
            (4, 4),
            (4, 5),
            (4, 6)
        ]
    
    oranges = []
    

    for position in orangegem_positions:
        orangegem = OrangeGem()
        GAME_BOARD.register(orangegem)
        GAME_BOARD.set_el(position[0], position[1], orangegem)
        oranges.append(orangegem)

    wall_positions = [
        (1, 1),
        (1, 2),
        (1, 5),
        (2, 5),
        (2, 6),
    ]
    
    walls = []
    

    for posi in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(posi[0], posi[1], wall)
        oranges.append(wall)

    tree_positions = [
            (1, 0),
            (2, 0),
            (0, 5),
            (2, 2)
        ]
    
    trees = []
    
    for posit in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(posit[0], posit[1], tree)
        trees.append(tree)
    trees[0].SOLID = False 
    trees[1].SOLID = False 


    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(6, 6, door)

    heart = Heart()
    GAME_BOARD.register(heart)
    GAME_BOARD.set_el(6, 0, heart)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(2, 1, chest)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(0, 6, key)



    GAME_BOARD.draw_msg("Hurry, Zelda! Save Link by reaching the door.")

    
