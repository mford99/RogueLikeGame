import pygame
import tcod
pygame.init()

#Game Sizes
gameWidth = 800
gameHeight = 600
cellWidth = 32
cellHeight = 32

#MapTileSizes
mapWidth = 40
mapHeight = 20
mapMaxNumRooms = 10

#Room Limiations
roomMaxHeight = 7
roomMinHeight = 3

roomMaxWidth = 5
roomMinWidth = 3

# #Colour Definitions
colorBlack = (0,0,0)
colorWhite = (255,255,255)
colorGrey = (100,100,100)
colorRed = (255,0,0)
colorGreen = (0,255,0)

# #Game Colours
colorDefaultBG = colorGrey

# #Sprites
mainEnemySprite = pygame.transform.scale(pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/mainEnemy.png'), (cellWidth, cellHeight))
rareCobraSprite = pygame.transform.scale(pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/cobra.png'), (cellWidth, cellHeight))
playerSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/mainCharacter1.png')
wallSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/wall.jpg')
wallExploredSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/wallunseen.png')
floorSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/floor.jpg')
floorExploredSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/floorExplored.png')

# #FOV Settings
FOVALGO = tcod.FOV_BASIC
FOVLIGHTWALLS = True
torchRadius = 10

# #Fonts
fontDebugMessage = pygame.font.Font('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/joystix.ttf', 16)
fontMessageText = pygame.font.Font('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/joystix.ttf', 12)
fontCursorText = pygame.font.Font('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/joystix.ttf', cellHeight)
# #FPS
gameFPS = 60

# #Messages
numMessages = 4

# #Equipment/Items
swordSprite = pygame.transform.scale(pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/Sword.png'), (cellWidth,cellHeight))
shieldSprite = pygame.transform.scale(pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/shield.png'), (cellWidth, cellHeight))
lightningScrollSprite = pygame.transform.scale(pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/lightningScroll.png'), (cellWidth, cellHeight))
confusionScrollSprite = pygame.transform.scale(pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/confusionScroll.png'), (cellWidth, cellHeight))
fireballSprite = pygame.transform.scale(pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/fireball.png'), (cellWidth, cellHeight))