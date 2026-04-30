import pygame

"""
This is a prototype for how to detect collisions between the player and
the level tiles, and how jumping logic can be implemented in the project.

To test:
    MOVE with wasd keys.
    SPACE to change to next test level.
    Exit game with Alt+F4, Ctrl+C in console or pressing X on the window.

Levels:
    1: Perfect fit collision while allowing all direction keys simultaniously.
    2: Jumping with perfect collision fits and cancelled jumps on collision.
    3: Open level to test jump height/speed.

Note:
    If prototype is running fast / slow, try changing clock.tick() or
    self.speed.
"""


class Engine:
    def __init__(self) -> None:
        self.size = self.width, self.height = 800, 600
        self.window = pygame.display.set_mode(self.size)
        self.running = True
        self.player = pygame.Rect([50, 50, 50, 50]) # Coordinates, size.
        # For this prototype, speed must align with the 50 unit grid.
        # Example: 1, 5, 10, 25, 50.
        self.speed = 5
        self.jumping = False
        self.landed = True
        self.jump_time = 0 # Creates the time it takes to complete a jump.
        self.jump_time_offset = 225 # How long the jump is active.
        self.level = 0 # Switch between the three levels with SPACE.
        # In the future, these levels will be saved in a .txt file.
        self.levels = [
                        [ # Collision.
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                            [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
                            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                            [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                        ],
                        [ # Gravity and jumping.
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
                            [1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                            [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
                            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                        ],
                        [ # Empty jumping test.
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                        ]
                    ]


    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption('Collision prototype')
        clock = pygame.time.Clock()
        # Creates first level.
        blocks = self.create_blocks()
        while self.running:
            clock.tick(60)
            # Close the game.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Switch between levels / tests.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        blocks = self.change_level(blocks)
            self.loop(blocks)
            self.render(blocks)


    def change_level(self, blocks: tuple[object, ...]) -> tuple[object, ...]:
        """
        Switches test level and sets the player at an appropriate location.
        """
        self.level += 1
        if self.level == len(self.levels):
            self.level = 0

        # Reset player position.
        self.player.x, self.player.y = 50, 500
        # Creates new level.
        return self.create_blocks()


    def render(self, blocks: tuple[object, ...]) -> None:
        """Displays the graphics."""
        # Background.
        self.window.fill((0, 0, 0))
        # Level.
        for i in blocks:
            pygame.draw.rect(self.window, (255, 0, 0), i)
        # Player.
        pygame.draw.rect(self.window, (0, 255, 0), self.player, width = 20)
        # Update.
        pygame.display.flip()


    def loop(self, blocks: tuple[object, ...]) -> None:
        """
        Takes keyboard inputs to move the player
        and calls gravity() and jump() when conditions are set
        """
        key = pygame.key.get_pressed()
        if self.level == 0:
            # Left.
            if key[pygame.K_a]:
                 # Create copy of player square in its current position.
                test = self.player.copy()
                # Move copy to where the player would move.
                test.x -= self.speed
                # If the copy does not collide with an object..
                if test.collidelist(blocks) == -1:
                    # ..it is safe to move the player.
                    self.player.x -= self.speed
            # Right.
            if key[pygame.K_d]:
                test = self.player.copy()
                test.x += self.speed
                if test.collidelist(blocks) == -1:
                    self.player.x += self.speed
            # Up.
            if key[pygame.K_w]:
                test = self.player.copy()
                test.y -= self.speed
                if test.collidelist(blocks) == -1:
                    self.player.y -= self.speed
            # Down.
            if key[pygame.K_s]:
                test = self.player.copy()
                test.y += self.speed
                if test.collidelist(blocks) == -1:
                    self.player.y += self.speed


        ## Test two. Gravity and jumping.
        elif self.level == 1 or self.level == 2:
            # Gravity is active when not jumping.
            if self.jumping == False:
                self.gravity(blocks)
            if self.jumping == True:
                self.jump(blocks)
            # Left.
            if key[pygame.K_a]:
                test = self.player.copy()
                test.x -= self.speed
                if test.collidelist(blocks) == -1:
                    self.player.x -= self.speed
            # Right.
            if key[pygame.K_d]:
                test = self.player.copy()
                test.x += self.speed
                if test.collidelist(blocks) == -1:
                    self.player.x += self.speed
            # Jump!
            if key[pygame.K_w]:
                if self.jumping == False and self.landed == True:
                    self.jumping = True
                    # Take the current time and add the offset in milliseconds.
                    self.jump_time = pygame.time.get_ticks() + self.jump_time_offset


    def gravity(self, blocks: tuple[object, ...]) -> None:
            """
            Pulls the player down to the ground when not jumping.

            Sets landed as true once in contact with ground.
            """
            test = self.player.copy()
            test.y += self.speed
            if test.collidelist(blocks) == -1:
                self.landed = False
                self.player.y += self.speed
            else:
                self.landed = True


    def jump(self, blocks: tuple[object, ...]) -> None:
        """
        Moves the player upwards until the time of the jump has expired
        or the test object collides with an object.
        
        Movement changes depending on how long the jump has gone on for.
        
        TODO :: Find a solution which gradually alters speed depending
        on duration, potentially through multiplications.
        """

        # Set landed as false while jumping, disallowing additional jumps.
        self.landed = False 
        if pygame.time.get_ticks() < self.jump_time:
            test = self.player.copy()
            test.y -= self.speed
            if test.collidelist(blocks) == -1:
                self.player.y -= self.speed
            else: # If colliding with Rect object, stops jump.
                self.jumping = False
        else: # If jump duration has passed, stop jump.
                self.jumping = False
    

    def create_blocks(self) -> tuple[object, ...]:
        """
        Iterate over array (list of lists) and create Rect object
        at the coordinates for 1 or leave blank if 0.

        Returns the tuple of objects to allow for confirming collisions.
        """
        edge = [] # Populate with pygame.Rect objects.
        x, y = 0, 0 # Determines where Rectangles are placed.
        for i in self.levels[self.level]:
            for ii in i:
                if ii == 1:
                    rect = pygame.Rect(x, y, 50, 50)
                    edge.append(rect)
                x += 50 # Shift x-origin for next rectangle.
            x = 0 # Resets after a row is finished.
            y += 50 # Shifts y-origin for next row of rectangles.
        return tuple(edge) # Returns tuple of objects.


if __name__ == '__main__':
    game = Engine()
    game.run()