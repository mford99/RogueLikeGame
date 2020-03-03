#third party libraries
import pygame
import tcod as libtcodpy

#game files
import constants

#class for an individual tile
class tileStrucutre:
    def __init__(self, blockPath):
        self.blockPath = blockPath

#class to update the game's UI by updating the screen
class GameDraw:
    def __init__(self,surface):
        self.surface = surface
    def draw_game(self):

        self.surface.fill(constants.colorDefaultBG)

        gameMap = Map()
        gameMap.drawToMap(self.surface)

        self.surface.blit(constants.playerSprite, ( 200, 200 ))
    
        pygame.display.flip()

#class to handle the game's map and drawing to said map
class Map:
    def __init__(self):
        self.Map = [[ tileStrucutre(False) for y in range(0,constants.mapWidth)] for x in range(0,constants.mapHeight)]

        self.Map[10][10].blockPath = True
        self.Map[10][15].blockPath = True
    
    def getCurrentMap(self):
        return self.Map
    
    def drawToMap(self, surface):
        for x in range(0,constants.mapWidth):
            for y in range(0,constants.mapHeight):
                if self.Map[x][y].blockPath == True:
                    surface.blit(constants.wallSprite, ( x*constants.cellWidth, y*constants.cellHeight))
                else: 
                    surface.blit(constants.floorSprite, ( x*constants.cellWidth, y*constants.cellHeight))

#Main Game class with main game loop
class GameRunner:
    def __init__(self):
        pygame.init()
        self.surfaceMain = pygame.display.set_mode( (constants.gameWidth,constants.gameHeight) )
        self.gameMap = Map()
    
    def game_main_loop(self):

        self.gameQuitStatus = False
        while not self.gameQuitStatus:
        
            GameDrawer = GameDraw(self.surfaceMain)
            GameDrawer.draw_game()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.gameQuitStatus = True

        pygame.quit()
        exit()

#class to start the game. AKin to TicTacToeApplication in Assignment 1 of Software Design
class MainGameApplication:
    def RunGame(self):
        self.NewGame = GameRunner()
        self.NewGame.game_main_loop()

if __name__ == '__main__':
    MainGame = MainGameApplication()
    MainGame.RunGame()