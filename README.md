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
			Download and install the necessary python libraries. They are pygame, the main game engine, and tcod which is 				used for some mathematical calculations. To download and install, simply run the following commands:
			
				pip install pygame	
				pip install tcod
			
			NOTE: If on windows, tcod requires Visual c++ runtime 2015 or later which can be downloaded at 			                               https://support.microsoft.com/en-ca/help/2977003/the-latest-supported-visual-c-downloads
			      
			      If on Linux/Ubuntu, tcod requires  libsdl2 (2.0.5+) and libomp5 to run.The instructions to download 	                               libsdl2 can be found at https://zoomadmin.com/HowToInstall/UbuntuPackage/libsdl2-dev
			      The instructions to download libomp5 are at https://www.howtoinstall.co/en/ubuntu/xenial/libomp5
					
				
	Step 4:
			Make sure the files are in the right place. There are two main files, MainGame.py and constants.py along with 
			several image files that the game uses. Make sure that the MainGame.py file and the constants.py file are
			in the same directory. Once this is done, add a new directory where the MainGame.py and constants.py are and 				call it 'Sprites'. Then, inside this Directory, make a new directory called 'Characters'. This is where every  				sprite the game uses are stored. Make sure every sprite is in this folder or the game will not work. Do not 				rename the sprites either.
	
	Step 5: Compile and run the game. To compile and run the game, first cd into the directory which contains MainGame.py and constants.py.
			Then, run the following command:
					
					python MainGame.py
		
			That's it! The game has officially started and you can enjoy PyGame: The Game!
			
	
	
					/**************************************************************
					*				Notes About PyGame The Game
					*
					*				By: Marcus Ford - 201712775
					*				    Bowen Wang - 201521242
					*
					****************************************************************/
	
	
			To play the game, use the up, down, left, and right arrow keys to move the player character, the snake.
			
			Holding the keys down will cause contionous key inputs. I.e. if the user wants to continously move left they can                         hold the left arrow key instead of constantly hitting the left key. 
			
			The goal of the game is to beat five floors of the dungeon without dying.
			
			Each enemy killed can be picked up.
			
			In order to pick up all items on a particular tile, hit the G key. The P key pauses the game. The I key opens 	                         the inventory where the user can then click on an item to use it. If the item is a corpse, the user will eat it                         to restoreHP. 
			
			If the item is a spell, the targeting menu for the spell will close the inventory and allow the 	 			 	user to cast the spell. 
			
			Finally, if the item selected is a sword or shield it will be equipped. When finding the 			  			  stairs to the next floor,
			
			Hitting LSHIFT or RSHIFT on them will take the user to the next floor.
			Finally, when selecting a target for a spell, the user can hit Q at any time to cancel the spell and place it
			back into the player's inventory.

