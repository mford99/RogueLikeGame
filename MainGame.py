#third party libraries
import pygame
import tcod
import math
from typing import Tuple

#game files
import constants

#class to handle putting stairs at a certain position
class genStairs:
    def __init__(self, surface, map, nonPlayerList, surfaceMap):
        self.surface  = surface
        self.map = map
        self.nonPlayerList = nonPlayerList
        self.surfaceMap = surfaceMap
    
    def genStairs(self, coords, downwards):
        x,y = coords

        if downwards:
            stairs = Stairs(downwards)

            stairsActor = Actor(x,y, constants.stairsSprite, self.surface, self.map, [], "Stairs", stairs= stairs, surfaceMap=self.surfaceMap)

            self.nonPlayerList.append(stairsActor)

class genPlayer:

    def __init__(self, surface, map, nonPlayerList, surfaceMap):
        self.surface  = surface
        self.map = map
        self.nonPlayerList = nonPlayerList
        self.surfaceMap = surfaceMap

    def generate(self, coords):
        x,y = coords
        playerCreature = Creature("Python", 15, baseAtck=3)
        playerInv = Container()
        player = Actor(x,y,constants.playerSprite, self.surface, self.map, self.nonPlayerList, "Player", playerCreature, None, playerInv, surfaceMap= self.surfaceMap)
        self.nonPlayerList.append(player)
        return player

class genEnemies:
    
    def __init__(self,surface, player, map, nonPlayerList, surfaceMap):
        self.surface = surface
        self.player = player
        self.map = map
        self.nonPlayerList = nonPlayerList
        self.surfaceMap = surfaceMap
    
    def genEnemy(self, coords):
        randomNum = tcod.random_get_int(0,1,100)

        if randomNum > 15: 
            crabEnemy = genCrab(coords, self.surface, self.player, self.map, self.nonPlayerList, self.surfaceMap)
            crabEnemyActor = crabEnemy.generate()
            self.nonPlayerList.append(crabEnemyActor)
            return crabEnemyActor
        else: 
            cobraEnemy = genCobra(coords, self.surface, self.player, self.map, self.nonPlayerList, self.surfaceMap)
            cobraEnemyActor = cobraEnemy.generate()
            self.nonPlayerList.append(cobraEnemyActor)
            return cobraEnemyActor

class genCrab:
    def __init__(self,coords, surface, player, map, nonPlayerList, surfaceMap):
        self.coords = coords
        self.player = player
        self.map = map
        self.surface = surface
        self.itemActor = None
        self.nonPlayerList = nonPlayerList
        self.surfaceMap = surfaceMap
    
    def generate(self):
        x,y = self.coords
        CorpseItem = Item(None, self.player, healOrDamageVal = 5, camera = None)

        maxHealth = tcod.random_get_int(0,7,10)
        baseAttck = tcod.random_get_int(0,2,3)

        enemyCreature = Creature("Mr. Crabs", maxHealth, baseAttck)
        aiCom = AIChase()
        self.itemActor = Actor(x,y, constants.mainEnemySprite, self.surface, self.map, self.nonPlayerList, "Crab", enemyCreature ,item = CorpseItem, ai = aiCom, surfaceMap=self.surfaceMap)
        return self.itemActor

class genCobra:
    def __init__(self,coords, surface, player, map, nonPlayerList, surfaceMap):
        self.coords = coords
        self.player = player
        self.map = map
        self.surface = surface
        self.itemActor = None
        self.nonPlayerList = nonPlayerList
        self.surfaceMap = surfaceMap

    def generate(self):
        x,y = self.coords
        CorpseItem = Item(None, self.player, healOrDamageVal = 8, camera=None)
        
        maxHealth = tcod.random_get_int(0,12,14)
        baseAttck = tcod.random_get_int(0,2,3)

        enemyCreature = Creature("Buns", hp = maxHealth, baseAtck = baseAttck)
        aiCom = AIChase()
        self.itemActor = Actor(x,y, constants.rareCobraSprite, self.surface, self.map, self.nonPlayerList, "Cobra", enemyCreature, item = CorpseItem, ai = aiCom, surfaceMap = self.surfaceMap)
        return self.itemActor

