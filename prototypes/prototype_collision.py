import pygame

class Engine:
    def __init__(self) -> None:
        self.size = self.width, self.height = 800, 600
        self.window = pygame.display.set_mode(self.size)
        self.running = True
        self.player = pygame.Rect([100, 100, 100, 100])
        self.jumping = False
        self.landed = True
        self.jump_time = 0
        self.level = 0
        self.levels = [
                        [ # Collision.
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 1, 1, 1, 0, 1, 1],
                            [1, 0, 1, 0, 1, 0, 1, 1],
                            [1, 0, 0, 0, 1, 0, 0, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1]
                        ],
                        [ # Gravity and jumping.
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 1, 1, 0, 1],
                            [1, 0, 0, 1, 1, 1, 0, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1]
                        ]
                    ]

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption('Collision prototype')
        clock = pygame.time.Clock()
        clock.tick(60)
        blocks = self.create_blocks()
        while self.running:
            # Close the game.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Switch between levels / tests.
                # Only activated once per key input.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.level == 0:
                            self.level = 1
                            blocks = self.create_blocks()
                                # Reset player position.
                            self.player.x, self.player.y = 100, 100
                        else:
                                self.level = 0
                                blocks = self.create_blocks()
                                self.player.x, self.player.y = 100, 100
                    # The only way I can get jump to be responsive
                    # and not break the other events.
                    # TODO :: Find a solution!
                    # BUG :: Infinite jumps as self.jumping resets to False during jump.
                    if self.level == 1:
                        if event.key == pygame.K_w:
                            if self.landed and not self.jumping:
                                self.jumping = True
                                self.jump_time = pygame.time.get_ticks() + 250
                                
            self.loop(blocks)
            self.render(blocks)

    def render(self, blocks: tuple[object, ...]) -> None:
        """Just displays the graphics, does not provide any logic."""
        # Background.
        self.window.fill((0, 0, 0))
        # Level.
        for i in blocks:
            pygame.draw.rect(self.window, (150, 0, 0), i)
        # Player.
        pygame.draw.rect(self.window, (0, 150, 0), self.player, width = 40)
        # Update.
        pygame.display.flip()

    def loop(self, blocks: tuple[object, ...]) -> None:
        
        key = pygame.key.get_pressed()
        
        # Test one: collision and smooth runnings.
        if self.level == 0:
            ## Approach one, with a funny bug. Try it!
            # collision = player.collidelist(edge)
            # if key[pygame.K_a]:
            #     player.x -= 1
            #     if collision != -1:
            #         player.x += 10
            # if key[pygame.K_d]:
            #     player.x += 1
            #     if collision != -1:
            #         player.x -= 10
            # if key[pygame.K_w]:
            #     player.y -= 1
            #     if collision != -1:
            #         player.y += 10
            # if key[pygame.K_s]:
            #     player.y += 1
            #     if collision != -1:
            #         player.y -= 10

            ## Approach two, check collision before.
            if key[pygame.K_a]:
                test = self.player.copy() # Create copy of player square.
                test.x -= 1 # Move copy.
                if test.collidelist(blocks) == -1: # If copy does not collide
                                                # with any object in the list..
                    self.player.x -= 1 # ..move player.
            if key[pygame.K_d]:
                test = self.player.copy()
                test.x += 1
                if test.collidelist(blocks) == -1:
                    self.player.x += 1
            if key[pygame.K_w]:
                test = self.player.copy()
                test.y -= 1
                if test.collidelist(blocks) == -1:
                    self.player.y -= 1
            if key[pygame.K_s]:
                test = self.player.copy()
                test.y += 1
                if test.collidelist(blocks) == -1:
                    self.player.y += 1


        ## Test two. Gravity and jumping.
        elif self.level == 1:
            if self.jumping == False:
                self.gravity(blocks)
            if self.jumping == True:
                self.jump(blocks)
                
            if key[pygame.K_a]:
                test = self.player.copy() # Create copy of player square.
                test.x -= 1 # Move copy.
                if test.collidelist(blocks) == -1: # If copy does not collide
                                                # with any object in the list..
                    self.player.x -= 1 # ..move player.
            if key[pygame.K_d]:
                test = self.player.copy()
                test.x += 1
                if test.collidelist(blocks) == -1:
                    self.player.x += 1
            # Jump!
            ## First attempt. Can hold button for infinite height.
            # if key[pygame.K_w]:
            #     self.jumping = True
            #     self.jump_time = pygame.time.get_ticks() + 250

            ## Second attempt. Can only trigger once.
            ## Calling event.get() again breaks other code which uses event.
            # if self.jumping == False:
            #   for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.type == pygame.K_SPACE:
            #             print('True')
            #             self.jumping = True
            #             self.jump_time = pygame.time.get_ticks() + 250

                

    def gravity(self, blocks: tuple[object, ...]) -> None:
            test = self.player.copy()
            test.y += 1
            if test.collidelist(blocks) == -1:
                self.player.y += 1
        
    def jump(self, blocks: tuple[object, ...]) -> None:
        self.landed = False
        if pygame.time.get_ticks() < self.jump_time:
            test = self.player.copy()
            test.y -= 1
            if test.collidelist(blocks) == -1:
                self.player.y -= 1
            else: # If colliding with Rect object, stops jump.
                self.jumping = False
                self.landed = True
        else: # If jump duration has passed, stop jump.
                self.jumping = False
                self.landed = True
    
    def create_blocks(self) -> tuple[object, ...]:
        """Iterate over array (list of lists) and create Rect object
        at the coordinates for 1 or leave blank if 0.
        Returns the list of objects to allow for confirming collisions."""
        edge = [] # Populate with pygame.Rect objects.
        x, y = 0, 0 # Determines where Rectangles are placed.
        for i in self.levels[self.level]:
            for ii in i:
                if ii == 1:
                    rect = pygame.Rect(x, y, 100, 100)
                    edge.append(rect)
                x += 100 # Shift x-origin for next rectangle.
            x = 0 # Resets after a row is finished.
            y += 100 # Shifts y-origin for next row of rectangles.
        return tuple(edge) # Returns tuple of objects.


if __name__ == '__main__':
    game = Engine()
    game.run()