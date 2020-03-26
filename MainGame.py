#third party libraries
import pygame
import tcod
import math
from typing import Tuple

#game files
import constants

#class for a menu such as an inventory menu and a menu that pauses the game
class menu():
    def __init__(self,surface, player, nonPlayerList, GameDrawer = None):
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

        gameMessages = []
        menuWidth = 250
        menuHeight = 200
        windowsWidth = constants.mapWidth* constants.cellWidth
        windowsHeight = constants.mapHeight * constants.cellHeight
        inventorySurface = pygame.Surface((menuWidth,menuHeight))

        menuX = windowsWidth/2 - menuWidth/2
        menuY = windowsHeight/2-menuHeight/2


        while not menuClose:
            printList = [obj.displayName for obj in self.player.container.inventory]
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
                              if(len(gameMessages) > 0):
                                  if isinstance(self.player.container.inventory[mouseLineSelection], Item):
                                     print( self.player.container.inventory[mouseLineSelection].item.owner.objName)
                                     gameMessages.append(self.player.container.inventory[mouseLineSelection].item.use(self.nonPlayerList))
                                  else:
                                     gameMessages.append(self.player.container.inventory[mouseLineSelection].equipment.use(self.nonPlayerList))
                              else:
                                  if isinstance(self.player.container.inventory[mouseLineSelection], Item):
                                     print( self.player.container.inventory[mouseLineSelection].item.owner.objName)
                                     gameMessages = [self.player.container.inventory[mouseLineSelection].item.use(self.nonPlayerList)]
                                  else:
                                     gameMessages = [self.player.container.inventory[mouseLineSelection].equipment.use(self.nonPlayerList)]

            #draws inventory items on inv menu
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
        return gameMessages

#class for selecting a target on the screen       
class targetselect:
    def __init__(self,surface, actor, map, nonPlayerList):
        self.surface = surface
        self.player = actor
        self.map = map
        self.nonPlayerList = nonPlayerList

    def menu_target_select(self, coordsOrigin = None, maxRange = None, penetrateWalls = True, mark = None):
        menuClose = False
        while not menuClose:
            #get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #get button clicks
            events_list = pygame.event.get()
            
            mouse_x_rel = mouse_x//constants.cellWidth
            mouse_y_rel = mouse_y//constants.cellHeight

            fullListTiles = []
            validListTiles = []
            if coordsOrigin:
                fullListTiles = self.map.mapLineCreate(coordsOrigin, (mouse_x_rel,mouse_y_rel))

                for i, coords in enumerate(fullListTiles):
                    x,y = coords
                    validListTiles.append((x,y))
                    if maxRange and i == maxRange-1:
                         break
                    if not penetrateWalls and (self.map.checkForWall(x,y)):
                        break

            else:
                validListTiles = [(mouse_x_rel,mouse_y_rel)]

            for event in events_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        menuClose = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button ==1:
                        return validListTiles[-1]
            
                
            self.surface.fill(constants.colorDefaultBG)

            self.map.drawToMap(self.surface)

            for obj in self.nonPlayerList:
                isVisble = tcod.map_is_in_fov(self.map.FOVMAP,obj.x, obj.y)
                if isVisble:
                 obj.draw()

            center = False
            if mark:
                center = True

            #may need to change later for firespell and lighting spell
            self.player.draw()
            for coords in validListTiles:
                x,y = coords
                if coords == validListTiles[-1]:
                    self.draw_tile_rect((x,y), mark, center)
                else:
                     self.draw_tile_rect((x,y))
            pygame.display.flip()
           # self.clock.tick(constants.gameFPS)

    def draw_tile_rect(self,coords, mark = None, center = False):
        x,y= coords
        new_x = x*constants.cellWidth
        new_y = y*constants.cellHeight
        new_surface = pygame.Surface((constants.cellWidth,constants.cellHeight))
        new_surface.fill(constants.colorWhite)
        new_surface.set_alpha(200)
        if mark:
            drawX = drawText(new_surface, mark, constants.colorRed, (constants.cellWidth/2,constants.cellHeight/2))
            drawX.drawOnSurface(incomingFont=constants.fontCursorText, center=center)
            
        self.surface.blit(new_surface,(new_x,new_y))
        
        
