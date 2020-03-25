#third party libraries
import pygame
import tcod
from typing import Tuple

#game files
import constants

#class for a menu such as an inventory menu and a menu that pauses the game
class menu():
    def __init__(self,surface, player, nonPlayerList):
        self.surface = surface
        self.player = player
        self.nonPlayerList = nonPlayerList
    def menuPause(self):

        windowsWidth = constants.mapWidth* constants.cellWidth
        windowsHeight = constants.mapHeight * constants.cellHeight
        menuText = "PAUSED PRESS P TO UNPAUSE"
        menuClose = False
        while not menuClose:
            eventList = pygame.event.get()

            for event in eventList:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_p:
                        menuClose = True

            drawPauseMessage = drawText(self.surface, menuText, constants.colorWhite, 
                                       ((windowsWidth) / 2,windowsHeight / 2))
            drawPauseMessage.coords     = (drawPauseMessage.coords[0]-(drawPauseMessage.textWidth()/2), drawPauseMessage.coords[1]-(drawPauseMessage.textHeight()/2))
            drawPauseMessage.drawOnSurface(constants.colorBlack)  
            pygame.display.flip()
   
    def menuInventory(self):

        menuClose = False

        menuWidth = 200
        menuHeight = 200
        windowsWidth = constants.mapWidth* constants.cellWidth
        windowsHeight = constants.mapHeight * constants.cellHeight
        inventorySurface = pygame.Surface((menuWidth,menuHeight))

        menuX = windowsWidth/2 - menuWidth/2
        menuY = windowsHeight/2-menuHeight/2


        while not menuClose:
            printList = [obj.objName for obj in self.player.container.inventory]
            drawInv = drawText(inventorySurface, "blah", constants.colorWhite,
                                   (0,0+1))
            inventorySurface.fill(constants.colorBlack)
            
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseXRelative = mouseX - menuX
            mouseYRelative = mouseY - menuY

            mouseLineSelection = int(mouseYRelative / drawInv.textHeight())
            mouseInWindow = (mouseXRelative > 0 and mouseYRelative > 0) and (mouseXRelative < menuWidth and mouseYRelative < menuHeight)

            eventList = pygame.event.get()
            for event in eventList:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_i:
                        menuClose = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (mouseInWindow and 
                            mouseLineSelection <= len(printList)-1):
                               self.player.container.inventory[mouseLineSelection].item.drop(self.nonPlayerList)

            for line , (name) in enumerate(printList):
                
                if line == mouseLineSelection and mouseInWindow:
                    drawInv = drawText(inventorySurface, name, constants.colorWhite,
                                   (0,0))
                    drawInv.coords = (0,0+line*drawInv.textHeight())
                    drawInv.drawOnSurface(constants.colorGrey)
                else:
                    drawInv = drawText(inventorySurface, name, constants.colorWhite,
                                    (0,0))
                    drawInv.coords = (0,0+line*drawInv.textHeight())
                    drawInv.drawOnSurface()
            self.surface.blit(inventorySurface, ((menuX),(menuY)))
            pygame.display.update()

#baseclass for an actor. Actor being any object that can interact with a surface
class Actor:
    def __init__(self, x, y, sprite, surface, map, enemyList, objName,creature = None, ai = None, container = None, item = None):
        self.x = x #map address
        self.y = y # map address
        self.sprite = sprite
        self.surface = surface
        self.map = map
        self.ai = AI()
        self.enemyList = enemyList
        self.objName = objName
       
        self.creature = creature
        if creature:
            self.creature.setOwner(self)

        self.ai = ai
        if ai:
            self.ai.setOwner(self)

        self.container = container
        if self.container:
            self.container.setOwner(self)

        self.item = item
        if self.item:
            self.item.setOwner(self)

    def draw(self):
        self.surface.blit(self.sprite, ( self.x*constants.cellWidth, self.y*constants.cellHeight ))
    def move(self,dx,dy):
        tileIsWall = ((self.map.getCurrentMap())[self.x + dx][self.y + dy].blockPath == True)

        target = None

        gameMessage = []

        for enemy in self.enemyList:
            if (enemy.x == self.x + dx and enemy.y == self.y + dy):
                target = enemy
                break
        if not tileIsWall and target is None:
                self.x += dx
                self.y += dy
        elif(not tileIsWall and target is not None):
            if target.creature == None:
                 self.x += dx
                 self.y += dy
        if target and target.creature is not None:
            gameMessage.append(self.creature.name + " attacks " + target.creature.name + "for 3 damage")
            deathMessage = target.creature.takeDamage(3)
            if deathMessage:
                gameMessage.append(deathMessage)
        return gameMessage
    def getai(self):
        return self.ai

