import sys
import pygame
from random import randint
from projectiles import Projectile
from settings import *
from level import Level
from player import Player
from enemies import Enemy
from level import SmallStars
from level import BigStars
from ui import UI

# Things to do:
# Make OC bar charge left.
# Give weapons restrictions and recharge bonus from energy. Supercharge.
# Give background objects bonuses, like energy from stars.
# Build device constructor.
# Build spawner settings in Level. Replace that crappy ENEMY_SPAWN_COUNTDOWN.
# Move projectiles.enemy_projectiles to Enemy.
# Add rocks as Enemy.
# Build GUI
# Bullets-player collisions
# Enemy-player collisions

pygame.init()
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        # Player ship (position, level boundaries, speed)
        player_sprite = Player((SCREEN_WIDTH /6, SCREEN_HEIGHT /2), SCREEN_WIDTH, SCREEN_HEIGHT, 10)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.enemies = pygame.sprite.Group()
        self.smallstars = SmallStars()
        self.bigstars = BigStars()
        self.hp_bar = UI(self.screen,(80, 860))
        self.en_bar = UI(self.screen,(80, 895))
        self.oc_bar = UI(self.screen,(380, 894))
        self.shield_bar = UI(self.screen,(80, 930))
        self.heat_bar = UI(self.screen,(80, 965))
        self.counter_1 = UI(self.screen,(460,860))
        self.counter_2 = UI(self.screen, (460, 895))
        self.counter_3 = UI(self.screen, (460, 930))
        self.counter_4 = UI(self.screen, (460, 965))

    def enemy_spawn(self):
        randompos = randint(50,900)
        randomspeed = randint(3,7)
        enemy_sprite = Enemy((2000, randompos), randomspeed, "heavy-fighter", 150, 20, "CannonLaserRocket", 200)
        self.enemies.add(enemy_sprite)

    def collision_checks(self):
        enemy_hit_dict = pygame.sprite.groupcollide(self.enemies, self.player.sprite.projectiles, False, False, pygame.sprite.collide_mask)
        player_hit_dict = pygame.sprite.groupcollide(self.player, self.enemies, False, False, pygame.sprite.collide_mask)
        for enemy, projectiles in enemy_hit_dict.items():
            # Deal damage to the enemy for each projectile that hit it
            for projectile in projectiles:
                enemy.hp -= projectile.damage
                if not projectile.piercing:
                    projectile.kill()
                if enemy.hp <= 0:
                    enemy.kill()
        for player, enemies in player_hit_dict.items():
            for enemy in enemies:
                player.hp -= enemy.hp / 3
                enemy.hp -= player.hp / 100
                player.energy += 100
                if enemy.hp <= 0:
                    enemy.kill()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == ENEMY_SPAWN_COUNTDOWN:
                    Game.enemy_spawn(self)
            self.screen.fill("black")
            dt = self.clock.tick(fps)
            self.level.run(dt)
            self.level.small_stars.draw(self.screen)
            self.level.big_stars.draw(self.screen)
            self.player.sprite.projectiles.draw(self.screen)
            self.enemies.update()
            self.enemies.draw(self.screen)
            self.player.update()
            self.player.draw(self.screen)
            self.collision_checks()
            # UI
            self.hp_bar.show_hp(self.player.sprite.hp, 100)
            self.en_bar.show_en(self.player.sprite.energy, self.player.sprite.max_energy)
            self.oc_bar.show_oc(self.player.sprite.energy, self.player.sprite.max_energy)
            self.shield_bar.show_shield(self.player.sprite.shield, 100)
            self.heat_bar.show_heat(self.player.sprite.heat, 100)
            self.counter_1.counter_hp(self.player.sprite.hp)
            self.counter_2.counter_en(self.player.sprite.energy)
            self.counter_3.counter_shield(self.player.sprite.shield)
            self.counter_4.counter_heat(self.player.sprite.heat)
            pygame.display.update()

current_time = pygame.time.get_ticks()

ENEMY_SPAWN_COUNTDOWN = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SPAWN_COUNTDOWN, 1000)

#REFRESH =

if __name__ == "__main__":
    game = Game()
    game.run()