import pygame
from abc import *

class Entity(ABC):
    def __init__(self) -> None:
        self.health = 1
        self.damage = 1
        self.speed = 2
        self.spritesheet = None
        self.sprite_size = (0, 0)
        self.graphic = {}
        self.position = (0, 0)
        self.hazard = False
    
    @abstractmethod
    def move(abc) -> None:
        pass