import pygame

pygame.init()

#Game Sizes
gameWidth = 800
gameHeight = 600
cellWidth = 32
cellHeight = 32

#MapTileSizes
mapWidth = 30
mapHeight = 30

#Colour Definitions
colorBlack = (0,0,0)
colorWhite = (255,255,255)
colorGrey = (100,100,100)

#Game Colours
colorDefaultBG = colorGrey

#Sprites
playerSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/mainCharacter.png')
wallSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/wall.png')
floorSprite = pygame.image.load('C:/ENGI5895SoftwareDesign/Project/Sprites/Characters/floor.jpg')