# game_project
# Name TBD

This is a simple platformer game. Land on top of enemies to defeat them and 
avoid their sides, find and collect the key to progress to the next level 
through the door. Hearts can be picked up to restore health.

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
* Master and subclasses were collected back into a collected module.
* Player bound attributes and methods were moved from Engine to Player class.
* TODO :: Simplify collision_checker as it contains many if/else statements. 
Suggestion, split into class methods for each instance that handles collision differently.
* Attributes now need to be shared down to Player and Enemy classes to work properly.
* Split enemies into separate classes for each type.
* Complicated methods are being simplified to be more easily readable.


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
Two Unittests       TODO  
## Documentation
Class Diagram       TODO  
Comments            DONE 4/5/26     Note: Can be made more explicit.  
Robustness          TODO            Note: No error handling, but game doesn't crash.  
## GitHub
Repository Created  DONE 21/4/26  
Collaborators Added DONE 21/4/26  

# C-Level
## Features
1                   TODO  
2                   TODO  
3                   TODO  
## Game
Scoring system      TODO  
## Enemy
Create Enemy        DONE 4/5/26  
Move Enemy          DONE 4/5/26  
Enemy Collision     DONE 4/5/26  
Player take damage  TODO  
Enemy take damage   DONE 4/5/26  
## Code
Inheritance         DONE 4/5/26  
Dictionaries        DONE 4/5/26  
Three Unittests     TODO  
## Documentation
Class Diagram +     TODO  
Code Readability    TODO            Note: Quite dense and complex, especially movement blocks.  

# A-Level
## Game
Music Playing       DONE 4/5/26  
Sound Effects       DONE 4/5/26  
Game Menu           TODO  
Game Over Condition TODO  
Game Over Screen    TODO  
Victory Condition   TODO  
UI (Health, Time)   TODO  
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



# Assets used
## Graphics
Spritesheets and tileset created with GIMP.  

## Audio
Royalty-free music and sounds sourced from Pixabay and edited with Audacity for timing and clarity.  

## Music
background.mp3 - by MFCC https://pixabay.com/music/upbeat-retro-arcade-game-music-297305/  

## Sound Effects
jump.wav - by freesound_community https://pixabay.com/sound-effects/film-special-effects-sfx-jump-07-80241/  
player_hit.wav - by freesound_community https://pixabay.com/sound-effects/musical-hurt-c-08-102842/  
death.wav - by freesound_community https://pixabay.com/sound-effects/film-special-effects-videogame-death-sound-43894/  
victory.wav - by freesound_community https://pixabay.com/sound-effects/musical-winsquare-6993/  
slime_hit.wav - by freesound_community https://pixabay.com/sound-effects/film-special-effects-various-mushy-impacts-or-wet-splats-70685/  
powerup.wav - by freesound_community https://pixabay.com/sound-effects/film-special-effects-8-bit-powerup-6768/  
land.wav - by Abdalrahman_bm https://pixabay.com/sound-effects/film-special-effects-8-bit-gravel-footsteps-1-408582/  