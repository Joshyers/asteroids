import pygame
import sys
import random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    dt = 0

    updatable = pygame.sprite.Group(player)
    drawable = pygame.sprite.Group(player)
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    asteroidField = AsteroidField()

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)

        for shot in shots:
            for asteroid in asteroids:
                if shot.collide_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.kill()
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        pass
                    log_event("asteroid_split")
                    random_angle = random.uniform(20, 50)
                    new_vector = asteroid.velocity.rotate(random_angle)
                    new_vector_2 = asteroid.velocity.rotate(-random_angle)
                    new_radius = asteroid.radius - ASTEROID_MIN_RADIUS
                    asteroid_1 = Asteroid(asteroid.position.x, asteroid.position.y, new_radius)
                    asteroid_1.velocity = new_vector
                    asteroid_2 = Asteroid(asteroid.position.x, asteroid.position.y, new_radius)
                    asteroid_2.velocity = new_vector_2


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