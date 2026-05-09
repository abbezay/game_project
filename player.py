import pygame
import entity

path = './assets/images/'

class Player(entity.Entity):
    def __init__(self) -> None:
        super().__init__()
        self.health = 4
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
                'length' : 0
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
        self.key_aquired = False
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

    def take_damage(self, blocks: list, direction: str) -> None:
        """Take damage when coming into contact with damage source.
        TODO :: Make knockback feel smoother.
        TODO :: View iframe window. Disallow additional knockback meanwhile."""
        knockback_x = 128
        knockback_y = 64
        if direction == 'right':
            knockback_x = -abs(128)
        test = self.hitbox.copy()
        test.x -= knockback_x
        test.y -= knockback_y
        if test.collidelist(blocks) != -1:
            if knockback_x > 0:
                knockback_x = -abs(knockback_x)
            else:
                knockback_x = abs(knockback_x)
        self.hitbox.x -= knockback_x
        self.hitbox.y -= knockback_y

        # Add iframes so player cannot be damaged again instantly.
        if self.iframes < pygame.time.get_ticks():
            # Time must pass before taking damage again.
            self.iframes = pygame.time.get_ticks() + 500
            self.health -= 1
            self.sounds['player_hit'].play()

        # Damaged cause is enough to kill the player.
        if self.health == 0:
            pygame.mixer.music.stop()
            self.sounds['death'].play()
            self.state = 'dead'
            self.graphic['dead']['cooldown'] = pygame.time.get_ticks() + 1600

    def draw(self, window, coordinates: object) -> bool:
        """
        Animate character for all states.
        Returns:
            After death animations returns True.
        """
        # TODO :: Add variables that hold complex values in order to increase readability.
        # Done.

        time = pygame.time.get_ticks()
        current_state = self.graphic[self.state]
        drawn_frame = current_state['frames'][current_state['frame']]
        
        if self.state == 'dead':
            pygame.Surface.blit(window, drawn_frame, (coordinates))
            if time > current_state['cooldown']:
                current_state['frame'] += 1
                self.graphic['dead']['cooldown'] = pygame.time.get_ticks() + 2500
                if current_state['frame'] >= len(current_state['frames']):
                    current_state['frame'] = 1
                    return True
        else:
            pygame.Surface.blit(window, drawn_frame, (coordinates))
            # Switch between frames.
            if time > current_state['cooldown']:
                current_state['cooldown'] = time + 500
                current_state['frame'] += 1
                if current_state['frame'] >= len(current_state['frames']):
                    current_state['frame'] = 0