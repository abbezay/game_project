# game_project
# Name: To Be Determined

This is a simple platformer game. Land on top of enemies to defeat them and 
avoid their sides. Find and collect the key and progress to the next level 
by reaching the door. Beat all five levels and score the highest points!  
Hearts can be picked up to restore health.

How to play:  
Run main.py from game folder.  

Movement:  
A - Move left.  
D - Move right.  
W - Jump.  


# Problems encountered during development
## Prototypes
* Complicated if/else block in prototypes simplified to for-loops.
* Tilesets and spritesheets of varying sizes and quality exchanged for
self-made assets.
* Background sizes difficult to align with various level sizes. Ideas for
fix include repeating background patterns and centering second
background layer with player starting position.
* Blank levels were quite messy to create freehand, so a tool was created
to automate the process. Still no tool to randomize level interior.
* Initial for loop to determine collision was replaced with collidelist.
* Collision detection lead to stuttering player model. Solution was to
introduce a test copy to see if any collision was made before moving 
the player.
## Inititial Release
* Classes were split into modules to make the code easier to work with.
* Master and subclasses were collected back into a collected module, see enemy.py and object.py.
* Player class held separate status flags in a dictionary for each state, 
which were simplified into a state string.
* Player bound attributes and methods were moved from Engine to Player class.
* TODO :: Simplify collision_checker as it contains many if/else statements. SOLVED :: Split method from Player class into self-contained in each enemy and object class.
Suggestion, split into class methods for each instance that handles collision differently.
* Attributes now need to be shared down to Player and Enemy classes to work properly.
* Split enemies into separate classes for each type.
* Complicated methods are being simplified to be more easily readable.
* Flying enemies are set to the side of their spawn point.
* Player can sometimes accidentally kill enemy when taking damage and being knocked up.
* BUG :: When restarting after game over, the levels aren't reset. SOLVED :: Restarting from game over now resets all necessary attributes.
* BUG :: Stalagtite doodads are not rendered. SOLVED :: confused x and y coordinates.
* BUG :: Level is finished when picking up the key if door is to the left. SOLVED :: self.hitbox.width = self.hitbox[0] * 2
self.hitbox.height = self.hitbox[1] * 2
was causing the hitbox to be multiplied by the coordinates, reaching to the right. Changed lines to multiply by self.hitbox.width / height instead.
* Moved music.load() and music.play() out of main.py and into Engine.loop() to allow for multiple music tracks.
* ISSUE :: Player can trigger the door and walk away, potentially lose on both time and to enemy collision during music.

# Project criteria
# E-Level
## Game
Game Window         DONE 4/5/26  
Main While Loop     DONE 4/5/26  
Event Handling      DONE 4/5/26  
Window Updates      DONE 4/5/26  
## Player
Draw Player         DONE 4/5/26  
Move Player         DONE 4/5/26  
Limit Play Area     DONE 4/5/26  
## Code
Two Classes         DONE 4/5/26  
Methods Used        DONE 4/5/26  
Two Unittests       DONE 9/5/26    
## Documentation
Class Diagram       DONE 9/5/26    
Comments            DONE 4/5/26     Note: Can be made more explicit.  
Robustness          TODO(?)         Note: No error handling, but game doesn't crash.  
## GitHub
Repository Created  DONE 21/4/26  
Collaborators Added DONE 21/4/26  

# C-Level
## Features
Background images   DONE 9/5/26    
Sound effects       DONE 4/5/26  
Music               DONE 4/5/26  
Main Menu           DONE 8/5/26  
Game Over Screen    DONE 8/5/26  
Multiple levels (5) DONE 9/5/26
PowerUp (heart)     DONE 5/5/26
Make it look good   TODO
Make it fun         TODO
## Game
Scoring system      DONE 7/5/26  
## Enemy
Create Enemy        DONE 4/5/26  
Move Enemy          DONE 4/5/26  
Enemy Collision     DONE 4/5/26  
Player take damage  DONE 5/5/26  
Enemy take damage   DONE 4/5/26  
## Code
Inheritance         DONE 4/5/26  
Dictionaries        DONE 4/5/26  
Three Unittests     DONE 9/5/26    
## Documentation
Class Diagram +     DONE 9/5/26    
Code Readability    TODO            Note: Too dense and complex in places.


# A-Level
## Game
Music Playing       DONE 4/5/26  
Sound Effects       DONE 4/5/26  
Game Menu           DONE 7/5/26  
Game Over Condition DONE 7/5/26  
Game Over Screen    DONE 7/5/26  
Victory Condition   DONE 5/5/26  
UI (Health, Time)   DONE 5/5/26  
## Code
Polymorphism        DONE 4/5/26  
## Documentation
Class Diagram ++    TODO   
Algorithm Chart     TODO  
Troubleshooting     TODO  
Evaluation          TODO  
Reflection          TODO  
## GitHub
Final Version       TODO  

# Self-Evaluation
The game has good menus and multiple varied levels, filled with multiple enemy types and an objective. The player

# Assets used
## Graphics
Spritesheets and tileset created with GIMP. 
Menu, game over and victory backgrounds generated with ChatGPT. 

## Audio
Royalty-free music and sounds sourced from Pixabay and edited with Audacity for timing and clarity.  

## Music
main_menu.mp3 - by kissan4 https://pixabay.com/music/video-games-glitch-mode-369215/  
background.mp3 - by Lofiewme https://pixabay.com/music/video-games-pixel-fantasia-355123/   
game_over_win.mp3 - by AberrantRealities https://pixabay.com/music/upbeat-mixer-fixer-287666/  
game_over_loss.mp3 - by Kuzu420 https://pixabay.com/music/video-games-game-over-2-short-music-351102/  

## Sound Effects
jump.wav - by freesound_community https://pixabay.com/sound-effects/film-special-effects-sfx-jump-07-80241/  
player_hit.wav - by freesound_community https://pixabay.com/sound-effects/musical-hurt-c-08-102842/  
death.wav - by freesound_community https://pixabay.com/sound-effects/film-special-effects-videogame-death-sound-43894/  
victory.wav - by freesound_community https://pixabay.com/sound-effects/musical-winsquare-6993/  
slime_hit.wav - by freesound_community https://pixabay.com/sound-effects/film-special-effects-various-mushy-impacts-or-wet-splats-70685/  
powerup.wav - by freesound_community https://pixabay.com/sound-effects/film-special-effects-8-bit-powerup-6768/  
land.wav - by Abdalrahman_bm https://pixabay.com/sound-effects/film-special-effects-8-bit-gravel-footsteps-1-408582/  

## Fonts
press_start_2p.ttf - by CodeMan38 https://fonts.google.com/specimen/Press+Start+2P  