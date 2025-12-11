import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    dt = 0

    updatable = pygame.sprite.Group(player)
    drawable = pygame.sprite.Group(player)
    asteroids = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)

    asteroidField = AsteroidField()

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)

        for asteroid in asteroids:
            if player.collide_with(asteroid):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()

        screen.fill("black")
            
        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()