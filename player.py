import pygame
from projectiles import Projectile
from projectiles import Flash
from math import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, img, img_hit, img_hot, img_shield, img_heat_shield , boundary_width, boundary_height, speed):
        super().__init__()
        self.normal_image = img
        self.hit_image = img_hit
        self.heat_image = img_hot
        self.shielded_image = img_shield
        self.heat_shield_image = img_heat_shield
        self.image = self.normal_image
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.max_x_constraint = boundary_width
        self.max_y_constraint = boundary_height
        self.s1_rdy = True
        self.s1_time = 0
        self.s1_cd = 100
        self.max_hp = 100
        self.hp = self.max_hp
        self.max_energy = 1000
        self.energy = self.max_energy / 2
        self.energy_gen = 0.6
        self.shield = 0
        self.max_shield = 100
        self.heat = 6
        self.projectiles = pygame.sprite.Group()
        self.bullet_time = 1


    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.s1_rdy:
            self.shoot1()
            self.s1_rdy = False
            self.s1_time = pygame.time.get_ticks()
        if keys[pygame.K_s]:
            self.bullet_time = 0.4
        else:
            self.bullet_time = 1

    # Use gun1 (A), position + speed.
    def shoot1(self):
        if self.energy > 100:
            self.projectiles.add(Projectile(self.rect.center, 30))
            self.projectiles.add(Flash(self.rect.center))
            self.energy -= 20


    def recharge(self):
        if not self.s1_rdy:
            current_time = pygame.time.get_ticks()
            if current_time - self.s1_time >= self.s1_cd:
                self.s1_rdy = True
    def boundary(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
        if self.rect.bottom >= self.max_y_constraint:
            self.rect.bottom = self.max_y_constraint
        if self.rect.top <= 0:
            self.rect.top = 0

    def update(self):
        self.get_input()
        self.boundary()
        self.recharge()
        self.projectiles.update()
        if self.heat > 5:
            self.heat -= 0.001
        else:
            self.heat -= 0.0005
        if self.energy <= self.max_energy:
            self.energy += self.energy_gen * ((self.max_energy - self.energy)/150)
        elif self.energy > 2 * self.max_energy:
            self.energy = 2 * self.max_energy - 10
        else:
            self.energy -= 1
        if self.shield > 30 and self.heat < 30:
            self.image = self.shielded_image
        elif self.shield < 30 and self.heat > 30:
            self.image = self.heat_image
        elif self.shield > 30 and self.heat > 30:
            self.image = self.heat_shield_image
        else:
            self.image = self.normal_image