class randomItemGeneration:
    def __init__(self,surface, player, map, nonPlayerList, surfaceMap):
        self.surface = surface
        self.player = player
        self.map = map
        self.nonPlayerList = nonPlayerList
        self.surfaceMap = surfaceMap
    
    def genItem(self, coords, camera):
        randomNum = tcod.random_get_int(0,1,5)

        if randomNum == 1: 
            lightningSpell = genLighting(coords, self.surface, self.player, self.map, self.surfaceMap)
            lightningSpellActor = lightningSpell.generate(camera)
            self.nonPlayerList.append(lightningSpellActor)
            return lightningSpellActor
        if randomNum == 2: 
            confusionSpell = genConfusionSpell(coords, self.surface, self.player, self.map, self.surfaceMap)
            confusionSpellActor = confusionSpell.generate(camera)
            self.nonPlayerList.append(confusionSpellActor)
            return confusionSpellActor
        if randomNum == 3: 
            sword = genSword(coords, self.surface, self.player, self.map,self.surfaceMap)
            swordActor = sword.generate()
            self.nonPlayerList.append(swordActor)
            return swordActor
        if randomNum == 4: 
            shield = genShield(coords, self.surface, self.player, self.map, self.surfaceMap)
            shieldActor = shield.generate()
            self.nonPlayerList.append(shieldActor)
            return shieldActor
        if randomNum == 5: 
            FireSpell = genFireballSpell(coords, self.surface, self.player, self.map, self.surfaceMap)
            FireballSpellActor = FireSpell.generate(camera=camera)
            self.nonPlayerList.append(FireballSpellActor)
            return FireballSpellActor

class genSword():
    
    def __init__(self,coords, surface, player, map, surfaceMap):
        self.coords = coords
        self.player = player
        self.map = map
        self.surface = surface
        self.itemActor = None
        self.surfaceMap = surfaceMap
    
    def generate(self):
        x,y = self.coords
        bonus = tcod.random_get_int(0, 1, 2)
        Sword = Equipment(self.player, bonus, 0, "rightHand")

        self.itemActor = Actor(x,y, constants.swordSprite, self.surface, self.map, [], "Sword",equipment= Sword, surfaceMap= self.surfaceMap)
        return self.itemActor
class genShield():
    
    def __init__(self,coords, surface, player, map, surfaceMap):
        self.coords = coords
        self.player = player
        self.map = map
        self.surface = surface
        self.itemActor = None
        self.surfaceMap = surfaceMap
    def generate(self):
        x,y = self.coords
        bonus = tcod.random_get_int(0, 1, 2)
        Sword = Equipment(self.player, 0, bonus, "leftHand")

        self.itemActor = Actor(x,y, constants.shieldSprite, self.surface, self.map, [], "Shield",equipment= Sword, surfaceMap = self.surfaceMap)
        return self.itemActor
#class for generating lightning spell w/ random damage
class genLighting():
    
    def __init__(self,coords, surface, player, map, surfaceMap):
        self.coords = coords
        self.player = player
        self.map = map
        self.surface = surface
        self.itemActor = None
        self.surfaceMap = surfaceMap
    
    def generate(self, camera):
        x,y = self.coords
        damage = tcod.random_get_int(0, 5, 7)
        LightningItem = Item(owner=None, player=self.player, healOrDamageVal= damage, camera=camera)

        self.itemActor = Actor(x,y, constants.lightningScrollSprite, self.surface, self.map, [], "Lighting Scroll", item = LightningItem, surfaceMap = self.surfaceMap)
        return self.itemActor
