import pygame
from abc import *

class Entity(ABC):
    def __init__(self) -> None:
        self.health = 1
        self.damage = 1
        self.speed = 2
        self.spritesheet = None
        self.sprite_size = (16 * 8, 16 * 8)
        self.graphic = {}
        self.position = (0, 0)
        self.hazard = True
    
    @abstractmethod
    def move(abc) -> None:
        pass

    @abstractmethod
    def draw(abc) -> None:
        pass