#classes for creatures, containers, and items

class Creature():
    def __init__(self, name, hp = 10):
        self.name = name
        self.hp = hp
        self.owner = None

    def setOwner(self, owner):
        self.owner = owner
    def takeDamage(self, damage):
        self.hp -= damage

        if(self.hp <=0):
            return self.owner.ai.deathFunction()

class Item:
    def __init__(self, owner, player, weight = 0.0, volume = 0.0):
        self.weight = weight
        self.baseVolume = volume
        self.owner = owner
        self.container = None
        self.player = player
    def pickUp(self, nonPlayerList):
        gameMessages = []
        if self.player.container:
            if self.player.container.volume + self.baseVolume > self.player.container.baseVolume:
                gameMessages = ["Not enough inv space"]
            else:
                gameMessages = ["Picking up item"]
                self.player.container.inventory.append(self.owner)
                nonPlayerList.remove(self.owner)
                self.container = self.player.container
        return gameMessages
    def drop(self, nonPlayerList):
        gameMessages = ["Dropping Item"]
        self.container.inventory.remove(self.owner)
        self.owner.x = self.player.x
        self.owner.y = self.player.y
        nonPlayerList.append(self.owner)
        return gameMessages
    
    def setOwner(self,actor):
        self.owner = actor

class Container :
    def __init__(self, volume = 10.0, inventory = []):
        self.inventory = inventory
        self.baseVolume = volume
        self.owner = None
        self.currentVolume = 0.0
    def setOwner(self,owner):
        self.owner = owner
    @property
    def volume(self):
        return self.currentVolume

#class for an individual tile
class tileStrucutre:
    def __init__(self, blockPath):
        self.blockPath = blockPath
        self.explored = False
        
#class to handle AI for the enemies
class AI:
    def __init__(self):
        self.owner = None
    def setOwner(self,owner):
        self.owner = owner
    def takeTurn(self):
        message = self.owner.move(tcod.random_get_int(0,-1,1), tcod.random_get_int(0,-1,1))
        return message
    def deathFunction(self):
        gameMessage = self.owner.creature.name + "is dead!"
        self.owner.creature = None
        self.owner.ai = None
        return gameMessage
#class to update the game's UI by updating/drawing the screen
class GameDraw:
    def __init__(self,surface, actor, map, nonPlayerList, clock, messages):
        self.surface = surface
        self.player = actor
        self.map = map
        self.nonPlayerList = nonPlayerList
        self.clock = clock
        self.gameMessages = messages
        self.drawTextObject = drawText(self.surface,"default", constants.colorWhite,(0,0))
    def drawGame(self):

        self.surface.fill(constants.colorDefaultBG)

        self.map.drawToMap(self.surface)

        for obj in self.nonPlayerList:
            isVisble = tcod.map_is_in_fov(self.map.FOVMAP,obj.x, obj.y)
            if isVisble:
                obj.draw()
        
        self.player.draw()
        self.drawMessages()

        pygame.display.flip()
    def drawMessages(self):
        toDraw = []
        if len(self.gameMessages) <= constants.numMessages:
            toDraw = self.gameMessages
        else:
            toDraw = self.gameMessages[-constants.numMessages:]

        startY = constants.mapHeight*constants.cellHeight - (constants.numMessages * self.drawTextObject.textHeight()) -10

        i = 0
        for message, color in toDraw:
            self.drawTextObject.message = message
            self.drawTextObject.colour = color
            self.drawTextObject.coords = (0, startY + (i*self.drawTextObject.textHeight()))
            self.drawTextObject.drawOnSurface(constants.colorBlack)
            i+=1

