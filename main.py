import sys
import pygame
from random import randint
import enemies
import projectiles
from settings import *
from level import Level
from level import SmallStars
from level import BigStars
from player import Player
from enemies import Enemy


#background = pygame.image.load("assets/background_nebula.jpg")
#background = pygame.transform.scale(background, (1500,1500))
#background.set_alpha(50)


pygame.init()
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.smallstars = SmallStars()
        self.stars = pygame.sprite.Group()
        self.bigstars = BigStars()
        self.bstars = pygame.sprite.Group()

        # Player ship (position, level boundaries, speed)
        player_sprite = Player((SCREEN_WIDTH /6, SCREEN_HEIGHT /2), SCREEN_WIDTH, SCREEN_HEIGHT, 10)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.enemies = pygame.sprite.Group()
        self.enemy_spawn() # Here list of enemies depending on level. MOVE THIS TO RUN()

    def enemy_spawn(self):
        randompos = randint(50,900)
        randomspeed = randint(3,7)
        enemy_sprite = Enemy((2000,randompos), randomspeed)
        self.enemies.add(enemy_sprite)



    def collision_checks(self):

        if self.player.sprite.projectiles:
            for projectile in self.player.sprite.projectiles:
                if (pygame.sprite.spritecollide(projectile, self.enemies, True, collided=pygame.sprite.collide_mask)):
                    projectile.kill()




    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == COUNTDOWN:
                    Game.enemy_spawn(self)
            self.screen.fill("black")
            dt = self.clock.tick(fps)
            self.level.run(dt)

            if len(self.stars.sprites()) < 100:
                self.stars.add(SmallStars())
            self.stars.draw(self.screen)
            self.stars.update()
            if len(self.bstars.sprites()) < 3:
                self.bstars.add(BigStars())
            self.bstars.draw(self.screen)
            self.bstars.update()

            self.player.sprite.projectiles.draw(self.screen)
            self.player.update()
            self.player.draw(self.screen)

            self.enemies.draw(self.screen)
            self.enemies.update()
            self.collision_checks()
            pygame.display.update()

current_time = pygame.time.get_ticks()

COUNTDOWN = pygame.USEREVENT + 1
pygame.time.set_timer(COUNTDOWN, 1000)


if __name__ == "__main__":
    game = Game()
    game.run()