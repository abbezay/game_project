import pygame
path = './assets/images/'

class Graphics:
    def __init__(self) -> None:
        self.tileset = pygame.image.load(path + 'tileset.png')
        self.tile_size = (16 * 8, 16 * 8)
        self.tile = {
            # Full block.
            1 : pygame.Surface.subsurface(self.tileset,
                ((0, 0), self.tile_size)),
            2 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0], 0), self.tile_size)),
            3 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 2, 0), self.tile_size)),
            4 : pygame.Surface.subsurface(self.tileset,
                ((0, self.tile_size[0]), self.tile_size)),
            5 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0], self.tile_size[1]), self.tile_size)),
            6 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 2, self.tile_size[1]), self.tile_size)),
            7 : pygame.Surface.subsurface(self.tileset,
                ((0, self.tile_size[0] * 2), self.tile_size)),
            8 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0], self.tile_size[1] * 2), self.tile_size)),
            9 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 2, self.tile_size[1] * 2), self.tile_size)),
            # Hollow block.
            11 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 3, 0), self.tile_size)),
            12 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 4, 0), self.tile_size)),
            13 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 5, 0), self.tile_size)),
            14 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 3, self.tile_size[1]), self.tile_size)),
            15 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 4, self.tile_size[1]), self.tile_size)),
            16 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 5, self.tile_size[1]), self.tile_size)),
            17 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 3, self.tile_size[1] * 2), self.tile_size)),
            18 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 4, self.tile_size[1] * 2), self.tile_size)),
            19 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 5, self.tile_size[1] * 2), self.tile_size)),
            # Doodads.
            21 : pygame.Surface.subsurface(self.tileset,
                ((0, self.tile_size[1] * 3), self.tile_size)),
            22 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0], self.tile_size[1] * 3), self.tile_size)),
            23 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 2, self.tile_size[1] * 3), self.tile_size)),
            24 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 3, self.tile_size[1] * 3), self.tile_size)),
        }

    def create_blocks(self, level_list: list[list]) -> tuple[object, ...]:
        blocks = [] # Populate with pygame.Rect objects.
        x, y = 0, 0 # Determines where Rectangles are placed.
        exceptions = [0, 21, 22, 23, 24]
        for i in level_list:
            for ii in i:
                if ii not in exceptions:
                    rectangle = pygame.Rect((x, y), self.tile_size)
                    blocks.append(rectangle)
                x += self.tile_size[0] # Shift x-origin for next rectangle.
            x = 0 # Resets after a row is finished.
            y += self.tile_size[1] # Shifts y-origin for next row of rectangles.
        return tuple(blocks) # Returns tuple of objects.

    def draw_tiles(self, level_list: list[list],
                   window, move_x, move_y) -> None:
        x, y = 0, 0
        for i in level_list:
            for ii in i:
                if ii in self.tile.keys():
                    aligned = (x - move_x, y - move_y)
                    pygame.Surface.blit(
                        window, self.tile[ii], (aligned))
                x += self.tile_size[0]
            x = 0
            y += self.tile_size[1]