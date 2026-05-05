import pygame
import entity

path = './assets/images/'

class Player(entity.Entity):
    def __init__(self) -> None:
        super().__init__()
        self.health = 5
        self.iframes = 0
        self.speed = 4
        self.spritesheet = pygame.image.load(path + 'char.png')
        self.graphic = {
            'idle' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((0, 0), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0]), 0), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0
            },
            'moving' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((0, self.sprite_size[1]), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0]), self.sprite_size[1]), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0
            },
            'jumping' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((0, self.sprite_size[1] * 2), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0]), self.sprite_size[1] * 2), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0,
            },
            'falling' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((0, self.sprite_size[1] * 3), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0]), self.sprite_size[1] * 3), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0
            },
            'dead' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((0, self.sprite_size[1] * 4), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0]), self.sprite_size[1] * 4), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0
            }
        }
        # Player hitboxes.
        self.hitbox = pygame.Rect(
            (0, 0), (16 * 8, 16 * 8))
        self.stomp = pygame.Rect(
            (0,0), (16 * 6, 5))
        # Determine player position, used to draw graphic.
        self.sprite_position = None 
        self.state = 'idle'
        self.landed = False
        # Sound effects.
        self.sounds = {
            'jump' : pygame.mixer.Sound('./assets/audio/jump.wav'),
            'land' : pygame.mixer.Sound('./assets/audio/land.wav'),
            'player_hit' : pygame.mixer.Sound('./assets/audio/player_hit.wav'),
            'slime_hit' : pygame.mixer.Sound('./assets/audio/slime_hit.wav'),
            'powerup' : pygame.mixer.Sound('./assets/audio/powerup.wav'),
            'victory' : pygame.mixer.Sound('./assets/audio/victory.wav'),
            'death' : pygame.mixer.Sound('./assets/audio/death.wav'),
        }

    def move(self, blocks: list) -> None:
        """Handles player state and movement inputs."""
        key = pygame.key.get_pressed()

        # Left.
        if self.state != 'dead':
            if key[pygame.K_a]:
                if self.state not in ['jumping', 'falling']:
                    self.state = 'moving'
                # Test collision.
                test = self.hitbox.copy()
                test.x -= self.speed
                if test.collidelist(blocks) == -1:
                    self.hitbox.x -= self.speed

            # Right.
            if key[pygame.K_d]:
                if self.state not in ['jumping', 'falling']:
                    self.state = 'moving'
                # Test collision.
                test = self.hitbox.copy()
                test.x += self.speed
                if test.collidelist(blocks) == -1:
                    self.hitbox.x += self.speed

            # Jump.
            if key[pygame.K_w]:
                if self.landed == True:
                    self.sounds['jump'].play()
                    self.state = 'jumping'
                    # Take the current time and add the offset in milliseconds.
                    self.graphic['jumping']['length'] = pygame.time.get_ticks() + 650
                

    def jump(self, blocks: list) -> None:
        """
        Moves the player upwards until the time of the jump has expired
        or the test object collides with an object.
        """
        # Set landed as false while jumping, disallowing additional jumps.
        self.landed = False
        current_time = pygame.time.get_ticks()
        if current_time < self.graphic['jumping']['length']:
            test = self.hitbox.copy()
            test.y -= self.speed * 2
            if test.collidelist(blocks) == -1:
                self.hitbox.y -= self.speed * 2
            else: # If colliding with Rect object, stops jump.
                self.state = 'falling'
        else: # If jump duration has passed, stops jump.
            self.state = 'falling'

    def gravity(self, blocks: list) -> None:
        """
        Pulls the player down to the ground when not jumping.

        Sets landed as true and play sound when player hits the ground.
        """
        test = self.hitbox.copy()
        test.y += self.speed * 2
        if test.collidelist(blocks) == -1:
            if self.state != 'dead':
                self.state = 'falling'
            self.landed = False
            self.hitbox.y += self.speed * 2
        else:
            if self.state != 'dead':
                self.state = 'idle'
            if self.landed == False:
                self.sounds['land'].play()
                self.landed = True

    def collision_checker(self, enemy_list: list, blocks: list) -> None:
        """Looks for collision between player and any living enemy."""
        for i in enemy_list:
            if i.state == 'alive':
                # Defeat enemy.
                if self.state == 'falling':
                    if self.stomp.colliderect(i.weakpoint):
                        self.sounds['slime_hit'].play()
                        self.state = 'jumping'
                        self.graphic['jumping']['length'] = pygame.time.get_ticks() + 350
                        i.state = 'dead'
                        i.hazard = False
                        i.graphic['dead']['cooldown'] = pygame.time.get_ticks() + 1000
                # Take damage from enemy.
            if i.hazard == True:
                if self.hitbox.colliderect(i.hitbox):
                    knockback_x = 128
                    knockback_y = 64
                    # Knockback left.
                    if self.hitbox.centerx < i.hitbox.centerx + 1:
                        test = self.hitbox.copy()
                        test.x -= knockback_x
                        if test.collidelist(blocks) != -1:
                            knockback_x = -abs(knockback_x)
                        self.hitbox.x -= knockback_x
                        self.hitbox.y -= knockback_y
                    # Knockback right.
                    elif self.hitbox.centerx > i.hitbox.centerx - 1:
                        test = self.hitbox.copy()
                        test.x += knockback_x
                        if test.collidelist(blocks) != -1:
                            print('collision right')
                            knockback_x = -abs(knockback_x)
                        self.hitbox.x += knockback_x
                        self.hitbox.y -= knockback_y
                    if self.iframes < pygame.time.get_ticks():
                        # One second must pass before taking damage again.
                        self.iframes = pygame.time.get_ticks() + 1000
                        self.health -= 1
                        self.sounds['player_hit'].play()
                        if self.health == 0:
                            pygame.mixer.music.stop()
                            self.sounds['death'].play()
                            self.state = 'dead'
                            self.graphic['dead']['cooldown'] = pygame.time.get_ticks() + 1600

    def draw(self, window, coordinates: object) -> None:
        """Animate character for all states."""
        # TODO :: Add variables that hold complex values in order to increase readability.
        
        time = pygame.time.get_ticks()
        current_state = self.graphic[self.state]
        drawn_frame = current_state['frames'][current_state['frame']]
        
        if self.state == 'dead':
            pygame.Surface.blit(window, drawn_frame, (coordinates))
            if time > current_state['cooldown']:
                current_state['frame'] += 1
                if current_state['frame'] >= len(current_state['frames']):
                    current_state['frame'] = 1      
        else:
            pygame.Surface.blit(window, drawn_frame, (coordinates))
            # Switch between frames.
            if time > current_state['cooldown']:
                current_state['cooldown'] = time + 500
                current_state['frame'] += 1
                if current_state['frame'] >= len(current_state['frames']):
                    current_state['frame'] = 0