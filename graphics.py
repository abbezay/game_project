import pygame
path = './assets/images/'

class Graphics:
    def __init__(self) -> None:
        self.tileset = pygame.image.load(path + 'tileset.png')
        self.backgrounds = {
            'main_menu' : pygame.image.load(path + 'mainmenu.png'),
            'game_over_loss' : pygame.image.load(path + 'game_over_loss.png'),
            'game_over_win' : pygame.image.load(path + 'game_over_win.png')
        }
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
            25 : pygame.Surface.subsurface(self.tileset,
                ((self.tile_size[0] * 4, self.tile_size[1] * 3), self.tile_size)),
        }
        self._myfont = pygame.font.Font('./assets/press_start_2p.ttf', 38)
        self.cooldown = 0
        


    def create_blocks(self, level_list: list[list]) -> tuple[object, ...]:
        blocks = [] # Populate with pygame.Rect objects.
        x, y = 0, 0 # Determines where Rectangles are placed.
        # Doodads, enemies and objects are drawn but not collidable.
        exceptions = [0, # Empty tile.
                      21, 22, 23, 24, 25, # Doodads.
                      51, 52, 53, # Enemies.
                      81, 82, 83] # Objects.
        for row in level_list:
            for number in row:
                if number not in exceptions:
                    blocks.append(pygame.Rect((x, y), self.tile_size))
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

    def draw_ui(self, window, engine) -> None:
        """Draws the UI from attributes in both Engine and Player."""

        # Add current level information.
        self.write('Level  ' + str(engine.level['current_level'] + 1),
                   engine._window, 40, 40)
        # Add score tracker.
        self.write('Score  ' + str(engine.score),
                   engine._window, 40, 100)
        # Add current health.
        self.write('Health ' + str(engine.player.health),
                   engine._window, 40, 160)
        # Add time left to complete level.
        self.write('Time left',
                   engine._window, engine._width // 2, 40,
                   centered = True)
        self.write(str(engine.countdown['time']),
                   engine._window, engine._width // 2, 80,
                   centered = True)

    def draw_main_menu(self, window, engine, event: pygame) -> bool:
        """Draws the interactable main menu.
        
        Returns:
            If play is clicked return True."""
        pygame.Surface.blit(window, self.backgrounds['main_menu'], (0, 0))
        self.write('To Be Determined',
                   engine._window, engine._width // 2, engine._height // 5,
                   centered = True)
        engine.buttons['start'].draw(window, self)
        engine.buttons['exit'].draw(window, self)
        if engine.buttons['start'].press(event):
            return True
        if engine.buttons['exit'].press(event):
            pygame.time.wait(360) # Allows click.wav to play before exit.
            engine.running = False

    def draw_game_over_loss(self, window, engine, event: pygame) -> bool:
        """Draws the interactable game over screen.
        
        Return:
            If return to main menu is clicked return True."""
        pygame.Surface.blit(window, self.backgrounds['game_over_loss'], (0, 0))
        self.write('Game Over',
                   engine._window, engine._width // 2, engine._height // 5,
                   centered = True)
        self.write('Score: ' + str(engine.score),
                   engine._window, engine._width // 2, engine._height // 4,
                   centered = True)
        if self.cooldown == 0:
            self.cooldown = pygame.time.get_ticks() + 3000
        elif self.cooldown < pygame.time.get_ticks():
            engine.buttons['return'].draw(window, self)
            if engine.buttons['return'].press(event):
                self.cooldown = 0
                return True

    def draw_game_over_win(self, window, engine, event: pygame) -> bool:
        """Draws the interactable victory screen.
        
        Return:
            If return to main menu is clicked return True."""
        pygame.Surface.blit(window, self.backgrounds['game_over_win'], (0, 0))
        self.write('You Win!',
                   engine._window, engine._width // 2, engine._height // 5,
                   centered = True)
        self.write('Score: ' + str(engine.score),
                   engine._window, engine._width // 2, engine._height // 4,
                   centered = True)
        if self.cooldown == 0:
            self.cooldown = pygame.time.get_ticks() + 10000
        elif self.cooldown < pygame.time.get_ticks():
            engine.buttons['return'].draw(window, self)
            if engine.buttons['return'].press(event):
                self.cooldown = 0 
                return True

    def write(self, text: str, window,
              x: int, y: int, centered = False) -> None:
        """Write text with depth."""
        
        GREY  = (180, 180, 180)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        # Text in shadow, highlight and body colour.
        _0 = self._myfont.render(text, 1, BLACK)
        _1 = self._myfont.render(text, 1, GREY)
        _2 = self._myfont.render(text, 1, WHITE)

        # Find text shape.
        _0_square = _0.get_rect()
        _1_square = _1.get_rect()
        _2_square = _2.get_rect()

        # Calculate shape centre and offset shadow and highlight.
        if centered:
            _0_square.center = (x + 3, y + 3)
            _1_square.center = (x - 1, y - 1)
            _2_square.center = (x, y)
        else:
            _0_square = (x + 3, y + 3)
            _1_square = (x -1 , y - 1)
            _2_square = (x, y)
        # Print graphic.
        window.blit(_0, _0_square)
        window.blit(_1, _1_square)
        window.blit(_2, _2_square)
    

class Button:
        """Clickable button."""
        def __init__(self, text: str, center_position: tuple[int],
                     size: tuple[int]) -> None:
            self.text = text
            self.button = pygame.Rect((0, 0), size)
            self.button.center = center_position # Center the rectangle.
            self.colour_base = (75, 75, 200)
            self.colour_hover = (0, 0, 100)
            self.click = pygame.mixer.Sound('./assets/audio/click.wav')
            self.hover = False
            self.held = False
        
        def draw(self, window, graphics: Graphics) -> None:
            """Draw the button."""
            if self.hover:
                button_colour = self.colour_hover
            else:
                button_colour = self.colour_base
            pygame.draw.rect(window, button_colour, self.button)
            graphics.write(self.text, window,
                            self.button.centerx, self.button.centery,
                            centered = True)

        def press(self, event: pygame) -> bool:
            """Returns True if clicked."""
            mouse = pygame.mouse.get_pos()
            if self.button.collidepoint(mouse):
                self.hover = True
            else:
                self.hover = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hover:
                    self.held = True
            if event.type == pygame.MOUSEBUTTONUP:        
                if self.hover and self.held:
                    self.click.play()
                    return True
                self.held = False
            