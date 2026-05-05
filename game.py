import pygame
import player, enemy, graphics


class Engine:
    def __init__(self) -> None:
        self.running = True
        # self._size = self._width, self._height = 1280, 720
        self._size = self._width, self._height = 1920, 1080
        self._window = pygame.display.set_mode(self._size)
        self.clock = pygame.time.Clock()

        self.level = {
            'level' : 0,
            'path' : ['level_1.txt', 'level_2.txt',
                      'level_3.txt', 'level_4.txt'],
            'start' : [(128 * 9, 128 * 20)],
            'block_list' : [[]],
            'blocks' : () # Rect objects are never moved.
            }
        # Counts down seconds left to complete level. Game over on 0.
        self.countdown = {
            'time' : 180,
            'cooldown' : 1000
            }
        # Adds up when defeating enemies, completing levels in time.
        self.score_total = 0

        # Class objects.
        self.graphics = graphics.Graphics()
        self.player = player.Player()
        self.enemy_list = []

        # Camera movement.
        self.camera_x = 0
        self.camera_y = 0

    def loop(self) -> None:
        # Matches drawing coordinates with player hitbox.
        self.camera_x = self.player.hitbox.centerx - self._width // 2
        self.camera_y = self.player.hitbox.centery - self._height // 2
        # Matches stomp hitbox with hitbox.
        self.player.stomp.midtop = self.player.hitbox.midbottom
        for i in self.enemy_list: # Move enemies.
           i.move(self.level['blocks'])
        self.player.move(self.level['blocks']) # Take movement inputs.
        # Check for collision between player and enemies.
        self.player.collision_checker(self.enemy_list, self.level['blocks'])
        # Gravity only active when not jumping.
        if self.player.state not in ['jumping']:
            self.player.gravity(self.level['blocks'])
        if self.player.state == 'jumping':
            self.player.jump(self.level['blocks'])
        self.render()
        
    def render(self) -> None:
        """Draws game graphics."""
        self._window.fill((50, 50, 100))
        # Draw tiles.
        self.graphics.draw_tiles(self.level['block_list'],
                                 self._window, self.camera_x, self.camera_y)
        
        # # Test, draw Enemy hitboxes.
        # # Body.
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

        # Draw enemies.
        for i in self.enemy_list:
            i.draw(self._window, self.camera_x, self.camera_y)
        
        # # Test, draw player hitboxes.
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
        # Draw player.
        self.player.draw(self._window, self.player.sprite_position)

        pygame.display.update()

    def level_countdown(self) -> None:
        """
        Countdown to complete level in time, else game over.
        Resets at the start of each level.
        """
        

    def initiate_level(self) -> None:
        self.level['block_list'] = self.load_blocks() # Converts level array to list.
        self.level['blocks'] = self.graphics.create_blocks(self.level['block_list']) # Create collisionable objects.
        self.player.hitbox.center = (self._width // 2, self._height // 2)
        self.player.sprite_position = self.player.hitbox.copy()
        # Sets player starting position, counted in tiles.
        self.player.hitbox.x, self.player.hitbox.y = self.level['start'][self.level['level']]
        # Populates level with enemies.
        for i in enemy.Enemy.populate(self.level['level']):
            self.enemy_list.append(i)
        # Set level coundown.
        self.countdown = 180
        # Starts level music.
        pygame.mixer.music.play()

    def load_blocks(self) -> list[list]:
        """
        Converts the .txt file to a nested list, which is used to build
        the level.
        """
        level_list = []
        with open('./levels/' + self.level['path'][self.level['level']], 'r') as f:
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