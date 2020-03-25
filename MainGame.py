#third party libraries
import pygame
import tcod
from typing import Tuple

#game files
import constants

#class for a menu such as an inventory menu and a menu that pauses the game
class menuPause():
    def __init__(self,surface):
        self.surface = surface
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

        while not menuClose:
            inventorySurface.fill(constants.colorBlack)
            eventList = pygame.event.get()

            for event in eventList:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_i:
                        menuClose = True
            self.surface.blit(inventorySurface, ((windowsWidth/2 - menuWidth/2),(windowsHeight/2-menuHeight/2)))
            pygame.display.update()


#baseclass for an actor. Actor being any object that can interact with a surface
class Actor:
    def __init__(self, x, y, sprite, surface, map, enemyList, creature = None, ai = None):
        self.x = x #map address
        self.y = y # map address
        self.sprite = sprite
        self.surface = surface
        self.map = map
        self.ai = AI()
        self.enemyList = enemyList
        self.creature = creature
        if creature:
            self.creature.setOwner(self)
        self.ai = ai
        if ai:
            self.ai.setOwner(self)
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
        if not tileIsWall and (target is None or target.creature.hp <=0): 
            self.x += dx
            self.y += dy
        if target and target.creature is not None:
            gameMessage.append(self.creature.name + " attacks " + target.creature.name + " for 3 damage")
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
    def __init(self):
        self.x = 5
class Container :
    def __init__(self):
        self.x = 5

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
    def __init__(self,surface, actor, map, enemyList, clock, messages):
        self.surface = surface
        self.player = actor
        self.map = map
        self.enemyList = enemyList
        self.clock = clock
        self.gameMessages = messages
        self.drawTextObject = drawText(self.surface,"default", constants.colorWhite,(0,0))
    def drawGame(self):

        self.surface.fill(constants.colorDefaultBG)

        self.map.drawToMap(self.surface)

        for enemy in self.enemyList:
            isVisble = tcod.map_is_in_fov(self.map.FOVMAP,enemy.x, enemy.y)
            if isVisble:
                enemy.draw()
        
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

#Main Game class with main game loop
class GameRunner:
    def __init__(self):
        pygame.init()
        self.gameMessages = []
        self.ai = AI()
        self.clock = pygame.time.Clock()
        self.surfaceMain = pygame.display.set_mode( (constants.mapWidth*constants.cellWidth,constants.mapHeight*constants.cellHeight) )
        self.menu = menuPause(self.surfaceMain)
        self.fovCalculate = True
        self.map = Map(self.fovCalculate, None)
        self.playerCreature = Creature("player")
        self.enemyCreature = Creature("GiantEnemyCrab")
        self.mainEnemy = Actor(15,15,constants.mainEnemySprite, self.surfaceMain, self.map, [],  self.enemyCreature, self.ai)
        self.enemyList = [self.mainEnemy]
        self.player = Actor(1,1,constants.playerSprite, self.surfaceMain, self.map, self.enemyList, self.playerCreature, None)
        self.GameDrawer = GameDraw(self.surfaceMain,self.player, self.map, self.enemyList, self.clock, self.gameMessages)
        self.mainEnemy.enemyList = [self.player]
        self.map.player = self.player
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