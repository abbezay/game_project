import pygame
from abc import *

class Entity(ABC):
    def __init__(self) -> None:
        self.speed = 2
        self.spritesheet = None
        self.sprite_size = (16 * 8, 16 * 8)
        self.graphic = {}
        self.position = (0, 0)
    
    @abstractmethod
    def move(abc) -> None:
        pass

    @abstractmethod
    def draw(abc) -> None:
        pass