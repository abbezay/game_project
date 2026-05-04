import pygame
import entity

path = './assets/images/'

class Enemy(entity.Entity):
    """Base class for enemy classes."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.spritesheet = pygame.image.load(path + 'enemy.png')
        self.sprite_size = (16 * 8, 16 * 8)
        self.position = position
        self.anchor = list(position)
        self.enemy_rect = pygame.Rect((0, 0), (16 * 8, 16 * 5))
        self.enemy_rect.bottomleft = position # Sets hitbox centered.
        self.enemy_weakpoint = pygame.Rect((0, 0), (16 * 6, 5))
        self.hazard = True
        self.state = 'alive'

    @staticmethod
    def populate(level: int) -> list[object]:
        """Creates enemy objects based on level and returns them in a list."""
        enemies = []
        if level == 0:
            enemies.append(EnemyGround((128 * 9, 128 * 17)))
            enemies.append(EnemyGround((128 * 12, 128 * 15)))
            enemies.append(EnemyFlying((128 * 9, 128 * 9)))
            return enemies
        

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
    
    def move(self) -> None:
        """Moves enemy hitboxes if not dead.
        
        Enemy patrols one tile to either side of spawn."""
        # Update weakpoint position on top of hitbox.
        self.enemy_weakpoint.midbottom = self.enemy_rect.midtop

        if self.state == 'alive':
            self.enemy_rect.x += self.speed
            if self.enemy_rect.x <= self.anchor[0] - (16 * 8):
                self.speed = abs(self.speed)
            elif self.enemy_rect.x >= self.anchor[0] + (16 * 8):
                self.speed = -abs(self.speed)
                
    
    def draw(self, window, move_x: int, move_y: int, time = None) -> None:
        """Animate enemy on loop."""
        time = pygame.time.get_ticks()
        # Move graphic to align with hitbox.
        sprite_offset = 16 * 3
        aligned = (self.enemy_rect.x - move_x,
                   self.enemy_rect.y - sprite_offset - move_y)

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
    
    def move(self) -> None:
        """Moves enemy hitboxes if not dead."""
        # Sets weakpoint on top of hitbox.
        self.enemy_weakpoint.midbottom = self.enemy_rect.midtop
        
        if self.state == 'alive':
            self.enemy_rect.y += self.speed
            if self.enemy_rect.y <= self.anchor[1] - (16 * 8):
                self.speed = abs(self.speed)
            elif self.enemy_rect.y >= self.anchor[1] + (16 * 8):
                self.speed = -abs(self.speed)
    
    def draw(self, window, move_x: int, move_y: int, time = None) -> None:
        """Animate enemy on loop."""
        time = pygame.time.get_ticks()
        # Move graphic to align with hitbox.
        sprite_offset = 16 * 3
        aligned = (self.enemy_rect.x - move_x,
                   self.enemy_rect.y - sprite_offset - move_y)

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