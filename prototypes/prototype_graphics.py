import pygame
# Use this path if file is run from parent folder.
path = './prototypes/'
# Use this path if file is run from current folder.
# path = ''

"""
TODO :: Add additional documentation to clarify aspects of code that
otherwise needs to be explained in person.
"""

class Engine:
    """Parameters to run pygame."""
    def __init__(self) -> None:
        self.running = True
        self.res_480p = self.width, self.height = 640, 480
        # self.res_720p = self.width, self.height = 1280, 720
        # self.res_1080p = self.width, self.height = 1920, 1080
        # self.res_1440p = self.width, self.height = 2560, 1440
        self.window = pygame.display.set_mode((self.width, self.height))
    
    def loop(self) -> None:
        """Program loop."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                graphics.character_flags['running'] = False
                graphics.character_flags['idle'] = True
        
        """
        TODO ::  Create helper function to move elements; tie movement
        speed of statics to adaptable variable. Flip character graphics
        when moving to the left. Update when moving to the right again.
        """
        key = pygame.key.get_pressed()
        if key[pygame.K_a]: # Left.
            graphics.coordinates['background_0'][0] += 1
            graphics.coordinates['background_1'][0] += 2
            graphics.coordinates['tile'][0] += 4
            graphics.character_flags['idle'] = False
            graphics.character_flags['running'] = True
        if key[pygame.K_d]: # Right.
            graphics.coordinates['background_0'][0] -= 1
            graphics.coordinates['background_1'][0] -= 2
            graphics.coordinates['tile'][0] -= 4
            graphics.character_flags['idle'] = False
            graphics.character_flags['running'] = True
        if key[pygame.K_w]: # Up.
            graphics.coordinates['background_0'][1] += 1
            graphics.coordinates['background_1'][1] += 2
            graphics.coordinates['tile'][1] += 4
            graphics.character_flags['idle'] = False
            graphics.character_flags['running'] = True
        if key[pygame.K_s]: # Down.
            graphics.coordinates['background_0'][1] -= 1
            graphics.coordinates['background_1'][1] -= 2
            graphics.coordinates['tile'][1] -= 4
            graphics.character_flags['idle'] = False
            graphics.character_flags['running'] = True
        
        
    def render(self) -> None:
        """Renders graphics."""
        # Background images.
        pygame.Surface.fill(self.window, (0, 0, 0))
        pygame.Surface.blit(self.window, graphics.backgrounds['background_0'],
                            (graphics.coordinates['background_0']))
        pygame.Surface.blit(self.window, graphics.backgrounds['background_1'],
                            (graphics.coordinates['background_1']))
        graphics.draw_tiles()
        graphics.draw_character()
        pygame.display.flip()

    def run(self) -> None:
        """Runs the GUI."""
        while self.running:
            self.loop()
            self.render()
        pygame.quit()


class Graphics:
    """Prototype class to show proof of concept for storing
    and using graphics in the game."""
    def __init__(self) -> None:
        self.backgrounds = {
                'background_0' : pygame.transform.scale2x(
                                    pygame.image.load(path + 'background_0.png')),
                'background_1' : pygame.transform.scale2x(
                                    pygame.image.load(path + 'background_1.png')),
            }
        # Tileset, tiles and mapping.
        self.tileset = pygame.image.load(path + 'tileset.png')
        self.tile = {
                'grass_left' : pygame.Surface.subsurface(
                    self.tileset, (0, 0, 124, 124)),
                'grass_middle' : pygame.Surface.subsurface(
                    self.tileset, (124, 0, 124, 124)),
                'grass_right' : pygame.Surface.subsurface(
                    self.tileset, (248, 0, 124, 124)),
                'dirt_middle_left' : pygame.Surface.subsurface(
                    self.tileset, (0, 124, 124, 124)),
                'dirt_middle_middle' : pygame.Surface.subsurface(
                    self.tileset, (124, 124, 124, 124)),
                'dirt_middle_right' : pygame.Surface.subsurface(
                    self.tileset, (248, 124, 124, 124)),
                'dirt_bottom_left' : pygame.Surface.subsurface(
                    self.tileset, (0, 248, 124, 124)),
                'dirt_bottom_middle' : pygame.Surface.subsurface(
                    self.tileset, (124, 248, 124, 124)),
                'dirt_bottom_right' : pygame.Surface.subsurface(
                    self.tileset, (248, 248, 124, 124)),
                'platform_left' : pygame.Surface.subsurface(
                    self.tileset, (0, 372, 124, 124)),
                'platform_middle' : pygame.Surface.subsurface(
                    self.tileset, (124, 372, 124, 124)),
                'platform_right' : pygame.Surface.subsurface(
                    self.tileset, (248, 372, 124, 124)),
            }
        
        # Level array mapping.
        # Two full blocks are enough to block view outside drawing area.
        self.array = [
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 5, 5, 5, 5],
                [5, 5, 5, 5, 8, 8, 8, 5, 5, 5, 5, 8, 8, 8, 8, 8, 0, 4, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 0, 4, 5, 5, 6, 0, 0, 0, 0, 0, 0, 4, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 0, 7, 8, 8, 9, 0, 0, 0, 0, 0, 0, 4, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 5, 5, 5, 5],
                [5, 5, 5, 5, 2, 3, 0,10,11,12, 0, 0, 0, 0, 0, 4, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 8, 9, 0, 0, 0, 0, 0,10,12, 0, 1, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 0, 0, 0, 1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 0, 0, 0, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [0, 5, 5, 6, 0, 0, 1, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 6, 0, 0, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            ]
        self.character = {
            'idle' : pygame.transform.scale2x(
                pygame.image.load(path + 'char_idle.png')),
            'idle_state' : 0,
            'idle_timing' : 0,
            'run' : pygame.transform.scale2x(
                pygame.image.load(path + 'char_run.png')),
            'running_state' : 0,
            'running_timing' : 0
        }
        self.character_flags = {
            'idle' : True,
            'running' : False
        }
        self.character_idle = [pygame.Surface.subsurface(self.character['idle'],
                                                         0, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['idle'],
                                                         100, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['idle'],
                                                         200, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['idle'],
                                                         300, 0, 100, 100)
                                    ]
        self.character_run = [pygame.Surface.subsurface(self.character['run'],
                                                         0, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['run'],
                                                         100, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['run'],
                                                         200, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['run'],
                                                         300, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['run'],
                                                         400, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['run'],
                                                         500, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['run'],
                                                         600, 0, 100, 100),
                               pygame.Surface.subsurface(self.character['run'],
                                                         700, 0, 100, 100)
                                    ]
        # Graphic coordinates. Changes when moving.
        self.coordinates = {
            'background_0' : [0, -400],
            'background_1' : [0, -400],
            # Used to place tiles based on array
            'tile' : [-248, -1860],
            # Sets character in the middle-bottom of the screen.
            'character' : [game.width // 2,
                           game.height // 2] 
            }
    
    def draw_character(self) -> None:
        """Animate character animations."""
        # Idle animation.
        if graphics.character_flags['idle']:
            if self.character['idle_state'] == 0:
                pygame.Surface.blit(game.window, self.character_idle[0],
                                    self.coordinates['character'])
            elif self.character['idle_state'] == 1:
                pygame.Surface.blit(game.window, self.character_idle[1],
                                    self.coordinates['character'])
            elif self.character['idle_state'] == 2:
                pygame.Surface.blit(game.window, self.character_idle[2],
                                    self.coordinates['character'])
            elif self.character['idle_state'] == 3:
                pygame.Surface.blit(game.window, self.character_idle[3],
                                    self.coordinates['character'])
        if pygame.time.get_ticks() > self.character['idle_timing']:
            self.character['idle_timing'] = pygame.time.get_ticks() + 500
            self.character['idle_state'] += 1
            if self.character['idle_state'] == 4:
                self.character['idle_state'] = 0
        
        # Running animation.
        if graphics.character_flags['running']:
            if self.character['running_state'] == 0:
                pygame.Surface.blit(game.window, self.character_run[0],
                                    self.coordinates['character'])
            elif self.character['running_state'] == 1:
                pygame.Surface.blit(game.window, self.character_run[1],
                                    self.coordinates['character'])
            elif self.character['running_state'] == 2:
                pygame.Surface.blit(game.window, self.character_run[2],
                                    self.coordinates['character'])
            elif self.character['running_state'] == 3:
                pygame.Surface.blit(game.window, self.character_run[3],
                                    self.coordinates['character'])
            elif self.character['running_state'] == 4:
                pygame.Surface.blit(game.window, self.character_run[4],
                                    self.coordinates['character'])
            elif self.character['running_state'] == 5:
                pygame.Surface.blit(game.window, self.character_run[6],
                                    self.coordinates['character'])
            elif self.character['running_state'] == 6:
                pygame.Surface.blit(game.window, self.character_run[7],
                                    self.coordinates['character'])
            elif self.character['running_state'] == 7:
                pygame.Surface.blit(game.window, self.character_run[8],
                                    self.coordinates['character'])
        if pygame.time.get_ticks() > self.character['running_timing']:
            self.character['running_timing'] = pygame.time.get_ticks() + 125
            self.character['running_state'] += 1
            if self.character['running_state'] == 4:
                self.character['running_state'] = 0
           
    """
    TODO :: Instead of drawing iterating over array and draw each tile
    repeatedly; create a Tile class which holds the tile object
    coordinates as attribute. You only have to create the tiles once
    and then blit them on repeat in the render method.

    Simplify if/else block.
    """
    def draw_tiles(self) -> None:
        """Renders tiles based on numpy array."""
        x, y = self.coordinates['tile'][0], self.coordinates['tile'][1] 
        z = 0
        tile = ''
        while z < len(self.array):
            for i in self.array[z]:
                if i == 0:
                    # Empty tile; nothing is rendered.
                    tile = ''
                elif i == 1:
                    tile = 'grass_left'
                elif i == 2:
                    tile = 'grass_middle'
                elif i == 3:
                    tile = 'grass_right'
                elif i == 4:
                    tile = 'dirt_middle_left'
                elif i == 5:
                    tile = 'dirt_middle_middle'
                elif i == 6:
                    tile = 'dirt_middle_right'
                elif i == 7:
                    tile = 'dirt_bottom_left'
                elif i == 8:
                    tile = 'dirt_bottom_middle'
                elif i == 9:
                    tile = 'dirt_bottom_right'
                elif i == 10:
                    tile = 'platform_left'
                elif i == 11:
                    tile = 'platform_middle'
                elif i == 12:
                    tile = 'platform_right'
                if tile != '':
                    pygame.Surface.blit(
                            game.window, graphics.tile[tile],
                            (x, y))
                x += 124
            x -= 124 * len(self.array[0])
            y += 124
            z += 1


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Graphics prototype')
    clock = pygame.time.Clock()
    fps = clock.tick(60)
    game = Engine()
    graphics = Graphics()
    game.run()