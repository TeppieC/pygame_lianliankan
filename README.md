This is a old project finished in Spring 2015. This game is for cmput275 final project.  
一个简单的连连看游戏，图片素材来源于网络，背景音乐为Joe Hisaishi的summer，使用pygame库  

Rules of the game
------------------
During the limited time, player has to find two identical pictures from the game surface and connecting them by clicking on both of them successively. Then the two pictures will be erased from the screen. The connecting line from one picture to another should have no more than a certain number of turns. The player will be asked to determine the max number of turns at the begining of the game by themselves.
Game will end if player has erased all pictures or time runs up.


General notes for the files and their usage:
--------------------------------------------
1. The game is run by typing "python3 main.py" on the terminal.
Player has to enter a number larger than or equal to 2 and then press [Enter] to start the game at the mode-select window.

2. modegui.py consists of a class called ModeGUI.
---Instance of this class will create a window that allows the player to type in the number of turns that is allowed in the game.
---Player has to enter a number larger than 1, and press [Enter] to proceed.
---Then the mode gui window will be closed and display the game gui window

3. gui.py consists of a class called GUI
---Instance of this class will create a window that displays and handles the functionality of the whole game. 
---The window will be closed when player successfully cleared all the pictures or time runs up.

4. tile.py consists of a class called Tile
---Objects of this class are used in gui.py.
---Each picture and blank tile in game gui is an instance of this class.

5. asset folder contains all pictures which will be displayed in the game


Layouts for each main function in the game:
---------------------------------------------
(Lxxx - Lxxx) During linexxx to linexxx in gui.py

1. Determine if two pictures are connectable and Draw connecting lines
	(L890 - L1126) Determine connectable
		
		search_left_side_tiles; 
		search_right_side_tiles;
		search_top_side_tiles; 
		search_bottom_side_tiles;
		  
		reachable; 
		connectable; 
		is_pair_to

	(L1127 - L1209) Draw connecting lines

		trace_back_items; 
		draw_lines; 
		draw_connect_lines
		

2. Hint power-up and search for hints
	(L429 - L798)
		display_pup_hint; 
		hint_highlight; 
		hint_dehighlight;
		press_pup_hint; 

		left_side_tiles; 
		right_side_tiles;
		top_side_tiles;	
		bottom_side_tiles; 

		hint_left_side_tiles;
		hint_right_side_tiles; 
		hint_top_side_tiles;
		hint_bottom_side_tiles; 

		search_zero_turn;
		search_one_turn; 
		search_two_turns; 
		search_paired_hints;

3. Shuffle power-up
	(L799 - L871)
		display_pup_shuf; 
		press_pup_shuf; 
		shuffle_pics

4. Automatic shuffle check
	(L872 - L888)
		check_whether_shuffle


Key function and its time complexity
------------------------------------
For checking if the two pictures are connectable, GUI.connectable() function takes O(r*c) where r is the number of rows and c is the number of columns in the game gui surface.
NOTE: For the efficiency of this function, I discussed with Zach during the demo, and we have reached O(r*c) at the end. Though it would be significantly clear if I choose to use two more attributes(hor, ver) when searching the routes as suggested by Zach.


Special notifications for gui.py:
--------------------------------
1. RECTs
We created several pygame.Rect for displaying each kind of objects in the game surface.

2. RND_PAIRS FUNCTION
Due to the game's rules, number of each kind of pictures has to be even. Therefore, a function called rnd_pairs() is created outside GUI class, in order to generate even number of pairs of pictures.

3. TILE & PIC
To clarify the difference between terms "tile" and "pic" used in the game, "tile" stands for the Tile objects in the game surface, including all pictures and blank tiles which has no pictures on them. While "pic" stands for those tiles which potentially has pictures on them.

4. ON_CLICK FUNCTION
The function on_click() would handles the functionality of the game when mouse is pressed in the game gui window.

5. AUTOMATIC-SHUFFLE
There will be some circumstances that there is no available picture pairs connectable remaining in the game, the game will check for such situation and shuffle the pictures automatically.

6. GUI.HIGHLIGHTED_ITEMS
The highlighted_items attribute of GUI class is a list that containing at most two Tile objects. When player select one picture, it will be appended to the list. The two items in this list won't be the same. Once the list is in length of 2, the game will check if the two pictures are the same and can be reached within certain turns.
Pictures in this list would be highlighted with orange circles.

7. SEARCH FOR HINT
You have to first select a picture and then press the hint power-up button to search for hints.
In the game, hint power-up is used after selecting a picture. The game will provide a same picture within making 2 turns to reach from the selected picture.
