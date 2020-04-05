# RogueLikeGame
Rogue-like game made in python

This is a roguelike, dungeon crawling top-down game made with pygame and small amounts of the tcod library. The instructions for playing and running the game are below:




								/**************************************************************
								*		Instructions for Running and Using PyGame The Game
								*
								*				By: Marcus Ford - 201712775
								*					Bowen Wang - 201521242
								*
								****************************************************************/

	Step 1:
			Install Python version 3.5.8 or above, if not already installed. To check for instillation, simply run 'python'
			on the command window to see if your OS recognizies the command.
			This can be down at the following link: https://www.python.org/downloads/	
			Follow the instructions on the website to download Python. Make sure you add python to the PATH on Windows.
	
	Step 2: 
			Install pip, if not already installed. To check for instillation, simply type 'pip' into the command windows/
			and see if your OS recognizies the command or not.
			The instructions to download pip can be found at: https://www.liquidweb.com/kb/install-pip-windows/
			
	Step 3:
			Download and install the necessary python libraries. They are pygame, the main game engine, and tcod which is used for some mathematical
			calculations. To download and install, simply run the following commands:
			
				pip install pygame	
				pip install tcod
				
	Step 4:
			Make sure the files are in the right place. There are two main files, MainGame.py and constants.py along with 
			several image files that the game uses. Make sure that the MainGame.py file and the constants.py file are
			in the same directory. Once this is done, add a new directory where the MainGame.py and constants.py are and call it
			'Sprites'. Then, inside this Directory, make a new directory called 'Characters'. This is where every sprite the game uses
			is stored. Make sure every sprite is in this folder or the game will not work. DO not rename the sprites either.
	
	Step 5: Compile and run the game. To compile and run the game, first cd into the directory which contains MainGame.py and constants.py.
			Then, run the following command:
					
					python MainGame.py
		
			That's it! The game has officially started and you can enjoy PyGame: The Game!

