import pygame
import entity

path = './assets/images/'

class Enemy(entity.Entity):
    """Base class for enemy classes."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.spritesheet = pygame.image.load(path + 'enemy.png')
        self.position = position
        self.anchor = list(position)
        self.hitbox = pygame.Rect((0, 0), (16 * 8, 16 * 5))
        self.hitbox.bottomleft = position # Centers hitbox.
        self.weakpoint = pygame.Rect((0, 0), (16 * 6, 5))
        self.state = 'alive'

    @staticmethod
    def populate(level: int) -> list[object]:
        """Creates enemy objects based on level and returns them in a list."""
        enemies = []
        if level == 0:
            enemies.append(EnemyGround((128 * 11, 128 * 19)))
            enemies.append(EnemyGround((128 * 14, 128 * 17)))
            enemies.append(EnemyFlying((128 * 11, 128 * 11)))
            enemies.append(EnemySpike((128 * 19, 128 * 14)))
            return enemies
    
    def draw(self, window, move_x: int, move_y: int, time = None) -> None:
        """Animate enemy on loop."""
        time = pygame.time.get_ticks()
        # Move graphic to align with hitbox.
        sprite_offset = 16 * 3
        aligned = (self.hitbox.x - move_x,
                   self.hitbox.y - sprite_offset - move_y)

        if self.state == 'dead':
            pygame.Surface.blit(window, self.graphic[self.state]['frames'][
                self.graphic[self.state]['frame']], (aligned))
            if time > self.graphic[self.state]['cooldown']:
                self.graphic[self.state]['frame'] += 1
                if self.graphic[self.state]['frame'] >= len(self.graphic[self.state]['frames']):
                    self.graphic[self.state]['frame'] = 1
        else:
            pygame.Surface.blit(window, self.graphic[self.state]['frames'][
                self.graphic[self.state]['frame']], (aligned))
            
            # Switch between frames.
            if time > self.graphic[self.state]['cooldown']:
                self.graphic[self.state]['cooldown'] = time + 500
                self.graphic[self.state]['frame'] += 1
                if self.graphic[self.state]['frame'] >= len(self.graphic[self.state]['frames']):
                    self.graphic[self.state]['frame'] = 0
        

class EnemyGround(Enemy):
    """Handles logic for ground enemies."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__(position)
        self.graphic = {
            'alive' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((0, 0), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0]), 0), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0
            },
            'dead' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0] * 2, 0), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0] * 3), 0), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0
                }
            }
    
    def move(self, blocks: list) -> None:
        """Moves enemy hitboxes if not dead.
        Enemy patrols left to right."""
        # Update weakpoint position on top of hitbox.
        self.weakpoint.midbottom = self.hitbox.midtop

        if self.state == 'alive':
            self.hitbox.x += self.speed
            if self.hitbox.x <= self.anchor[0] - (16 * 8):
                self.speed = abs(self.speed)
            elif self.hitbox.x >= self.anchor[0] + (16 * 8):
                self.speed = -abs(self.speed)
                
    
class EnemyFlying(Enemy):
    """Handles logic for Flying enemies."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__(position)
        self.graphic = {
            'alive' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((0, self.sprite_size[1]), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0]), self.sprite_size[1]), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0
            },
            'dead' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0] * 2, self.sprite_size[1]), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0] * 3), self.sprite_size[1]), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0
            }
        }
    
    def move(self, blocks: list) -> None:
        """Moves enemy hitboxes if not dead.
        Enemy patrols up and down."""
        # Sets weakpoint on top of the hitbox.
        self.weakpoint.midbottom = self.hitbox.midtop
        
        if self.state == 'alive':
            self.hitbox.y += self.speed
            if self.hitbox.y <= self.anchor[1] - (16 * 8):
                self.speed = abs(self.speed)
            elif self.hitbox.y >= self.anchor[1] + (16 * 8):
                self.speed = -abs(self.speed) # Reverse direction.
        # Apply gravity when dead.
        else:
            self.speed = abs(self.speed) # Reset direction.
            test = self.hitbox.copy()
            test.y += self.speed
            if test.collidelist(blocks) == -1:
                self.hitbox.y += self.speed

class EnemySpike(Enemy):
    def __init__(self, position: tuple[int]) -> None:
        super().__init__(position)
        self.graphic = {
            'alive' : {
                'frames' : [
                    pygame.Surface.subsurface(self.spritesheet,
                    ((0, self.sprite_size[1] * 2), self.sprite_size)),
                    pygame.Surface.subsurface(self.spritesheet,
                    ((self.sprite_size[0]), self.sprite_size[1] * 2), self.sprite_size)
                ],
                'frame' : 0,
                'cooldown' : 0
            }
        }
    
    def move(self, blocks: list) -> None:
        """This enemy does not move."""
        pass