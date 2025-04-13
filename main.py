import sys, pygame
from settings import *
from game import Game

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game = Game(screen)

pygame.init()
game.run()
clock.tick(60)