#class to handle displaying a singular text string to the game's text log to a surface
class drawText:
    def __init__(self,surface,text : str, textColour, coords : Tuple[int,int]):
        self.displaySurface = surface
        self.message = text
        self.coords = coords
        self.colour = textColour
        self.textSurface = constants.fontMessageText.render(self.message, False, self.colour)
        self.textRect = self.textSurface.get_rect()
    def drawOnSurface(self, incomingBGColor = None):
        
        if incomingBGColor:
            self.textSurface = constants.fontMessageText.render(self.message, False, self.colour, incomingBGColor)
        else:
             self.textSurface = constants.fontMessageText.render(self.message, False, self.colour)
        self.textRect = self.textSurface.get_rect()

        self.textRect.topleft = self.coords
        self.displaySurface.blit(self.textSurface, self.textRect)
    def textHeight(self):
        return self.textRect.height
    def textWidth(self):
        return self.textRect.width

#class to handle the game's map
class Map:
    def __init__(self, fovCalculate, player):
        self.fovCalculate = fovCalculate
        self.player = player
        self.map = [[ tileStrucutre(False) for y in range(0,constants.mapWidth)] for x in range(0,constants.mapHeight)]

        self.map[10][10].blockPath = True
        self.map[10][15].blockPath = True

        for x in range(constants.mapWidth):
            self.map[x][0].blockPath = True
            self.map[x][constants.mapHeight-1].blockPath = True
        for x in range(constants.mapHeight):
            self.map[0][x].blockPath = True
            self.map[constants.mapHeight-1][x].blockPath = True
    
        self.makeFOV()

    def getCurrentMap(self):
        return self.map
    
    def drawToMap(self, surface):
        for x in range(0,constants.mapWidth):
            for y in range(0,constants.mapHeight):

                isVisible = tcod.map_is_in_fov(self.FOVMAP,x,y)
               
                if isVisible:
                    self.map[x][y].explored = True
                    if self.map[x][y].blockPath == True:
                        surface.blit(constants.wallSprite, ( x*constants.cellWidth, y*constants.cellHeight))
                    else: 
                        surface.blit(constants.floorSprite, ( x*constants.cellWidth, y*constants.cellHeight))
                elif(self.map[x][y].explored):
                    if self.map[x][y].blockPath == True:
                        surface.blit(constants.wallExploredSprite, ( x*constants.cellWidth, y*constants.cellHeight))
                    else: 
                        surface.blit(constants.floorExploredSprite, ( x*constants.cellWidth, y*constants.cellHeight))
    def makeFOV(self):
            self.FOVMAP = tcod.map_new(constants.mapWidth, constants.mapHeight)

            for y in range(constants.mapHeight):
                for x in range(constants.mapWidth):
                    tcod.map_set_properties(self.FOVMAP, x, y, not self.map[x][y].blockPath, not self.map[x][y].blockPath)

    def calculateFOV(self):
        if(self.fovCalculate):
            self.fovCalculate = False
            tcod.map_compute_fov(self.FOVMAP, self.player.x, self.player.y, constants.torchRadius, constants.FOVLIGHTWALLS, constants.FOVALGO)

    def map_objects_atcoords(self,coords_x,coords_y, nonPlayerList):
        objectOptions = [obj for obj in nonPlayerList if obj.x == coords_x and obj.y == coords_y]
        return objectOptions