#baseclass for an actor. Actor being any object that can interact with a surface
class Actor:
    def __init__(self, x, y, sprite, surface, map, enemyList, objName,creature = None, ai = None, container = None, item = None, equipment = None):
        self.x = x #map address
        self.y = y # map address
        self.objName = objName
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
        
        self.equipment = equipment
        if self.equipment:
            self.equipment.setOwner(self)

            self.item = Item(self,self)

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
            if(self.objName != "Player"):
                if(target.objName == "Player"):
                    gameMessage.append(self.displayName + " attacks " + target.displayName + " for " + str(self.creature.power) + " damage")
                    deathMessage = self.creature.attack(target)
                    if deathMessage:
                        gameMessage.append(deathMessage)
            else:
                gameMessage.append(self.displayName + " attacks " + target.displayName + " for " + str(self.creature.power) + " damage")
                deathMessage = self.creature.attack(target)
                if deathMessage:
                    gameMessage.append(deathMessage)
        return gameMessage
    def getai(self):
        return self.ai
    
    def distanceTo(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx**2 + dy**2)

    def moveTowards(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        dx = int(round(dx/distance))
        dy = int(round(dy/distance))

        return self.move(dx,dy)

    @property
    def displayName(self):
        
        if self.creature:
            return self.creature.name + " the " + self.objName
        elif self.item:
            if self.equipment:
                if self.equipment.equipped:
                    return self.objName + " equipped"
                else:
                    return self.objName + " unequipped"
            else:
                return self.objName


#class for creatures which are controlled by actors
class Creature:
    def __init__(self, name, hp = 10, baseAtck = 2, baseDef = 0):
        self.name = name
        self.hp = hp
        self.owner = None
        self.maxHp = hp
        self.baseAtck = baseAtck
        self.baseDef = baseDef
        self.currentAtck = baseAtck
        self.currentDef = baseDef

    def setOwner(self, owner):
        self.owner = owner
    def takeDamage(self, damage):
        self.hp = self.hp -(damage + self.defense)

        if(self.hp <=0):
            return self.owner.ai.deathFunction()
    def attack(self, target):
        return target.creature.takeDamage(self.power)
    @property 
    def power(self):
        totalPower = self.baseAtck

        if self.owner.container:
            objectBonuses = [obj.equipment.attackBonus for obj in self.owner.container.equippedItems]

            for bonus in objectBonuses:
                totalPower += bonus
        return totalPower
    
    @property 
    def defense(self):
        return self.baseDef
    
    def restoreHP(self, value):
        if(self.hp == self.maxHp):
            return "cancelled"
        else:
            self.hp = min(self.hp+value,self.maxHp)
            return "success"

#class for items. Item class contains different methods depending on what spells are in the game
class Item:
    def __init__(self, owner, player, weight = 0.0, volume = 0.0, healOrDamageVal = 0):
        self.weight = weight
        self.baseVolume = volume
        self.owner = owner
        self.container = None
        self.player = player
        self.value = healOrDamageVal
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
        self.objName = self.owner.objName

    #by default heals the player by eating a corpse
    # will call different methods depending on 
    # what the actor's name is. TO BE FINSIHED
    def use(self, nonPlayerList):
        useResult = self.player.creature.restoreHP(self.value)
        if useResult == "cancelled":
            gameMessages = "Already at full health"
        else:
            gameMessages = "Consumsed corpse to heal for: " + str(self.value)
            self.container.inventory.remove(self.owner)
        return gameMessages

    def lightingSpell(self, value, nonPlayerList):
        
        targetSelection = targetselect(self.player.surface, self.player, self.player.map, nonPlayerList)
        pointSelected = targetSelection.menu_target_select((self.player.x, self.player.y),5,False, mark="X")
        listOfTiles = []
        gameMessages = []
        if pointSelected:
            listOfTiles = self.player.map.mapLineCreate((self.player.x, self.player.y), pointSelected)
            for coords in listOfTiles:
                x,y = coords
                targets = self.player.map.map_objects_atcoords(x,y, nonPlayerList)

                for target in targets:
                    gameMessages.append("lightning spell did " + str(value) + " damage to " + target.displayName)
                    if target.creature:
                        target.creature.takeDamage(value)
        return gameMessages
    
    def confusionSpell(self, numTurns, nonPlayerList):

        targetSelection = targetselect(self.player.surface, self.player, self.player.map, nonPlayerList)
        pointSelected = targetSelection.menu_target_select(mark="X")

        gameMessage = []
        if pointSelected:
            tileX, tileY = pointSelected
            targets = self.player.map.map_objects_atcoords(tileX, tileY, nonPlayerList)

            for target in targets:
                oldAI = target.ai

                target.ai = AIConfuse(oldAI, numTurns)
                target.ai.owner = target

                gameMessage = [ target.ai.owner.displayName + " eyes glaze over"]
        return gameMessage

class Equipment:

    def __init__(self, player, attackBonus , defenseBonus , slot):
        self.attackBonus = attackBonus
        self.defenseBonus = defenseBonus
        self.slot = slot
        self.player = player
        self.equipped = False
        self.baseVolume = 0
        self.container = None

    def setOwner(self,actor):
        self.owner = actor
        self.objName = self.owner.objName

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

    def toggleEquipped(self):
        
        if  self.equipped:
            return self.unequip()
        else:
            return self.equip()
            
    def equip(self):
        self.equipped = True
        return "Item Equipped"
    def unequip(self):
        self.equipped = False
        return "Item Unequipped"

    def use(self, nonPlayerList, equip = True):
        return self.toggleEquipped()

#class for  a container. I.e just a list that is connected to a certain actor
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
    @property
    def equippedItems(self):
        return [obj for obj in self.inventory if isinstance(obj, Equipment) and obj.equipment.equipped]

#class for an individual tile on the map
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
        gameMessage = self.owner.displayName + " is dead!"
        self.owner.creature = None
        self.owner.ai = None
        return gameMessage

class AIChase(AI):
    
    def takeTurn(self):
        gameMessages = []
        monster = self.owner
        player = self.owner.enemyList[0]
        inFOV = tcod.map_is_in_fov(monster.map.FOVMAP, monster.x, monster.y)

        if inFOV:
            gameMessages = monster.moveTowards(player)
        return gameMessages
        
class AIConfuse(AI):

    def __init__(self, oldAI, numTurns = 4):
        self.oldAI = oldAI
        self.numTurns = numTurns
    def takeTurn(self):
        message = []
        if self.numTurns >=0:
            message = self.owner.move(tcod.random_get_int(0,-1,1), tcod.random_get_int(0,-1,1))
            self.numTurns -= 1
        else:
            self.owner.ai = self.oldAI
            message = [self.owner.displayName + " is no longer confused"]
        return message      
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


#class to handle displaying a singular text string to a surface
class drawText:
    def __init__(self,surface,text : str, textColour, coords : Tuple[int,int]):
        self.displaySurface = surface
        self.message = text
        self.coords = coords
        self.colour = textColour
        self.textSurface = constants.fontMessageText.render(self.message, False, self.colour)
        self.textRect = self.textSurface.get_rect()
    def drawOnSurface(self, incomingBGColor = None, incomingFont = None, center = False):
        
        if incomingFont:
            if incomingBGColor:
                self.textSurface = incomingFont.render(self.message, False, self.colour, incomingBGColor)
            else:
                self.textSurface = incomingFont.render(self.message, False, self.colour)
        else:
            if incomingBGColor:
                self.textSurface = constants.fontMessageText.render(self.message, False, self.colour, incomingBGColor)
            else:
                self.textSurface = constants.fontMessageText.render(self.message, False, self.colour)
        self.textRect = self.textSurface.get_rect()

        if center == False:
            self.textRect.topleft = self.coords
        else:
            self.textRect.center = self.coords
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
    
    def mapLineCreate(self, coords1, coords2):

        x1, y1 = coords1
        x2, y2 = coords2

        tcod.line_init(x1, y1, x2, y2)

        calcX, calcY = tcod.line_step()

        coordList = []

        if x1==x2 and y1 == y2:
            return [(x1,y1)]
        
        while(not calcX is None):
            coordList.append((calcX,calcY))

            if calcX == x2 and calcY == y2:
                return coordList
            calcX, calcY = tcod.line_step()
    def checkForWall(self, x, y):
        return self.map[x][y].blockPath

#Main Game class with main game loop
class GameRunner:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(200, 70)
        self.gameMessages = []
        self.ai = AIChase()
        self.ai1 = AIChase()
        self.playerInv = Container()
        self.clock = pygame.time.Clock()
        self.surfaceMain = pygame.display.set_mode( (constants.mapWidth*constants.cellWidth,constants.mapHeight*constants.cellHeight) )
        self.fovCalculate = True

        self.map = Map(self.fovCalculate, None)

        self.playerCreature = Creature("Python")
        self.enemyCreature = Creature("Mr.Krabs")
        self.enemyCreature1 = Creature("Crabby")

        self.itemCom1 = Item(None, None, healOrDamageVal = 5)
        self.itemCom2 = Item(None, None, healOrDamageVal = 5)
        self.testItem = Item(None, None)
        self.testSword = Equipment(None, 2, 0, None)

        self.Sword = Actor(3,3, constants.swordSprite, self.surfaceMain, self.map, [], "Short Sword", equipment=self.testSword)
        self.mainEnemy = Actor(15,15,constants.mainEnemySprite, self.surfaceMain, self.map, [], "Crab", self.enemyCreature, self.ai, item = self.itemCom1)
        self.mainEnemy2 = Actor(15,15,constants.mainEnemySprite, self.surfaceMain, self.map, [], "Crab", self.enemyCreature1, self.ai1, item = self.itemCom2)
        self.enemyList = [self.mainEnemy, self.mainEnemy2, self.Sword]
        
        self.player = Actor(1,1,constants.playerSprite, self.surfaceMain, self.map, self.enemyList, "Player", self.playerCreature, None, self.playerInv)
       
        self.GameDrawer = GameDraw(self.surfaceMain,self.player, self.map, self.enemyList, self.clock, self.gameMessages)
        
        self.menu = menu(self.surfaceMain, self.player, self.enemyList, self.GameDrawer)
        
        self.mainEnemy.enemyList = [self.player, self.mainEnemy2]
        self.mainEnemy2.enemyList = [self.player, self.mainEnemy]

        self.map.player = self.player
        self.itemCom1.player = self.player
        self.itemCom2.player = self.player
        self.testItem.player = self.player
        self.testSword.player = self.player
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
            pygame.display.flip()
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
                        if obj.equipment:
                               print("reached equip pickup")
                               gameMessages = obj.equipment.pickUp(self.GameDrawer.nonPlayerList)
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
                   gameMessages = self.menu.menuInventory()
                   if gameMessages != []:
                            for message in gameMessages:
                                self.gameMessagesAppend(message,constants.colorWhite)
                elif event.key == pygame.K_q:
                    gameMessages = self.testItem.lightingSpell(10, self.GameDrawer.nonPlayerList)
                    if gameMessages != []:
                            for message in gameMessages:
                                self.gameMessagesAppend(message,constants.colorWhite)

                    
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