#class for confusion spell with random time and place
class genConfusionSpell():
    
    def __init__(self,coords, surface, player, map, surfaceMap):
        self.coords = coords
        self.player = player
        self.map = map
        self.surface = surface
        self.itemActor = None
        self.surfaceMap = surfaceMap
    def generate(self, camera):
        x,y = self.coords
        numTurns = tcod.random_get_int(0, 2, 4)
        ConfusionItem = Item(owner=None, player=self.player, healOrDamageVal= numTurns, camera= camera)

        self.itemActor = Actor(x,y, constants.confusionScrollSprite, self.surface, self.map, [], "Confusion Scroll", item = ConfusionItem, surfaceMap = self.surfaceMap)

        return self.itemActor

#CLASS FOR FIREBALL GENERATION
class genFireballSpell():

    def __init__(self,coords, surface, player, map, surfaceMap):
        self.coords = coords
        self.player = player
        self.map = map
        self.surface = surface
        self.itemActor = None
        self.surfaceMap = surfaceMap
    def generate(self, camera):
        x,y = self.coords
        damage = 5
        FireballItem = Item(owner=None, player=self.player, healOrDamageVal= damage, camera= camera)

        self.itemActor = Actor(x,y, constants.fireballSprite, self.surface, self.map, [], "Fireball Scroll", item = FireballItem, surfaceMap = self.surfaceMap)

        return self.itemActor

