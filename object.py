import pygame
import entity

path = './images/'

class Object(entity.Entity):
    """`Base class for objects"""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.spritesheet = pygame.image.load(path + 'tileset.png')
        self.position = position
        self.hitbox = pygame.Rect((0, 0), (16 * 8, 16 * 8))
        self.state = 'visible'
        self.hazard = False

    def collision(self) -> None:
        """Handle collision with player different depending on object."""
        pass

class Key(Object):
    """Needs to be collected to finish level."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.graphic = pygame.Surface.subsurface(self.tileset,
                       ((0, self.tile_size[1] * 4), self.tile_size))

class Door(Object):
    """Needs to be entered with key to finish level."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.graphic = pygame.Surface.subsurface(self.tileset,
                       ((self.tile_size[0], self.tile_size[1] * 4), self.tile_size))

class Heart(Object):
    """Adds one health back to player when picked up."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.graphic = pygame.Surface.subsurface(self.tileset,
                       ((self.tile_size[0], self.tile_size[1] * 4), self.tile_size))