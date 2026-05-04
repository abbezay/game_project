import pygame
import entity

path = './assets/images/'

class Player(entity.Entity):
    def __init__(self) -> None:
        super().__init__()
        self.health = 5
        self.spritesheet = pygame.image.load(path + 'char.png')
        self.sprite_size = (16 * 8, 16 * 8)
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
        self.state = 'idle'
        self.landed = False

    def move(self) -> None:
        pass
    
    def draw(self, window, coordinates: object) -> None:
        """
        Animate character for all states."""
        time = pygame.time.get_ticks()

        if self.state == 'dead':
            pygame.Surface.blit(window, self.graphic[self.state]['frames'][
                self.graphic[self.state]['frame']], (coordinates))
            if time > self.graphic[self.state]['cooldown']:
                self.graphic[self.state]['frame'] += 1
                if self.graphic[self.state]['frame'] >= len(self.graphic[self.state]['frames']):
                    self.graphic[self.state]['frame'] = 1      
        else:
            pygame.Surface.blit(window, self.graphic[self.state]['frames'][
                self.graphic[self.state]['frame']], (coordinates))
            
            # Switch between frames.
            if time > self.graphic[self.state]['cooldown']:
                self.graphic[self.state]['cooldown'] = time + 500
                self.graphic[self.state]['frame'] += 1
                if self.graphic[self.state]['frame'] >= len(self.graphic[self.state]['frames']):
                    self.graphic[self.state]['frame'] = 0