import pygame
import player, enemy, object, graphics


class Engine:
    def __init__(self) -> None:
        self.running = True
        # self._size = self._width, self._height = 1280, 720
        self._size = self._width, self._height = 1920, 1080
        self._window = pygame.display.set_mode(self._size)
        self.clock = pygame.time.Clock()
        self.level = {
            'current_level' : 4,
            'path' : ['level_0.txt', 'level_1.txt',
                      'level_2.txt', 'level_3.txt',
                      'level_4.txt'],
            # Starting position counted in blocks x, then y.
            'start' : [(128 * 9, 128 * 20), (128 * 7, 128 * 9),
                       (128 * 8, 128 * 20), (128 * 13, 128 * 8),
                       (128 * 14, 128 * 8)],
            'block_list' : [[]],
            'blocks' : () # Rect objects are never moved.
            }
        # Counts down seconds left to complete level. Game over on 0.
        self.countdown = {
            'time' : 0,
            'cooldown' : 0
            }
        # Increases when defeating enemies and completing levels in time.
        self.score = 0
        # Class objects.
        self.graphics = graphics.Graphics()
        self.player = player.Player()
        self.enemy_list = []
        self.object_list = []
        # Camera movement. These set the coordinates where the graphics
        # are rendered, without moving the collidable Rect objects,
        # so that the player only sees what is happening around them.
        self.camera_x = 0
        self.camera_y = 0
        # Sets what is being rendered.
        self.state = 'main menu'
        self.level_initated = False
        self.music_playing = False
        self.buttons = {
            'start' : graphics.Button('Start Game',
                        (self._width // 2, self._height // 3),
                        (450, 100)),
            'exit' : graphics.Button('Exit Game',
                        (self._width // 2, self._height // 2),
                        (450, 100)),
            'return' : graphics.Button('Return to Main Menu',
                        (self._width // 2, self._height // 2),
                        (900, 150))
            }

    def loop(self, event: pygame) -> None:
        """Loops the game dependant on current state."""
        # Main menu.
        if self.state == 'main menu':
            if self.music_playing == False:
                self.music_playing = True
                pygame.mixer.music.load('./assets/audio/main_menu.mp3')
                pygame.mixer.music.play(-1)
            if self.graphics.draw_main_menu(self._window, self, event):
                self.music_playing = False
                pygame.mixer.music.stop()
                self.state = 'playing'
            pygame.display.flip()
            
        # Game over.
        elif self.state == 'game_over':
            if self.music_playing == False:
                self.music_playing = True
                pygame.mixer.music.load('./assets/audio/game_over_loss.mp3')
                pygame.mixer.music.play(-1)
            if self.graphics.draw_game_over_loss(self._window, self, event):
                # Reset attributes to allow a new run.
                self.level['current_level'] = 0
                self.level_initated = False
                self.music_playing = False
                self.score = 0
                self.player.key_aquired = False
                self.player.health = 4
                self.player.state = 'alive'
                self.state = 'main menu'
            pygame.display.flip()
            
        # Playing level.
        elif self.state == 'playing':
            if self.music_playing == False:
                self.music_playing = True
                pygame.mixer.music.load('./assets/audio/background.mp3')
                pygame.mixer.music.play()
            if self.level_initated == False:
                pygame.mixer.music.rewind()
                self.initiate_level()
                self.level_initated = True
            # Matches drawing coordinates with player hitbox.
            self.camera_x = self.player.hitbox.centerx - self._width // 2
            self.camera_y = self.player.hitbox.centery - self._height // 2
            # Matches stomp hitbox with hitbox.
            self.player.stomp.midtop = self.player.hitbox.midbottom
            for enemy in self.enemy_list: # Enemy move and check collision.
                enemy.move(self.level['blocks'])
                if enemy.collide(self.level['blocks'], self.player):
                    # If enemy is defeated, add score.
                    self.score += 20
            for object in self.object_list: # Object collisions.
                if object.collide(self.player):
                    # Player finish a level.
                    self.score += self.countdown['time'] * 3
                    self.score += self.player.health * 25
                    self.player.key_aquired = False
                    self.level['current_level'] += 1
                    if self.level['current_level'] >= len(self.level['path']):
                        self.music_playing = False
                        self.state = 'victory'
                    else:
                        self.level_initated = False
                    return
            self.player.move(self.level['blocks']) # Take movement inputs.
            # Gravity only active when not jumping.
            if self.player.state not in ['jumping']:
                self.player.gravity(self.level['blocks'])
            if self.player.state == 'jumping':
                self.player.jump(self.level['blocks'])
            self.level_countdown()
            self.render_level()

        # Victory.
        elif self.state == 'victory':
            if self.music_playing == False:
                self.music_playing = True
                pygame.mixer.music.load('./assets/audio/game_over_win.mp3')
                pygame.mixer.music.play(-1)
            if self.graphics.draw_game_over_win(self._window, self, event):
                # Reset attributes to allow a new run.
                self.level['current_level'] = 0
                self.level_initated = False
                self.music_playing = False
                self.score = 0
                self.player.key_aquired = False
                self.player.health = 4
                self.player.state = 'alive'
                self.state = 'main menu'
            pygame.display.flip()
        
    def render_level(self) -> None:
        """Draws game graphics."""
        self._window.fill((50, 50, 100))
        # Draw tiles.
        self.graphics.draw_tiles(self.level['block_list'],
                                 self._window, self.camera_x, self.camera_y)
        
        # # Troubleshooting aid: display enemy hitboxes.
        # Body.
        # for i in self.enemy_list:
        #             pygame.draw.rect(self._window, (0, 0, 150),
        #                     pygame.Rect(i.hitbox.x - self.camera_x,
        #                         i.hitbox.y - self.camera_y,
        #                         i.hitbox.width,
        #                         i.hitbox.height))
        # # Weakpoint.
        # for i in self.enemy_list:
        #             pygame.draw.rect(self._window, (0, 0, 150),
        #                     pygame.Rect(i.weakpoint.x - self.camera_x,
        #                         i.weakpoint.y - self.camera_y,
        #                         i.weakpoint.width,
        #                         i.weakpoint.height))

        # # Troubleshooting aid: display player hitboxes.
        # # Body.
        # pygame.draw.rect(self._window, (150, 0, 0),
        #                     (self.player.hitbox.x - self.camera_x,
        #                     self.player.hitbox.y - self.camera_y,
        #                     self.player.hitbox.width,
        #                     self.player.hitbox.height))
        # # Stomp.
        # pygame.draw.rect(self._window, (150, 0, 0),
        #                     pygame.Rect(self.player.stomp.x - self.camera_x,
        #                         self.player.stomp.y - self.camera_y,
        #                         self.player.stomp.width,
        #                         self.player.stomp.height))

        
        # Draw objects.
        for i in self.object_list:
            i.draw(self._window, self.camera_x, self.camera_y)
        # Draw enemies.
        for i in self.enemy_list:
            i.draw(self._window, self.camera_x, self.camera_y)
        # Draw UI.
        self.graphics.draw_ui(self._window, self)
        # Draw player.
        if self.player.draw(self._window, self.player.sprite_position):
            self.music_playing = False
            self.state = 'game_over'
        pygame.display.update()

    def level_countdown(self) -> None:
        """
        Countdown to complete level in time, else game over.
        Resets at the start of each level.
        """
        if self.countdown['time'] == 0:
            pygame.mixer.music.stop()
            self.player.sounds['death']
            pygame.time.wait(2000)
            self.state = 'game_over'
        
        if self.countdown['cooldown'] < pygame.time.get_ticks():
            self.countdown['time'] -= 1
            self.countdown['cooldown'] = pygame.time.get_ticks() + 1000

    def initiate_level(self) -> None:
        """
        Set conditions necessary to play the levels.
        """
        # Converts level array to list.
        self.level['block_list'] = self.load_blocks() 
        # Create level tiles.
        self.level['blocks'] = self.graphics.create_blocks(self.level['block_list']) 
        # Populate level with enemies.
        self.enemy_list = enemy.Enemy.populate(self.level['block_list'])
        # Populate level with objects.
        self.object_list = object.Object.populate(self.level['block_list'])
        self.player.hitbox.center = (self._width // 2, self._height // 2)
        self.player.sprite_position = self.player.hitbox.copy()
        # Sets player starting position, counted in tiles.
        self.player.hitbox.x, self.player.hitbox.y = self.level['start'][self.level['current_level']]
        # Set level coundown.
        self.countdown['time'] = 60
        self.countdown['cooldown'] = pygame.time.get_ticks() + 1000
        # Starts level music.
        pygame.mixer.music.play()

    def load_blocks(self) -> list[list]:
        """
        Converts the .txt file to a nested list, which is used to build
        the level.
        """
        level_list = []
        with open('./levels/' + self.level['path'][self.level['current_level']], 'r') as f:
            f.readline() # Skips initial line.
            while True:
                line = f.readline().strip()
                if line == ']':
                    return level_list
                line = line.replace('[', '').replace(']', '').split(',')
                list_line = []
                for i in line:
                    i = i.strip()
                    if i != '':
                        list_line.append(int(i))
                level_list.append(list_line)