#class for a menu such as an inventory menu and a menu that pauses the game
class menu():
    def __init__(self,surface, player, nonPlayerList, surfaceMap, GameDrawer = None):
        self.surface = surface
        self.player = player
        self.nonPlayerList = nonPlayerList
        self.surfaceMap = surfaceMap
    def menuPause(self):

        windowsWidth = constants.cameraWidth
        windowsHeight = constants.cameraHeight
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
        windowsWidth = constants.cameraWidth
        windowsHeight = constants.cameraHeight
        inventorySurface = pygame.Surface((menuWidth,menuHeight))

        menuX = windowsWidth/2 - menuWidth/2
        menuY = windowsHeight/2-menuHeight/2
        printList = []
        for obj in self.player.container.inventory:
            printList.append(obj.displayName)

        while not menuClose:
            printList = [obj.displayName for obj in self.player.container.inventory]

            drawInv = drawText(inventorySurface, "", constants.colorWhite,
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
                                  if self.player.container.inventory[mouseLineSelection].item != None:
                                    menuClose = True
                                    useMessages = self.player.container.inventory[mouseLineSelection].item.use(self.nonPlayerList)
                                    if (isinstance(useMessages, list)):
                                        gameMessages = gameMessages + useMessages
                                    else:
                                        gameMessages.append(useMessages)
                                  else:
                                    menuClose = True
                                    useMessages = self.player.container.inventory[mouseLineSelection].equipment.use(self.nonPlayerList)
                                    if (isinstance(useMessages, list)):
                                        gameMessages = gameMessages + useMessages
                                    else:
                                        gameMessages.append(useMessages)
                              else:
                                  if self.player.container.inventory[mouseLineSelection].item != None:
                                     
                                    menuClose = True
                                    useMessages = self.player.container.inventory[mouseLineSelection].item.use(self.nonPlayerList)
                                    if (isinstance(useMessages, list)):
                                      
                                        gameMessages = gameMessages + useMessages
                                    else:
                                       
                                        gameMessages.append(useMessages)
                                  else:
                                      
                                    menuClose = True
                                    useMessages = self.player.container.inventory[mouseLineSelection].equipment.use(self.nonPlayerList)
                                    if (isinstance(useMessages, list)):
                                       
                                        gameMessages = gameMessages + useMessages
                                    else:
                                       
                                        gameMessages.append(useMessages)

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
    def __init__(self,surface, actor, map, nonPlayerList, surfaceMap, camera):
        self.surface = surface
        self.player = actor
        self.map = map
        self.nonPlayerList = nonPlayerList
        self.surfaceMap = surfaceMap
        self.camera = camera

    def menu_target_select(self, coordsOrigin = None, maxRange = None, penetrateWalls = True, mark = None, pierce_creature = True, radius = None):
        menuClose = False
        while not menuClose:
            #get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #get button clicks
            events_list = pygame.event.get()
            
            mapPixelX, mapPixelY = self.camera.winToMap((mouse_x, mouse_y))

            mapPixelX = mapPixelX
            mapPixelY = mapPixelY

            mouse_x_rel = mapPixelX//constants.cellWidth
            mouse_y_rel = mapPixelY//constants.cellHeight

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
                    if not pierce_creature and (self.map.map_objects_atcoords(x,y,self.nonPlayerList)):
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
            center = False
            if mark:
                center = True

            self.surface.fill(constants.colorBlack)
        
            self.surfaceMap.fill(constants.colorBlack)
                
            self.camera.update()

            self.map.drawToMap(self.surface)

            for obj in self.nonPlayerList:
                isVisble = tcod.map_is_in_fov(self.map.FOVMAP,obj.x, obj.y)
                if isVisble:
                    obj.draw()

        
            self.player.draw()

            #may need to change later for firespell and lighting spell
            for coords in validListTiles:
                x,y = coords
                if coords == validListTiles[-1]:
                    self.draw_tile_rect((x,y), mark, center)
                if radius:
                    area_effect = self.map.mapRadiusCreate(validListTiles[-1], radius)
                    for (x,y) in area_effect:
                        self.draw_tile_rect((x, y))
                else:
                     self.draw_tile_rect((x,y))
            self.surface.blit(self.surfaceMap, (0,0), self.camera.rectangle)
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
            
        self.surfaceMap.blit(new_surface,(new_x,new_y))

class Camera:

    def __init__(self, player):
        self.width = constants.cameraWidth
        self.height = constants.cameraHeight   
        self.x, self.y = (0,0)
        self.player = player
    
    @property
    def rectangle(self):

        posRect = pygame.Rect((0,0), (constants.cameraWidth, constants.cameraHeight))

        posRect.center = (self.x, self.y)

        return posRect
    
    @property
    def mapAddress(self):

        mapX = self.x//constants.cellWidth
        mapY = self.y//constants.cellHeight

        return (mapX, mapY)

    def update(self):
        
        targetX = (self.player.x * constants.cellWidth) + (constants.cellWidth/2)
        targetY = (self.player.y * constants.cellHeight) + (constants.cellHeight/2)
        
        distanceX, distanceY = self.mapDistance((targetX, targetY))

        self.x += int(distanceX)
        self.y += int(distanceY)

    def mapDistance(self, coords):

        newX, newY = coords
        distX = newX - self.x      
        distY = newY - self.y

        return (distX, distY)
    
    def camDist(self, coords):
        winX, winY = coords

        distX = winX - (self.width//2)
        distY = winY - (self.height//2)

        return (distX, distY)
    
    def winToMap(self, coords):

        targetX, targetY = coords

        #convert window coords to distance from camera
        camDX, camDY = self.camDist((targetX,targetY))

        mapPX = self.x + camDX
        mapPY = self.y + camDY

        return((mapPX, mapPY))

#baseclass for an actor. Actor being any object that can interact with a surface
class Actor:
    def __init__(self, x, y, sprite, surface, map, enemyList, objName,creature = None, ai = None, container = None, item = None, equipment = None, surfaceMap = None, stairs = None):
        self.x = x #map address
        self.y = y # map address
        self.objName = objName
        self.sprite = sprite
        self.surface = surface
        self.map = map
        self.ai = AI()
        self.enemyList = enemyList
        self.objName = objName
        self.surfaceMap = surfaceMap
       
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

        self.stairs = stairs
        if stairs:
            self.stairs.owner = self

            self.item = Item(self, None, None)

    def draw(self):
        self.surfaceMap.blit(self.sprite, ( self.x*constants.cellWidth, self.y*constants.cellHeight ))
    def move(self,dx,dy):
        tileIsWall = ((self.map.getCurrentMap())[self.x + dx][self.y + dy].blockPath == True)

        target = None

        gameMessage = []

        for enemy in self.enemyList:
            try:
                if (enemy.x == self.x + dx and enemy.y == self.y + dy):
                    target = enemy
                    break
            except AttributeError:
                if (enemy.itemActor.x == self.x + dx and enemy.itemActor.y == self.y + dy):
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
                    if target.creature:
                        gameMessage.append(target.displayName + " has health of " + str(target.creature.hp) + "/" + str(target.creature.maxHp))
                    else:
                        gameMessage.append(target.displayName +  " has died!")
                    if deathMessage:
                        gameMessage.append(deathMessage)
            else:
                gameMessage.append(self.displayName + " attacks " + target.displayName + " for " + str(self.creature.power) + " damage")
                deathMessage = self.creature.attack(target)
                if target.creature:
                    gameMessage.append(target.displayName + " has health of " + str(target.creature.hp) + "/" + str(target.creature.maxHp))
                else:
                    gameMessage.append(target.displayName +  " has died!")
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
        elif self.equipment:
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
        self.hp = min(self.maxHp, self.hp - damage + self.defense)
        
        if(self.hp <=0):
            return self.deathFunction()
            
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
        totalDefense = self.baseDef
        if self.owner.container:
            objectBonuses = [obj.equipment.defenseBonus for obj in self.owner.container.equippedItems]
            
            for bonus in objectBonuses:
                totalDefense += bonus
        return totalDefense
    
    def deathFunction(self):
        gameMessage = self.owner.displayName + " is dead!"
        self.owner.creature = None
        self.owner.ai = None
        return gameMessage

    def restoreHP(self, value):
        if(self.hp == self.maxHp):
            return "At full hp"
        else:
            self.hp = min(self.hp+value,self.maxHp)
            return "Consumed corpse to heal for " + str(value)

#class for items. Item class contains different methods depending on what spells are in the game
class Item:
    def __init__(self, owner, player, camera, nonPlayerList = None, weight = 0.0, volume = 0.0, healOrDamageVal = 0):
        self.weight = weight
        self.baseVolume = volume
        self.owner = owner
        self.container = None
        self.player = player
        self.value = healOrDamageVal
        self.nonPlayerList = nonPlayerList
        self.camera = camera
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
        useResult = None
        if self.owner.objName == "Lighting Scroll":
            useResult = self.lightingSpell(self.value, nonPlayerList)
        elif self.owner.objName == "Confusion Scroll":
            useResult = self.confusionSpell(self.value, nonPlayerList)
        elif self.owner.objName == "Fireball Scroll":
            useResult = self.FireballSpell(self.value, nonPlayerList)
        else:
            useResult = self.player.creature.restoreHP(self.value)
        if useResult != "Spell cancelled" and useResult != "At full hp":
            self.container.inventory.remove(self.owner)
        return useResult

    def lightingSpell(self, value, nonPlayerList):
        
        targetSelection = targetselect(self.player.surface, self.player, self.player.map, nonPlayerList, self.player.surfaceMap, self.camera)
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
        else:
            gameMessages = "Spell cancelled"
        return gameMessages
    
    def confusionSpell(self, numTurns, nonPlayerList):

        targetSelection = targetselect(self.player.surface, self.player, self.player.map, nonPlayerList, self.player.surfaceMap, self.camera)
        pointSelected = targetSelection.menu_target_select(mark="X")

        gameMessage = []
        if pointSelected:
            tileX, tileY = pointSelected
            targets = self.player.map.map_objects_atcoords(tileX, tileY, nonPlayerList)

            for target in targets:
                oldAI = target.ai

                target.ai = AIConfuse(oldAI, numTurns)
                target.ai.owner = target

                gameMessage = target.ai.owner.displayName + " eyes glaze over"
        else:
            gameMessage = "Spell cancelled"
        return gameMessage

    def FireballSpell(self, damage, nonPlayerList):
        
        targetSelections = targetselect(self.player.surface, self.player, self.player.map, nonPlayerList, self.player.surfaceMap, self.camera)
        pointSelected = targetSelections.menu_target_select((self.player.x, self.player.y),maxRange = 5, mark = "X", penetrateWalls= False, pierce_creature = False, radius= 1)
        gameMessages = []
        if pointSelected:
            tiles_to_dmg = self.player.map.mapRadiusCreate(pointSelected, 1)
            for (x, y) in tiles_to_dmg:
                creatures_to_damage = self.player.map.map_objects_atcoords(x, y, nonPlayerList)

                for enemy in creatures_to_damage:
                    enemy.creature.takeDamage(damage)
                    if enemy is not self.player:
                        gameMessages.append("Fireball spell did " + str(damage) + " damage to " + enemy.displayName)
        else:
            gameMessages = "Spell cancelled"
        return gameMessages

#class to handle stairs
class Stairs:
    def __init__(self, downwards = True):
        self.downwards = downwards

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
                gameMessages = ["Picking up equipment"]
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

        allEquippedItems = []
        if self.player:
            allEquippedItems = self.player.container.equippedItems 

        for item in allEquippedItems:
            if (item.equipment.slot and item.equipment.slot == self.slot):
                return "Equipment Slot is Occupied! Can't equip item"

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
        equippedItems = [obj for obj in self.inventory if obj.equipment != None and obj.equipment.equipped]
        return equippedItems

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
    def __init__(self,surface, actor, map, nonPlayerList, clock, messages, surfaceMap, camera):
        self.surface = surface
        self.player = actor
        self.map = map
        self.nonPlayerList = nonPlayerList
        self.clock = clock
        self.gameMessages = messages
        self.drawTextObject = drawText(self.surface,"default", constants.colorWhite,(0,0))
        self.surfaceMap = surfaceMap
        self.camera = camera

    def drawGame(self):

        self.surface.fill(constants.colorBlack)
        
        self.surfaceMap.fill(constants.colorBlack)
        displayRect = pygame.Rect((50,50),(constants.cameraWidth, constants.cameraHeight) )
        
        self.camera.update()

        self.map.drawToMap(self.surface)

        for obj in self.nonPlayerList:
            isVisble = tcod.map_is_in_fov(self.map.FOVMAP,obj.x, obj.y)
            if isVisble:
                obj.draw()

        
        self.player.draw()
        self.surface.blit(self.surfaceMap, (0,0), self.camera.rectangle)

        self.drawMessages()

        
    def drawMessages(self):
        toDraw = []
        if len(self.gameMessages) <= constants.numMessages:
            toDraw = self.gameMessages
        else:
            toDraw = self.gameMessages[-constants.numMessages:]

        startY = constants.cameraHeight - (constants.numMessages * self.drawTextObject.textHeight()) -10

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

#class for a singular rectangle room
class RectRoom:
    def __init__(self,coords, size):
        self.x, self.y = coords
        self.width, self.height = size
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height
    
    #method to get center coords of the room
    def center(self):
        centerX = (self.x2 + self.x)//2
        centerY = (self.y2 + self.y)//2
        return ((centerX, centerY))
    
    #method to check if object intercepts another one
    #returns true if two objects intersect
    def intersect(self, other):

        objectsIntersect = (self.x <= other.x2 and self.x2 >= other.x and 
                             self.y <= other.y2 and self.y2 >= other.y)
        
        return objectsIntersect

#class to handle the game's map
class Map:
    def __init__(self, fovCalculate, nonPlayerList, surface, player= None, surfaceMap = None, camera = None):
        # constructor uses tunnelling algorithm to create rooms
        self.fovCalculate = fovCalculate
        self.player = player
        self.map = [[ tileStrucutre(True) for y in range(0,constants.mapWidth)] for x in range(0,constants.mapHeight)]
        self.surfaceMap = surfaceMap
        self.listOfRooms = []

        self.camera = camera

        for i in range(0, constants.mapMaxNumRooms):
            
            w = tcod.random_get_int(0, constants.roomMinWidth, constants.roomMaxWidth)
            h = tcod.random_get_int(0, constants.roomMinHeight, constants.roomMaxHeight)
            
            x = tcod.random_get_int(0, 2, constants.mapWidth - w -2)
            y = tcod.random_get_int(0, 2, constants.mapHeight - h -2)

            newRoom = RectRoom((x,y), (w,h))

            failed = False

            for otherRoom in self.listOfRooms:
                if newRoom.intersect(otherRoom):
                    failed = True
                    break
           
            if not failed:
                self.createRoom(newRoom)
                currentCenter = newRoom.center()

                if (len(self.listOfRooms) != 0):
                  previousCenter = self.listOfRooms[-1].center()

                  # dig tunnels
                  self.createTunnels(currentCenter, previousCenter)
                self.listOfRooms.append(newRoom)
        self.makeFOV()

    def createTunnels(self, coords1, coords2):
        #change var name later
        coinFlip = (tcod.random_get_int(0,0,1) ==1)

        x1, y1 = coords1
        x2, y2 = coords2
        if coinFlip:
            for x in range(min(x1,x2), max(x1, x2) + 1):
                self.map[x][y1].blockPath = False
            for y in range(min(y1,y2), max(y1, y2) + 1):
                self.map[x2][y].blockPath = False
        else:
            for y in range(min(y1,y2), max(y1, y2) + 1):
                self.map[x1][y].blockPath = False
            for x in range(min(x1,x2), max(x1, x2) + 1):
                self.map[x][y2].blockPath = False

    def createRoom(self, newRoom):
        for x in range(newRoom.x, newRoom.x2):
            for y in range(newRoom.y, newRoom.y2):
                self.map[x][y].blockPath = False
               
    def getCurrentMap(self):
        return self.map
    
    def drawToMap(self, surface):

        camX, camY = self.camera.mapAddress

        displayMapW = constants.cameraWidth//constants.cellWidth
        displayMapH = constants.cameraHeight//constants.cellHeight

        renderWMax  = camX + (displayMapW//2)
        renderWMin  = camX - (displayMapW//2)
        
        renderHMax  = camY + (displayMapH//2)
        renderHMin  = camY - (displayMapH//2)

        if renderHMin < 0:
            renderHMin = 0
        if renderWMin < 0:
            renderWMin = 0
        if renderWMax  > constants.mapWidth:
            renderWMax = constants.mapWidth
        if renderHMax > constants.mapHeight:
            renderHMax = constants.mapHeight 

        for x in range(renderWMin,renderWMax):
            for y in range(renderHMin,renderHMax):

                isVisible = tcod.map_is_in_fov(self.FOVMAP,x,y)
               
                if isVisible:
                    self.map[x][y].explored = True
                    if self.map[x][y].blockPath == True:
                        self.surfaceMap.blit(constants.wallSprite, ( x*constants.cellWidth, y*constants.cellHeight))
                    else: 
                        self.surfaceMap.blit(constants.floorSprite, ( x*constants.cellWidth, y*constants.cellHeight))
                elif(self.map[x][y].explored):
                    if self.map[x][y].blockPath == True:
                        self.surfaceMap.blit(constants.wallExploredSprite, ( x*constants.cellWidth, y*constants.cellHeight))
                    else: 
                        self.surfaceMap.blit(constants.floorExploredSprite, ( x*constants.cellWidth, y*constants.cellHeight))
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

    def mapRadiusCreate(self, coords, radius):
        center_x, center_y = coords

        tile_list = []

        start_x = (center_x - radius)
        end_x = (center_x + radius + 1)

        start_y = (center_y - radius)
        end_y = (center_y + radius + 1)
        for x in range(start_x,end_x):
            for y in range (start_y,end_y):
                tile_list.append((x,y))
        return tile_list

#Main Game class with main game loop
class GameRunner:
    def __init__(self, map = None):
        pygame.init()
        pygame.key.set_repeat(200, 70)
        self.clock = pygame.time.Clock()
        self.surfaceMain = pygame.display.set_mode( (constants.cameraWidth, constants.cameraHeight) )
        
        self.surfaceMap = pygame.Surface((constants.mapWidth * constants.cellWidth, constants.mapHeight * constants.cellHeight))

        self.fovCalculate = True
        self.gameMessages = []
        self.nonPlayerList = []
        self.camera = Camera(None)

        if map:
            self.map = map
        else:
            self.map = Map(self.fovCalculate, self.nonPlayerList, self.surfaceMain, surfaceMap=self.surfaceMap, camera= self.camera)
        self.currentRooms = self.map.listOfRooms

        self.playerGen = genPlayer(self.surfaceMain, self.map, self.nonPlayerList, self.surfaceMap)
        self.player = self.playerGen.generate(self.map.listOfRooms[0].center())

        self.camera.player = self.player

        self.GameDrawer = GameDraw(self.surfaceMain,self.player, self.map, self.nonPlayerList, self.clock, self.gameMessages, self.surfaceMap, self.camera)
        
        self.menu = menu(self.surfaceMain, self.player, self.nonPlayerList, self.surfaceMap, self.GameDrawer)

        self.map.player = self.player

        self.placeObjects()

    #method to place objects on map, may be moved to a different class later
    def placeObjects(self):

        for i, room in enumerate(self.currentRooms):

            if i ==0:
                self.player.x , self.player.y = room.center()
            elif i == len(self.currentRooms)-1:
                newStairs = genStairs(self.surfaceMain, self.map, self.nonPlayerList, self.surfaceMap)
                newStairs.genStairs(room.center(), True)
            else:
                if i !=0:
                    x = tcod.random_get_int(0, room.x+1, room.x2 - 1)
                    y = tcod.random_get_int(0, room.y+1, room.y2 - 1)

                    newEnemy = genEnemies(self.surfaceMain, self.player, self.map, self.nonPlayerList, self.surfaceMap)
                    newEnemy.genEnemy((x,y))
    
                x = tcod.random_get_int(0, room.x+1, room.x2 - 1)
                y = tcod.random_get_int(0, room.y+1, room.y2 - 1)

                if (x,y) is not (self.player.x , self.player.y): 

                    newItem = randomItemGeneration(self.surfaceMain, self.player, self.map, self.nonPlayerList, self.surfaceMap)
                    newItem.genItem((x,y), self.camera)


    def game_main_loop(self):
 
        gameQuitStatus = False
        TransNext = False
        while not gameQuitStatus:
            playerAction = "no-action"
            playerAction = self.handleKeys()
            self.map.calculateFOV()
            if playerAction == "QUIT":
                gameQuitStatus = True
                pygame.quit()
                exit()

            if playerAction != "no-action":
                for enemy in self.nonPlayerList:
                    if( hasattr(enemy, "ai") and enemy.ai != None):
                        gameMessage = enemy.getai().takeTurn()
                        if gameMessage != []:
                            for message in gameMessage:
                                self.gameMessagesAppend(message,constants.colorWhite)
            self.GameDrawer.drawGame()
            self.clock.tick(constants.gameFPS)
            pygame.display.flip()

            if playerAction == "Transition Next":
                gameQuitStatus = True
                TransNext = True
        
        return (TransNext, self.map)

    def gameMessagesAppend(self, gameMessage, msgColor):
        self.gameMessages.append((gameMessage,msgColor))
     
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

                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    for obj in self.map.map_objects_atcoords(self.player.x, self.player.y, self.nonPlayerList):
                        if obj.displayName == "Stairs":
                            return "Transition Next"
               
        return "no-action"        

#class to start the game. AKin to TicTacToeApplication in Assignment 1 of Software Design
class MainGameApplication:
    def __init__(self):
        self.NewGame = GameRunner()
        self.prevMaps = []

    def RunGame(self):
        mapTransitionNext = True
        while(True):
            if(mapTransitionNext == True):
                self.NewGame = GameRunner()
                mapTransitionNext, prevMap = self.NewGame.game_main_loop()
                self.prevMaps.append(prevMap)

#because python doesn't have a main function like Java or C++
if __name__ == '__main__':
    newGame = MainGameApplication()
    newGame.RunGame()
