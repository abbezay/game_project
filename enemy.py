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
        self.hitbox = pygame.Rect((0, 0), (16 * 6, 16 * 5))
        self.hitbox.midbottom = position # Centers hitbox.
        self.weakpoint = pygame.Rect((0, 0), (16 * 6, 5))
        self.state = 'alive'

    @staticmethod
    def populate(level_list: list[list]) -> list[object]:
        """
        Creates enemy objects and returns them in a list.
        """
        enemies = []
        
        x, y = 0, 0 # Determines where enemy collidable objects are placed.
        tile_size = (16 * 8, 16 * 8)
        spawn = {
                51 : EnemyGround, 
                52 : EnemyFlying,
                53 : EnemySpike
            }
        for row in level_list:
            for number in row:
                if number in spawn:
                    enemy = spawn[number]((x, y + tile_size[1]))
                    enemies.append(enemy)
                x += tile_size[0] # Shift x-origin for next rectangle.
            x = 0 # Resets after a row is finished.
            y += tile_size[1] # Shifts y-origin for next row of rectangles.
        return enemies # Returns list of objects.
        
    def move(self, blocks: list) -> None:
        """Moves enemy hitboxes if not dead.
        Enemy patrols left to right."""
        # Update weakpoint position on top of hitbox.
        self.weakpoint.midbottom = self.hitbox.midtop

        if self.state == 'alive':
            self.hitbox.x += self.speed
            if self.hitbox.x <= self.anchor[0]:
                self.speed = abs(self.speed)
            elif self.hitbox.x >= self.anchor[0] + (16 * 8) * 2:
                self.speed = -abs(self.speed)
    
    def collide(self, blocks: list, player) -> bool:
        """Handle collision with player"""
        if self.state != 'alive':
            return # No collision happens if enemy is dead.
        
        # Player jumps on enemy.
        if player.state == 'falling':
            if player.stomp.colliderect(self.weakpoint):
                player.sounds['slime_hit'].play()
                self.state = 'dead'
                self.graphic['dead']['cooldown'] = pygame.time.get_ticks() + 1000
                player.state = 'jumping' # The player bounces off the enemy.
                player.graphic['jumping']['length'] = pygame.time.get_ticks() + 350
                return True
        
        # Enemy damages player. 
        if self.hitbox.colliderect(player.hitbox):
            # Determine which side player collide with.
            if self.hitbox.centerx + 1 > player.hitbox.centerx:
                player.take_damage(blocks, 'left')
            else:
                player.take_damage(blocks, 'right')
            return

    def draw(self, window, move_x: int, move_y: int) -> None:
        """Animate enemy on loop.
        Camera coordinates and sprite offsets are used to render the
        enemy in the correct position."""
        time = pygame.time.get_ticks()
        # Move graphic to align with hitbox.
        sprite_offset_x = 16
        sprite_offset_y = 16 * 3
        aligned = (self.hitbox.x - sprite_offset_x - move_x,
                   self.hitbox.y - sprite_offset_y - move_y)

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
            test.y += self.speed * 4
            if test.collidelist(blocks) == -1:
                self.hitbox.y += self.speed * 4

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

    def collide(self, blocks: list, player) -> None:
        """Spike cannot be killed or damaged."""
        if self.hitbox.colliderect(player.hitbox):
            # Determine which side player collide with.
            if self.hitbox.centerx + 1 > player.hitbox.centerx:
                player.take_damage(blocks, 'left')
            else:
                player.take_damage(blocks, 'right')
            return