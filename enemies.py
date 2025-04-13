import random

import pygame
from pygame.math import Vector2
import math
from settings import *
from random import randint


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, img, game):
        super().__init__()
        normal_image = img
        hit_image = img
        heat_image = img
        shielded_img = img
        self.game = game
        self.sprites = []
        self.sprites.append(normal_image)
        self.sprites.append(hit_image)
        self.sprites.append(heat_image)
        self.sprites.append(hit_image)
        self.sprites.append(shielded_img)
        self.sprites.append(hit_image)
        self.current_sprite = 0
        self.sprite_first_frame = 0
        self.sprite_last_frame = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.hit = False
        # Stats
        self.pos = Vector2(pos)
        self.speed = 1
        self.hp = 1
        self.scrap = 1
        self.heat = 0
        self.collision_damage = 5
        self.weapon_type = "default"
        self.weapon_cooldown = 100
        self.weapon_damage = 0
        self.weapon_ready = False
        self.timer = 0


    def update(self, bullet_time):
        player = self.game.player.sprite  # Reference to player from Game
        direction = (player.pos - self.pos).normalize()
        self.pos += direction * self.speed * bullet_time
        angle = -direction.angle_to(Vector2(1, 0))
        self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], -angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)


        if self.hit:
            self.sprite_last_frame += 0.9
            self.hit = False
        if self.current_sprite >= self.sprite_last_frame:
            self.current_sprite = self.sprite_first_frame
            self.sprite_last_frame = self.sprite_first_frame
        self.timer += 0.99
        if self.timer > 2 * self.weapon_cooldown - self.weapon_cooldown * bullet_time:
            self.timer = 0
            self.weapon_ready = True
        self.destroy()

    def destroy(self):
        if self.rect.x <= -1000 or self.rect.x > SCREEN_WIDTH + 1000:
            self.kill()
        if self.rect.y <= -1000 or self.rect.y > SCREEN_HEIGHT + 1000:
            self.kill()
        if self.hp <= 0:
            self.kill()


class Bomber(Enemy):
    def __init__(self, pos, img, game):
        super().__init__(pos, img, game)
        normal_image = img
        hit_image = img
        heat_image = img
        shielded_img = img
        self.sprites = []
        self.sprites.append(normal_image)
        self.sprites.append(hit_image)
        self.sprites.append(heat_image)
        self.sprites.append(hit_image)
        self.sprites.append(shielded_img)
        self.sprites.append(hit_image)
        self.current_sprite = 0
        self.sprite_first_frame = 0
        self.sprite_last_frame = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.hit = False
        self.pos = pos
        # Stats
        self.behavior = "tactical"
        self.fire_distance_min = 400
        self.fire_distance_max = 700
        self.speed = 2
        self.hp = 25
        self.heat = 0
        self.collision_damage = 5
        self.weapon_type = "rocket"
        self.weapon_cooldown = 100
        self.weapon_damage = 10
        self.weapon_ready = False
        self.timer = self.weapon_cooldown
        self.scrap = randint(0,5)

    def update(self, bullet_time):
        player = self.game.player.sprite
        direction = (player.pos - self.pos).normalize()
        distance = self.pos.distance_to(player.pos)

        # TACTICAL: maintain firing range
        if distance < self.fire_distance_min:
            self.pos -= direction * self.speed * bullet_time  # retreat
        elif distance > self.fire_distance_max:
            self.pos += direction * self.speed * bullet_time  # approach slowly

        # Rotation
        angle = -direction.angle_to(Vector2(1, 0))
        self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], -angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        if self.hit:
            self.sprite_last_frame += 0.9
            self.hit = False
        if self.current_sprite >= self.sprite_last_frame:
            self.current_sprite = self.sprite_first_frame
            self.sprite_last_frame = self.sprite_first_frame

        # Weapon cooldown
        self.timer += 0.99
        if self.timer > 2 * self.weapon_cooldown - self.weapon_cooldown * bullet_time:
            self.timer = 0
            self.weapon_ready = True

        self.destroy()

class Scout(Enemy):
    def __init__(self, pos, img, game):
        super().__init__(pos, img, game)
        normal_image = img
        hit_image = img
        heat_image = img
        shielded_img = img
        self.sprites = []
        self.sprites.append(normal_image)
        self.sprites.append(hit_image)
        self.sprites.append(heat_image)
        self.sprites.append(hit_image)
        self.sprites.append(shielded_img)
        self.sprites.append(hit_image)
        self.current_sprite = 0
        self.sprite_first_frame = 0
        self.sprite_last_frame = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.hit = False
        self.pos = pos
        # Stats
        self.speed = 5
        self.hp = 10
        self.heat = 0
        self.collision_damage = 2
        self.weapon_type = "radar"
        self.weapon_cooldown = 150
        self.weapon_damage = 0
        self.weapon_ready = False
        self.timer = self.weapon_cooldown
        self.scrap = randint(0,2)




