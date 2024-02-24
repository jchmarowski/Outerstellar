import sys, pygame
from settings import *
from game import Game

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
game = Game(screen)

pygame.init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill("black")
    game.run()
    pygame.display.update()
    clock.tick(60)

# Things to do:

# Sort out UI. Add scrap counter.
# Enemies dont have heat sprite animation.
# Add bounce to crashes with enemies and neutrals
# Add stage stages: combat-slow, combat-heavy, combat-environment, combat-boss.
# Add game status: menu, play, space-station, world map.
# When dead restart stage.
# Add targeting - vector2? Plus homing for missiles.
# Build classes for all units.
# Make OC bar charge left.
# Build device constructor. >_<
# Bullet Time is working ok at 0.55, just needs command to activate it. Line 58

# from pygame.math import Vector2