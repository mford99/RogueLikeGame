import pygame
import tcod
pygame.init()

#Game Sizes
gameWidth = 800
gameHeight = 600
cellWidth = 32
cellHeight = 32

#MapTileSizes
mapWidth = 20
mapHeight = 20

#Colour Definitions
colorBlack = (0,0,0)
colorWhite = (255,255,255)
colorGrey = (100,100,100)
colorRed = (255,0,0)

#Game Colours
colorDefaultBG = colorGrey

#Sprites
mainEnemySprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/mainEnemy.png')
playerSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/mainCharacter1.png')
wallSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/wall.jpg')
wallExploredSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/wallunseen.png')
floorSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/floor.jpg')
floorExploredSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/floorExplored.png')

#FOV Settings
FOVALGO = tcod.FOV_BASIC
FOVLIGHTWALLS = True
torchRadius = 10

#Fonts
fontDebugMessage = pygame.font.Font('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/joystix.ttf', 16)
fontMessageText = pygame.font.Font('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/joystix.ttf', 12)
#FPS
gameFPS = 60

#Messages
numMessages = 4