#Main Game class with main game loop
class GameRunner:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(200, 70)
        self.gameMessages = []
        self.ai = AI()
        self.ai1 = AI()
        self.playerInv = Container()
        self.clock = pygame.time.Clock()
        self.surfaceMain = pygame.display.set_mode( (constants.mapWidth*constants.cellWidth,constants.mapHeight*constants.cellHeight) )
        self.fovCalculate = True

        self.map = Map(self.fovCalculate, None)

        self.playerCreature = Creature("player")
        self.enemyCreature = Creature("GiantEnemyCrab")
        self.enemyCreature1 = Creature("Crabby Boi 2")

        self.itemCom1 = Item(None, None)
        self.itemCom2 = Item(None, None)
        self.mainEnemy = Actor(15,15,constants.mainEnemySprite, self.surfaceMain, self.map, [], "Crab", self.enemyCreature, self.ai, item = self.itemCom1)
        self.mainEnemy2 = Actor(15,15,constants.mainEnemySprite, self.surfaceMain, self.map, [], "Crab Boi 2", self.enemyCreature1, self.ai1, item = self.itemCom2)
        self.enemyList = [self.mainEnemy, self.mainEnemy2]
        
        self.player = Actor(1,1,constants.playerSprite, self.surfaceMain, self.map, self.enemyList, "Python", self.playerCreature, None, self.playerInv)
        
        self.menu = menu(self.surfaceMain, self.player, self.enemyList)
       
        self.GameDrawer = GameDraw(self.surfaceMain,self.player, self.map, self.enemyList, self.clock, self.gameMessages)
        self.mainEnemy.enemyList = [self.player]
        self.mainEnemy2.enemyList = [self.player]

        self.map.player = self.player
        self.itemCom1.player = self.player
        self.itemCom2.player = self.player
    def game_main_loop(self):
 
        gameQuitStatus = False
        while not gameQuitStatus:
            playerAction = "no-action"
            playerAction = self.handleKeys()
            self.map.calculateFOV()
            if playerAction == "QUIT":
                gameQuitStatus = True

            if playerAction != "no-action":
                for enemy in self.enemyList:
                    if(enemy.ai != None):
                        gameMessage = enemy.getai().takeTurn()
                        if gameMessage != []:
                            for message in gameMessage:
                                self.gameMessagesAppend(message,constants.colorWhite)
            self.GameDrawer.drawGame()
            self.clock.tick(constants.gameFPS)
        pygame.quit()
        exit()

    def gameMessagesAppend(self, gameMessage, msgColor):
        self.gameMessages.append((gameMessage,msgColor))
       # self.GameDrawer.gameMessages.append((gameMessage,msgColor))
     
    def handleKeys(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                   gameMessage = self.player.move(0,-1)
                   if gameMessage != []:
                        for message in gameMessage:
                            self.gameMessagesAppend(message,constants.colorWhite)
                   self.map.fovCalculate = True
                   return "player-moved"
                elif event.key == pygame.K_DOWN:
                    gameMessage = self.player.move(0,1)
                    if gameMessage != []:
                        for message in gameMessage:
                            self.gameMessagesAppend(message,constants.colorWhite)
                    self.map.fovCalculate = True
                    return "player-moved"
                elif event.key == pygame.K_LEFT:
                   gameMessage = self.player.move(-1,0)
                   if gameMessage != []:
                        for message in gameMessage:
                            self.gameMessagesAppend(message,constants.colorWhite)
                   self.map.fovCalculate = True
                   return "player-moved"
                elif event.key == pygame.K_RIGHT:
                   gameMessage = self.player.move(1,0)
                   if gameMessage != []:
                        for message in gameMessage:
                            self.gameMessagesAppend(message,constants.colorWhite)
                   self.map.fovCalculate = True
                   return "player-moved"
                if event.key == pygame.K_g:
                    #get items at current location
                    objects_at_player = self.map.map_objects_atcoords(self.player.x, self.player.y, self.GameDrawer.nonPlayerList)

                    for obj in objects_at_player:
                        if obj.item:
                           gameMessages = obj.item.pickUp(self.GameDrawer.nonPlayerList)
                           if gameMessages != []:
                                for message in gameMessages:
                                    self.gameMessagesAppend(message,constants.colorWhite)
                if event.key == pygame.K_d:
                     if len(self.player.container.inventory) > 0:
                         gameMessages = self.player.container.inventory[-1].item.drop(self.GameDrawer.nonPlayerList)
                         if gameMessages != []:
                                for message in gameMessages:
                                    self.gameMessagesAppend(message,constants.colorWhite)
                elif event.key == pygame.K_p:
                    self.menu.menuPause()
                elif event.key == pygame.K_i:
                    self.menu.menuInventory()
        return "no-action"

#class to start the game. AKin to TicTacToeApplication in Assignment 1 of Software Design
class MainGameApplication:
    def __init__(self):
        self.NewGame = GameRunner()

    def RunGame(self):
        self.NewGame.game_main_loop()

if __name__ == '__main__':
    MainGame = MainGameApplication()
    MainGame.RunGame()