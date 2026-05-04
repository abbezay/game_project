import pygame
import player, enemy, graphics


class Engine:
    def __init__(self) -> None:
        self.running = True
        self.size = self.width, self.height = 1280, 720
        self.window = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.level = {
            'level' : 0,
            'path' : ['level_1.txt', 'level_2.txt',
                      'level_3.txt', 'level_4.txt'],
            'start' : [(128 * 5, 128 * 18)],
            'block_list' : [[]],
            'blocks' : () # Rect objects are never moved.
            }
        # Counts down seconds left to complete level. Game over on 0.
        self.countdown = {
            'time' : 180,
            'cooldown' : 1000
            }
        # Adds up when defeating enemies, completing levels in time.
        self.score = 0
        # Background music. Resets each level.
        self.sounds = {
            'jump' : pygame.mixer.Sound('./assets/audio/jump.wav'),
            'land' : pygame.mixer.Sound('./assets/audio/land.wav'),
            'player_hit' : pygame.mixer.Sound('./assets/audio/player_hit.wav'),
            'slime_hit' : pygame.mixer.Sound('./assets/audio/slime_hit.wav'),
            'powerup' : pygame.mixer.Sound('./assets/audio/powerup.wav'),
            'victory' : pygame.mixer.Sound('./assets/audio/victory.wav'),
            'death' : pygame.mixer.Sound('./assets/audio/death.wav'),
        }

        # Class objects.
        self.graphics = graphics.Graphics()
        self.player = player.Player()
        self.enemy = []

        # Player hitboxes.
        self.player_rect = pygame.Rect(
            (0, 0), (16 * 8, 16 * 8))
        self.player_stomp = pygame.Rect(
            (0,0), (16 * 6, 5))
        # Determine player position, used to draw graphic.
        self.player_static = None 
        # Movement and camera.
        self.speed = 4
        self.camera_x = 0
        self.camera_y = 0

        


    def loop(self) -> None:
        # Matches drawing coordinates with player hitbox.
        self.camera_x = self.player_rect.centerx - self.width // 2
        self.camera_y = self.player_rect.centery - self.height // 2
        # Matches stomp hitbox with player_rect.
        self.player_stomp.midtop = self.player_rect.midbottom
        
        for i in self.enemy:
           i.move()
        self.movement()
        if self.player.state == 'falling':
            self.collision_checker()
        self.render()
       
        
    def render(self) -> None:
        """Draws game graphics."""
        self.window.fill((50, 50, 100))
        # Draw tiles.
         
        self.graphics.draw_tiles(self.level['block_list'],
                                 self.window, self.camera_x, self.camera_y)
        
        # Test, draw Enemy hitboxes.
        # Body.
        # for i in self.enemy:
        #             pygame.draw.rect(self.window, (0, 0, 150),
        #                     pygame.Rect(i.enemy_rect.x - self.camera_x,
        #                         i.enemy_rect.y - self.camera_y,
        #                         i.enemy_rect.width,
        #                         i.enemy_rect.height))
        # # Weakpoint.
        # for i in self.enemy:
        #             pygame.draw.rect(self.window, (0, 0, 150),
        #                     pygame.Rect(i.enemy_weakpoint.x - self.camera_x,
        #                         i.enemy_weakpoint.y - self.camera_y,
        #                         i.enemy_weakpoint.width,
        #                         i.enemy_weakpoint.height))

        # Draw enemies.
        for i in self.enemy:
            i.draw(self.window, self.camera_x, self.camera_y)
        
        # Test, draw player hitboxes.
        # Body.
        # pygame.draw.rect(self.window, (150, 0, 0),
        #                     (self.player_rect.x - self.camera_x,
        #                     self.player_rect.y - self.camera_y,
        #                     self.player_rect.width,
        #                     self.player_rect.height))
        # # Stomp.
        # pygame.draw.rect(self.window, (150, 0, 0),
        #                     pygame.Rect(self.player_stomp.x - self.camera_x,
        #                         self.player_stomp.y - self.camera_y,
        #                         self.player_stomp.width,
        #                         self.player_stomp.height))
        # Draw player.
        self.player.draw(self.window, self.player_static)

        pygame.display.update()

    def level_timer(self) -> None:
        """
        Countdown to complete level in time, else game over.
        Resets at the start of each level.
        """
        

    def initiate_level(self) -> None:
        self.level['block_list'] = self.load_blocks() # Converts level array to list.
        self.level['blocks'] = self.graphics.create_blocks(self.level['block_list']) # Create collisionable objects.
        self.player_rect.center = (self.width // 2, self.height // 2)
        self.player_static = self.player_rect.copy()
        # Sets player starting position, counted in tiles.
        self.player_rect.x, self.player_rect.y = self.level['start'][self.level['level']]
        # Populates level with enemies.
        for i in enemy.Enemy.populate(self.level['level']):
            self.enemy.append(i)
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
    
    def movement(self) -> None:
        """Handles player state and movement inputs."""
        key = pygame.key.get_pressed()

        # Gravity only active when not jumping.
        if self.player.state not in ['jumping']:
            self.gravity()
        if self.player.state == 'jumping':
            self.jump()

        # Left.
        if self.player.state != 'dead':
            if key[pygame.K_a]:
                if self.player.state not in ['jumping', 'falling']:
                    self.player.state = 'moving'
                # Test collision.
                test = self.player_rect.copy()
                test.x -= self.speed
                if test.collidelist(self.level['blocks']) == -1:
                    self.player_rect.x -= self.speed

            # Right.
            if key[pygame.K_d]:
                if self.player.state not in ['jumping', 'falling']:
                    self.player.state = 'moving'
                # Test collision.
                test = self.player_rect.copy()
                test.x += self.speed
                if test.collidelist(self.level['blocks']) == -1:
                    self.player_rect.x += self.speed

            # Jump.
            if key[pygame.K_w]:
                if self.player.landed == True:
                    self.sounds['jump'].play()
                    self.player.state = 'jumping'
                    # Take the current time and add the offset in milliseconds.
                    self.player.graphic['jumping']['length'] = pygame.time.get_ticks() + 650

            # Death test. Temp.
            if key[pygame.K_s]:
                pygame.mixer.music.stop()
                self.sounds['death'].play()
                self.player.state = 'dead'
                self.player.graphic['dead']['cooldown'] = pygame.time.get_ticks() + 1600

    def collision_checker(self) -> None:
        """Looks for collision between player and enemy objects."""
        for i in self.enemy:
            if i.state == 'alive':
                if self.player_stomp.colliderect(i.enemy_weakpoint):
                    self.sounds['slime_hit'].play()
                    self.player.state = 'jumping'
                    self.player.graphic['jumping']['length'] = pygame.time.get_ticks() + 350
                    i.state = 'dead'
                    i.graphic['dead']['cooldown'] = pygame.time.get_ticks() + 1000


    def gravity(self) -> None:
        """
        Pulls the player down to the ground when not jumping.

        Sets landed as true and play sound when player hits the ground.
        """
        test = self.player_rect.copy()
        test.y += self.speed * 2
        if test.collidelist(self.level['blocks']) == -1:
            if self.player.state != 'dead':
                self.player.state = 'falling'
            self.player.landed = False
            self.player_rect.y += self.speed * 2
        else:
            if self.player.state != 'dead':
                self.player.state = 'idle'
            if self.player.landed == False:
                self.sounds['land'].play()
                self.player.landed = True

    def jump(self) -> None:
        """
        Moves the player upwards until the time of the jump has expired
        or the test object collides with an object.
        """
        # Set landed as false while jumping, disallowing additional jumps.
        self.player.landed = False
        if pygame.time.get_ticks() < self.player.graphic['jumping']['length']:
            test = self.player_rect.copy()
            test.y -= self.speed * 2
            if test.collidelist(self.level['blocks']) == -1:
                self.player_rect.y -= self.speed * 2
            else: # If colliding with Rect object, stops jump.
                self.player.state = 'falling'
        else: # If jump duration has passed, stop jump.
            self.player.state = 'falling'