class Enemy_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, weapon_damage, scrap, image = None, target = None):
        super().__init__()
        self.image = pygame.Surface((16,5))
        self.image.fill("red")
        self.mask = pygame.mask.from_surface(self.image)
        self.org_pos = Vector2(pos)
        self.pos = self.org_pos
        self.rect = self.image.get_rect(center = pos)
        self.damage = weapon_damage
        self.speed = 8
        self.heat = 0
        self.scrap = scrap
        self.piercing = False
        self.target = Vector2((-50,self.rect.y))
        self.movement = self.target - self.org_pos

    def update(self, bullet_time):
        self.pos += self.movement.normalize() * self.speed * bullet_time
        self.rect.center = self.pos
        self.destroy()

    def destroy(self):
        if self.rect.x <= -300 or self.rect.x > SCREEN_WIDTH + 300:
            self.kill()
        if self.rect.y < -300 or self.rect.y > SCREEN_HEIGHT +300:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, img, img2):
        super().__init__()
        self.image1 = img
        self.image2 = img2
        self.image = self.image1.copy()
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.timer = 15
        self.frame = 0
        self.alpha = 255
        self.flash = True
        self.scale = 0.8
        
        # Stats
        self.damage = 5
        self.heat = 0.3
        self.piercing = False



    def update(self, bullet_time):
        self.frame += 1
        self.timer -= 1
        self.scale += 0.05
        self.alpha = max(0, self.alpha - 2)

        if self.flash:
            img = self.image1 if self.frame % 2 == 0 else self.image2
        else:
            img = self.image1

        scaled = pygame.transform.rotozoom(img, 0, self.scale)
        scaled.set_alpha(self.alpha)
        self.image = scaled
        self.rect = self.image.get_rect(center=self.pos)

        if self.timer <= 0:
            self.kill()

class Radar_ping(Enemy_projectile):
    def __init__(self, pos, weapon_damage, scrap, image, target):
        super().__init__(pos, weapon_damage, scrap, image, target)
        self.target = Vector2(target)
        self.org_pos = Vector2(pos)
        self.pos = self.org_pos
        self.movement = self.target - self.org_pos
        self.angle = math.degrees(math.atan2(-self.movement[1], self.movement[0]))
        self.image = pygame.transform.rotate(image, self.angle)
        self.image.set_alpha(110)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.damage = weapon_damage
        self.speed = 10
        self.heat = 0
        self.scrap = 0
        self.piercing = True

class Rocket(pygame.sprite.Sprite):
    def __init__(self, pos, target, img, game, img2, img3):
        super().__init__()
        self.game = game
        self.pos = Vector2(pos)
        self.target = target
        self.velocity = Vector2(0, 0)
        self.speed = 2  # starts slow
        self.max_speed = 10
        self.acceleration = 0.1
        self.turn_rate = 1.5
        self.hit = False

        # Visual
        self.image = img
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.explosion_img = img2
        self.explosion_img2 = img3

        # Damage/stats
        self.lifetime = 240
        self.hp = 6
        self.damage = 3
        self.heat = 0
        self.scrap = 0
        self.piercing = False

    def update(self, bullet_time):
        # Accelerate
        if self.speed < self.max_speed:
            self.speed += self.acceleration * bullet_time

        # Homing logic
        to_player = (self.target.pos - self.pos).normalize()
        desired_angle = Vector2(1, 0).angle_to(to_player)
        angle_diff = (desired_angle - self.angle + 180) % 360 - 180  # shortest turn
        angle_diff = max(-self.turn_rate, min(self.turn_rate, angle_diff))  # limit turn

        self.angle += angle_diff
        direction = Vector2(1, 0).rotate(self.angle)

        self.velocity = direction * self.speed * bullet_time
        self.pos += self.velocity

        # Rotate image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.explode()
            self.kill()
        self.destroy()

        if pygame.sprite.collide_mask(self, self.game.player.sprite):
            self.explode()
            self.kill()
            return

    def destroy(self):
        if not (-300 < self.rect.x < SCREEN_WIDTH + 300 and -300 < self.rect.y < SCREEN_HEIGHT + 300):
            self.kill()

    def explode(self):
        if hasattr(self, "_exploded"):
            return
        self._exploded = True
        explosion = Explosion(self.pos, self.explosion_img, self.explosion_img2)
        self.game.enemy_projectiles.add(explosion)

