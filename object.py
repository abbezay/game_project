import pygame
import entity

path = './assets/images/'

class Object(entity.Entity):
    """`Base class for objects"""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__()
        self.spritesheet = pygame.image.load(path + 'tileset.png')
        self.position = position
        self.hitbox = pygame.Rect((0, 0), (16 * 8, 16 * 8))
        self.hitbox.bottomleft = position # Centers hitbox.
        self.visible = True

    @staticmethod
    def populate(level_list: list[list]) -> list[object]:
        """
        Populates the level with objects.
        """
        objects = []
        
        x, y = 0, 0 # Determines where enemy collidable objects are placed.
        tile_size = (16 * 8, 16 * 8)
        spawn = {
                81 : Key, 
                82 : Door,
                83 : Heart
            }
        for row in level_list:
            for number in row:
                if number in spawn:
                    object = spawn[number]((x, y + tile_size[1]))
                    objects.append(object)
                x += tile_size[0] # Shift x-origin for next rectangle.
            x = 0 # Resets after a row is finished.
            y += tile_size[1] # Shifts y-origin for next row of rectangles.
        return objects # Returns list of objects.
    
    def move(self) -> None:
        """Objects do not move."""
        pass

    def draw(self, window, move_x: int, move_y: int, time = None) -> None:
        """Draw objects when not collected."""
        aligned = (self.hitbox.x - move_x,
                   self.hitbox.y - move_y)
        if self.visible:
            pygame.Surface.blit(window, self.graphic, (aligned))


class Key(Object):
    """Needs to be collected to finish level."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__(position)
        self.graphic = pygame.Surface.subsurface(self.spritesheet,
                       ((0, self.sprite_size[1] * 4), self.sprite_size))

    def collide(self, player) -> None:
        """Handle collision with player."""
        if not self.visible:
            return # No collision happens if object isn't visible.
        
        # Player interacts with object. 
        if self.hitbox.colliderect(player.hitbox):
            self.visible = False
            player.key_aquired = True
            player.sounds['powerup'].play()
            

class Door(Object):
    """Needs to be entered with key to finish level."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__(position)
        self.graphic = pygame.Surface.subsurface(self.spritesheet,
                       ((self.sprite_size[0], self.sprite_size[1] * 4), self.sprite_size))
        self.graphic = pygame.transform.scale2x(self.graphic)
        self.hitbox.width = self.hitbox.width * 2
        self.hitbox.height = self.hitbox.height * 2
        self.door_opening = False
        self.cooldown = 0
    
    def collide(self, player) -> bool:
        """Handle collision with player."""
        # Player interacts with object.
        if self.door_opening:
            if self.cooldown < pygame.time.get_ticks():
                # Wait for cooldown before finishing level.
                return True    
        elif player.key_aquired == True:
            if self.hitbox.colliderect(player.hitbox):
                # Set cooldown before level is finished.
                pygame.mixer.music.stop()
                player.sounds['victory'].play()
                self.door_opening = True
                self.cooldown = pygame.time.get_ticks() + 2400
                            

class Heart(Object):
    """Adds one health back to player when picked up."""
    def __init__(self, position: tuple[int]) -> None:
        super().__init__(position)
        self.graphic = pygame.Surface.subsurface(self.spritesheet,
                       ((self.sprite_size[0] * 2, self.sprite_size[1] * 4), self.sprite_size))

    def collide(self, player) -> None:
        """Handle collision with player."""
        if not self.visible:
            return # No collision happens if object isn't visible.
        
        # Player interacts with object. 
        if self.hitbox.colliderect(player.hitbox):
            self.visible = False
            player.health += 1
            player.sounds['powerup'].play()