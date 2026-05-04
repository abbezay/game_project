import pygame
import game

def main():
    # Create attributes for the first level.
    game.initiate_level()
    while game.running:
        game.clock.tick(60) # 60 fps.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
        game.loop()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('./assets/audio/background.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.display.set_caption('Platformer game TBD')
    game = game.Engine()
    main()