import sys
import pygame
from random import randint
from projectiles import Projectile
from settings import *
from player import Player
from enemies import Enemy
from enemies import Bomber
from enemies import Enemy_projectile
from level import Level
from level import SmallStars
from level import BigStars
from ui import UI

# Things to do:
# Build classes for all units
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

img_dict = {}
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

        # Load all images
        self.load_image("bomber1", (120, 120))
        self.load_image("bomber2", (120, 120))

        # Init player and enemy groups.
        player_sprite = Player((SCREEN_WIDTH /6, SCREEN_HEIGHT /2), SCREEN_WIDTH, SCREEN_HEIGHT, 10)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.enemies = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.bomber = pygame.sprite.Group()

        # Init background effects and UI
        self.smallstars = SmallStars()
        self.bigstars = BigStars()
        self.hp_bar = UI(self.screen,(30, 860))
        self.en_bar = UI(self.screen,(30, 895))
        self.oc_bar = UI(self.screen,(330, 894))
        self.shield_bar = UI(self.screen,(30, 930))
        self.heat_bar = UI(self.screen,(30, 965))
        self.counter_1 = UI(self.screen,(380,860))
        self.counter_2 = UI(self.screen, (380, 895))
        self.counter_3 = UI(self.screen, (380, 930))
        self.counter_4 = UI(self.screen, (380, 965))

    def load_image(self, image_name, scale):
        image = pygame.image.load(f"assets/{image_name}.png").convert_alpha()
        resized = pygame.transform.scale(image, scale)
        img_dict[image_name] = resized


    def enemy_spawn(self):
        randompos = randint(50,850)
        randomspeed = randint(3,7)
        #enemy_sprite = Enemy((1700, randompos), 1, "ice", 100, 20, "CannonLaserRocket", 200)
        #self.enemies.add(enemy_sprite)
        sprite2 = Bomber((1900, randompos), img_dict["bomber1"], img_dict["bomber2"])
        self.enemies.add(sprite2)

        #for x in self.level.queue1:
        #    new = Enemy(*x)
        #    self.enemies.add(new)

    def collision_checks(self):
        enemy_hit_dict = pygame.sprite.groupcollide(self.enemies, self.player.sprite.projectiles, False, False, pygame.sprite.collide_mask)
        player_hit_dict = pygame.sprite.groupcollide(self.player, self.enemies, False, False, pygame.sprite.collide_mask)
        for enemy, projectiles in enemy_hit_dict.items():
            # Deal damage to the enemy for each projectile that hit it
            for projectile in projectiles:
                enemy.hp -= projectile.damage
                enemy.hit = True
                if not projectile.piercing:
                    projectile.kill()
                if enemy.hp <= 0:
                    enemy.kill()
        for player, enemies in player_hit_dict.items():
            for enemy in enemies:
                player.hp -= enemy.collision_damage
                enemy.hp -= 10
                player.energy += 100
                if enemy.hp <= 0:
                    enemy.kill()

    def enemy_fire(self):
        for enemy in self.enemies:
            if enemy.weapon_ready == True:
                fire = Enemy_projectile(enemy.pos, -6)
                self.enemy_projectiles.add(fire)
                enemy.weapon_ready = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == ENEMY_SPAWN_COUNTDOWN:
                    self.enemy_spawn()
            self.screen.fill("black")
            dt = self.clock.tick(fps)
            self.level.run(dt)
            self.level.small_stars.draw(self.screen)
            self.level.big_stars.draw(self.screen)
            self.enemies.update()
            self.enemies.draw(self.screen)
            self.enemy_projectiles.update()
            self.enemy_projectiles.draw(self.screen)
            self.enemy_fire()
            self.bomber.update()

            self.player.update()
            self.player.draw(self.screen)
            self.player.sprite.projectiles.draw(self.screen)
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
pygame.time.set_timer(ENEMY_SPAWN_COUNTDOWN, 3000)


if __name__ == "__main__":
    game = Game()
    game.run()