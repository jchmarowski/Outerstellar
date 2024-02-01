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

# Enemies dont have heat sprite animation.
# Add bounce to crashes with enemies and neutrals
# Add game stages: combat-slow, combat-heavy, combat-environment, combat-boss, space-station.
# When dead restart stage.
# Add targeting - vector2? Plus homing for missiles.
# Build classes for all units.
# Make OC bar charge left.
# Give weapons restrictions and recharge bonus from energy. Supercharge.
# Build device constructor. >_<
# Build spawner settings in Level.
# Add comets, but as enemy or neutral?
# Bullet Time is working ok at 0.4, just needs command to activate it. Line 58
# World map? (im getting carried away...)