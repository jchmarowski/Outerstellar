import pygame
from pygame.math import Vector2
from weaponsbase import WeaponBase
from settings import *
import random

class Blaster(WeaponBase): # <><><><><><>_____ Rapid fire _____<><><><><><>
    def __init__(self, img_dict):
        self.type = "weapon"
        self.name = "blaster"
        self.img_dict = img_dict
        self.cooldown = 50
        self.last_fired = 0

    def get_energy_cost(self):
        return 1

    def fire(self, pos, direction, group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fired < self.cooldown:
            return 0
        self.last_fired = current_time

        projectile = self.img_dict["blaster_proj"]

        group.add(BlasterProj(pos, direction, projectile))
        group.add(BlasterFlash(pos + direction * 25, direction, self.img_dict))
        return self.get_energy_cost()

class BlasterProj(pygame.sprite.Sprite):
    def __init__(self, pos, direction, img):
        super().__init__()
        self.original_image = img
        self.image = self.rotate_image(direction)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.direction = direction.normalize()
        self.speed = 25
        self.damage = 5
        self.heat = 1
        self.piercing = False

    def rotate_image(self, direction):
        angle = direction.angle_to(Vector2(1, 0))
        return pygame.transform.rotate(self.original_image, angle)

    def update(self):
        self.pos += self.direction * self.speed
        self.image = self.rotate_image(self.direction)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.x < -100 or self.rect.x > SCREEN_WIDTH + 100 or self.rect.y < -100 or self.rect.y > SCREEN_HEIGHT + 100:
            self.kill()


class BlasterFlash(pygame.sprite.Sprite):
    def __init__(self, pos, direction, img_dict):
        super().__init__()
        variant = random.choice(["blaster_flash1", "blaster_flash2", "blaster_flash3"])
        self.original_image = img_dict[variant]
        self.image = self.rotate_image(direction)
        self.alpha = random.randint(200, 255)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.direction = direction.normalize()

        self.damage = 0
        self.heat = 1
        self.speed = random.randint(2,6)
        self.piercing = False

    def rotate_image(self, direction):
        angle = direction.angle_to(Vector2(1, 0))
        rotated = pygame.transform.rotate(self.original_image, angle)
        return rotated

    def update(self):
        self.alpha -= 30
        self.pos += self.direction * self.speed
        self.image = self.rotate_image(self.direction)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        if self.alpha <= 0:
            self.kill()

class Cannon(WeaponBase): # <><><><><><>_____ High power, slow firing _____<><><><><><>
    def __init__(self, img_dict):
        self.type = "weapon"
        self.name = "cannon"
        self.img_dict = img_dict
        self.cooldown = 500
        self.last_fired = 0

    def get_energy_cost(self):
        return 20

    def fire(self, pos, direction, group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fired < self.cooldown:
            return 0
        self.last_fired = current_time
        group.add(CannonProj(pos, direction, self.img_dict["cannon_proj"]))

        perp = direction.rotate(90) * 25
        forward = direction * 45

        pos_front = pos + forward
        pos_left = pos + forward + perp
        pos_right = pos + forward - perp

        group.add(CannonFlashFront(pos_front, direction, self.img_dict["cannon_flash_f"]))
        group.add(CannonFlashSide(pos_left, direction, self.img_dict["cannon_flash_l"], drift_dir=1))
        group.add(CannonFlashSide(pos_right, direction, self.img_dict["cannon_flash_r"], drift_dir=-1))

        return self.get_energy_cost()

class CannonProj(pygame.sprite.Sprite):
    def __init__(self, pos, direction, img):
        super().__init__()
        self.original_image = img
        self.image = self.rotate_image(direction)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.direction = direction.normalize()
        self.speed = 45
        self.damage = 5
        self.heat = 1
        self.piercing = True

    def rotate_image(self, direction):
        angle = direction.angle_to(Vector2(1, 0))
        return pygame.transform.rotate(self.original_image, angle)

    def update(self):
        self.pos += self.direction * self.speed
        self.image = self.rotate_image(self.direction)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.x < -100 or self.rect.x > SCREEN_WIDTH + 100 or self.rect.y < -100 or self.rect.y > SCREEN_HEIGHT + 100:
            self.kill()


class CannonFlashFront(pygame.sprite.Sprite):
    def __init__(self, pos, direction, img):
        super().__init__()
        self.original_image = img
        self.image = img.copy()
        self.alpha = 255
        self.angle = 0
        self.rotation_speed = 5
        self.pos = Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.direction = direction
        self.scale = 1.0
        self.damage = 0
        self.heat = 3
        self.piercing = True

    def update(self):
        self.alpha -= 20
        self.angle += self.rotation_speed
        self.scale += 0.03

        rotated = pygame.transform.rotozoom(self.original_image, self.angle, self.scale)
        rotated.set_alpha(self.alpha)
        self.image = rotated
        self.rect = self.image.get_rect(center=self.pos)

        if self.alpha <= 0:
            self.kill()

class CannonFlashSide(pygame.sprite.Sprite):
    def __init__(self, pos, direction, img, drift_dir=1):
        super().__init__()
        self.original_image = img
        self.angle = direction.angle_to(Vector2(1, 0)) + 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.alpha = 255
        self.pos = Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.drift = direction.rotate(90 * drift_dir) * 0.5  # ±90°
        self.scale = 1.0
        self.damage = 0
        self.heat = 3
        self.piercing = True

    def update(self):
        self.alpha -= 25
        self.scale += 0.02
        self.pos += self.drift

        scaled = pygame.transform.rotozoom(self.original_image, self.angle, self.scale)
        scaled.set_alpha(self.alpha)
        self.image = scaled
        self.rect = self.image.get_rect(center=self.pos)

        if self.alpha <= 0:
            self.kill()