import random
import sys
import pygame
from pygame.math import Vector2
from random import randint
from projectiles import Projectile
from settings import *
from player import Player
from enemies import Enemy, Bomber, Scout, Enemy_projectile, Scrap, Radar_ping
from neutrals import Neutrals, Asteroid, Rock
from level import Level, SmallStars, BigStars
from ui import UI


pygame.init()

img_dict = {}

random_number = (40,80)
class Game:
    def __init__(self, screen):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

        # Load all images
        self.load_image("player-scout1", (110, 110))
        self.load_image("player-scout2", (110, 110))
        self.load_image("player-scout3", (110, 110))
        self.load_image("player-scout4", (110, 110))
        self.load_image("player-scout5", (110, 110))

        # enemies
        self.load_image("bomber1", (110, 110))
        self.load_image("bomber2", (110, 110))
        self.load_image("scout1", (100, 100))
        self.load_image("ping", (400, 200))

        # neutrals
        self.load_image("star1", (60, 60))
        self.load_image("star2", (70, 70))
        self.load_image("star3", (80, 80))
        self.load_image("asteroid1", (100, 100))
        self.load_image("asteroid2", (100, 100))
        self.load_image("asteroid3", (100, 100))
        self.load_image("asteroid4", (100, 100))
        self.load_image("rock1", (45, 45))
        self.load_image("rock2", (30, 30))
        self.load_image("rock3", (35, 35))

        # UI
        self.load_image("generator", (300, 300))



        # Init player and enemy groups.
        player_sprite = Player((300,500), img_dict["player-scout1"], img_dict["player-scout2"], img_dict["player-scout3"], img_dict["player-scout4"], img_dict["player-scout5"], SCREEN_WIDTH, SCREEN_HEIGHT, 7)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.bullet_time = 1

        self.neutrals = pygame.sprite.Group()

        self.enemies = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()

        # Init background effects and UI
        small_star = SmallStars()
        self.small_stars = pygame.sprite.Group(small_star)
        big_star = BigStars(img_dict["star1"], img_dict["star2"], img_dict["star3"])
        self.big_stars = pygame.sprite.Group(big_star)
        self.hp_bar = UI(self.screen,(30, 860))
        self.en_bar = UI(self.screen,(30, 895))
        self.oc_bar = UI(self.screen,(330, 894))
        self.shield_bar = UI(self.screen,(30, 930))
        self.heat_bar = UI(self.screen,(30, 965))
        self.counter_1 = UI(self.screen,(270,860))
        self.counter_2 = UI(self.screen, (270, 895))
        self.counter_3 = UI(self.screen, (270, 930))
        self.counter_4 = UI(self.screen, (270, 965))

    def load_image(self, image_name, scale):
        image = pygame.image.load(f"assets/{image_name}.png").convert_alpha()
        resized = pygame.transform.scale(image, scale)
        img_dict[image_name] = resized


    def spawn(self):
        random_number = randint(0,50)
        randompos = randint(40,970)
        bomber = Bomber((1750, randompos), img_dict["bomber1"], img_dict["bomber2"], img_dict["bomber2"], img_dict["bomber2"])
        self.enemies.add(bomber)
        if random_number > 45:
            asteroid = Asteroid((1750, randompos), img_dict["asteroid1"], img_dict["asteroid2"], img_dict["asteroid3"], img_dict["asteroid4"])
            self.neutrals.add(asteroid)
        elif random_number > 40:
            rand_rock = random.choice(["rock1", "rock2", "rock3"])
            rock = Rock((1750, randompos), img_dict[rand_rock], img_dict[rand_rock], img_dict[rand_rock], img_dict[rand_rock])
            self.neutrals.add(rock)
        elif random_number > 1:
            scout = Scout((1750, randompos), img_dict["scout1"], img_dict["scout1"], img_dict["scout1"], img_dict["scout1"])
            self.enemies.add(scout)

    def enemy_fire(self):
        for enemy in self.enemies:
            if enemy.weapon_ready == True:
                if enemy.weapon_type == "standard":
                    attack = Enemy_projectile(enemy.rect.center, enemy.weapon_damage, 0)
                    self.enemy_projectiles.add(attack)
                    enemy.weapon_ready = False
                elif enemy.weapon_type == "radar":
                    if enemy.rect.x > self.player.sprite.rect.x:
                        radar = Radar_ping(enemy.rect.center, enemy.weapon_damage, 0, img_dict["ping"], self.player.sprite.rect.center)
                        self.enemy_projectiles.add(radar)
                        enemy.weapon_ready = False



    def collision_checks(self):
        player_hitting_enemies = pygame.sprite.groupcollide(self.enemies, self.player.sprite.projectiles, False, False, pygame.sprite.collide_mask)
        player_hitting_neutrals = pygame.sprite.groupcollide(self.neutrals, self.player.sprite.projectiles, False, False, pygame.sprite.collide_mask)
        player_crashing_enemies = pygame.sprite.groupcollide(self.player, self.enemies, False, False, pygame.sprite.collide_mask)
        player_crashing_neutrals = pygame.sprite.groupcollide(self.player, self.neutrals, False, False, pygame.sprite.collide_mask)
        enemies_hitting_player = pygame.sprite.groupcollide(self.player, self.enemy_projectiles, False, False, pygame.sprite.collide_mask)

        for enemy, projectiles in player_hitting_enemies.items():
            for projectile in projectiles:
                enemy.hp -= projectile.damage + projectile.damage * (enemy.heat/100)
                enemy.hit = True
                if enemy.heat < 100:
                    enemy.heat += projectile.heat
                if not projectile.piercing:
                    projectile.kill()
                if enemy.hp <= 0:
                    enemy.destroy()
                    if enemy.scrap > 0:
                        scrap_spawn = Scrap(enemy.rect.center, 0, enemy.scrap)
                        self.enemy_projectiles.add(scrap_spawn)
        for neutral, projectiles in player_hitting_neutrals.items():
            for projectile in projectiles:
                neutral.hp -= projectile.damage + projectile.damage * (neutral.heat / 100)
                neutral.hit = True
                if neutral.heat < 100:
                    neutral.heat += projectile.heat
                if not projectile.piercing:
                    projectile.kill()
                if neutral.hp <= 0:
                    neutral.kill()
        for player, enemies in player_crashing_enemies.items():
            for enemy in enemies:
                player.hp -= enemy.collision_damage
                enemy.hp -= 10
                if enemy.hp <= 0:
                    enemy.kill()
        for player, neutrals in player_crashing_neutrals.items():
            for neutral in neutrals:
                player.hp -= neutral.damage
                neutral.hp -= 10
                if neutral.hp <= 0:
                    neutral.kill()
        for player, enemy_projectiles in enemies_hitting_player.items():
            for projectile in enemy_projectiles:
                player.hp -= projectile.damage + projectile.damage * (player.heat/100)
                player.hit = True
                player.scrap += projectile.scrap
                if not projectile.piercing:
                    projectile.kill()
                if player.heat < 100:
                    player.heat += projectile.heat




    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == THREE_SECONDS:
                    self.spawn()
                    if len(self.big_stars.sprites()) < 2:
                        self.big_stars.add(BigStars(img_dict["star1"], img_dict["star2"], img_dict["star3"]))
            self.screen.fill("black")
            dt = self.clock.tick(fps)
            self.level.run(dt)
            self.collision_checks()
            self.bullet_time = self.player.sprite.bullet_time
            # Background
            if len(self.small_stars.sprites()) < 100:
                self.small_stars.add(SmallStars())
            self.big_stars.update(self.bullet_time)
            self.small_stars.update(self.bullet_time)
            self.big_stars.draw(self.screen)
            self.small_stars.draw(self.screen)

            #Player, enemies, neutrals
            self.enemies.update(self.bullet_time)
            self.enemies.draw(self.screen)
            self.enemy_projectiles.update(self.bullet_time)
            self.enemy_projectiles.draw(self.screen)
            self.enemy_fire()
            self.neutrals.update(self.bullet_time)
            self.neutrals.draw(self.screen)
            self.player.update()
            self.player.draw(self.screen)
            self.player.sprite.projectiles.draw(self.screen)

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

THREE_SECONDS = pygame.USEREVENT + 1
pygame.time.set_timer(THREE_SECONDS, 2000)


if __name__ == "__main__":
    game = Game()
    game.run()