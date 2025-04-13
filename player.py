import pygame
from weapons import *
from math import *
from pygame.math import Vector2
from settings import *



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, img, img_hit, img_hot, img_shield, img_heat_shield, speed, img_dict, weapon_sounds, game):
        super().__init__()
        self.game = game
        self.current_weapon = Cannon(img_dict)
        self.weapon_sounds = weapon_sounds

        self.img_dict = img_dict
        self.normal_image = img
        self.hit_image = img_hit
        self.heat_image = img_hot
        self.shielded_image = img_shield
        self.heat_shield_image = img_heat_shield
        self.image = self.normal_image
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos
        self.velocity = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.max_speed = speed
        self.speed = self.max_speed
        self.rect = self.image.get_rect(center = pos)
        self.angle = 0

        self.max_hp = 1000
        self.hp = self.max_hp
        self.max_energy = 1000
        self.energy = self.max_energy / 2
        self.energy_gen = 1
        self.shield = 0
        self.max_shield = 100
        self.heat = 6
        self.projectiles = pygame.sprite.Group()
        self.bullet_time = 1
        self.hit = False
        self.scrap = 0
        self.boundary_left = False
        self.boundary_right = False
        self.boundary_top = False
        self.boundary_down = False


    def get_input(self):
        # W, S, A, D, L Shift, Space

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and self.pos.x < SCREEN_WIDTH - SCREEN_WIDTH / 4 - 40:
            self.acc.x += self.speed
        if keys[pygame.K_a] and self.pos.x > SCREEN_WIDTH / 4 + 40:
            self.acc.x -= self.speed
        if keys[pygame.K_w] and self.pos.y > SCREEN_HEIGHT / 4:
            self.acc.y -= self.speed
        if keys[pygame.K_s] and self.pos.y < SCREEN_HEIGHT - SCREEN_HEIGHT / 4:
            self.acc.y += self.speed
        if keys[pygame.K_LSHIFT]:
            self.speed = self.max_speed * 4
        if not self.game.ui_blocking_input:
            if pygame.mouse.get_pressed()[0]:  # LMB
                for weapon in self.game.get_weapons_by_group("W1"):
                    self.fire_main(weapon)

            if pygame.mouse.get_pressed()[2]:  # RMB
                for weapon in self.game.get_weapons_by_group("W2"):
                    self.fire_secondary(weapon)
        if keys[pygame.K_SPACE]:
            self.bullet_time = 0.55
        else:
            self.bullet_time = 1


        self.velocity += self.acc
        self.pos += self.velocity + 1 * self.acc
        self.rect = self.pos
        self.acc = Vector2(0,0)
        self.velocity = self.velocity * 0.97




    # Use gun1 (A), position + speed.
    def fire_main(self, weapon):
        if not weapon:
            return

        energy_cost = weapon.get_energy_cost() if hasattr(weapon, "get_energy_cost") else 0
        if self.energy >= energy_cost:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            direction = (mouse_pos - self.pos).normalize()
            offset = self.game.get_weapon_offset(weapon)
            rotated_offset = offset.rotate(-90).rotate(-self.angle)
            origin = self.pos + rotated_offset
            cost = weapon.fire(origin, direction, self.projectiles)

            if cost > 0:
                self.energy -= cost
                if self.game.sfx_on:
                    weapon_name = getattr(weapon, "name", None)
                    sound = self.weapon_sounds.get(weapon_name)
                    if sound:
                        try:
                            sound.set_volume(self.game.sfx_volume)
                            sound.play()
                        except Exception as e:
                            print(f"⚠️ Failed to play sound for {weapon_name}: {e}")
    def fire_secondary(self, weapon):
        if not weapon:
            return

        energy_cost = weapon.get_energy_cost() if hasattr(weapon, "get_energy_cost") else 0
        if self.energy >= energy_cost:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            direction = (mouse_pos - self.pos).normalize()
            offset = self.game.get_weapon_offset(weapon)
            rotated_offset = offset.rotate(-90).rotate(-self.angle)
            origin = self.pos + rotated_offset
            cost = weapon.fire(origin, direction, self.projectiles)


            if cost > 0:
                self.energy -= cost
                if self.game.sfx_on:
                    weapon_name = getattr(weapon, "name", None)
                    sound = self.weapon_sounds.get(weapon_name)
                    if sound:
                        try:
                            sound.set_volume(self.game.sfx_volume)
                            sound.play()
                        except Exception as e:
                            print(f"⚠️ Failed to play sound for {weapon_name}: {e}")

    def boundary(self):
        if self.pos.x <= SCREEN_WIDTH / 4:
            self.acc.x += 0.2
            self.boundary_left = True
            if self.pos.x <= SCREEN_WIDTH / 5:
                self.acc.x += 0.6
        else:
            self.boundary_left = False
        if self.pos.x >= SCREEN_WIDTH - SCREEN_WIDTH / 4:
            self.acc.x -= 0.2
            self.boundary_right = True
            if self.pos.x >= SCREEN_WIDTH - SCREEN_WIDTH / 5:
                self.acc.x -= 0.6
        else:
            self.boundary_right = False
        if self.pos.y <= SCREEN_HEIGHT / 4:
            self.acc.y += 0.2
            self.boundary_top = True
            if self.pos.y <= SCREEN_HEIGHT / 5:
                self.acc.y += 0.6
        else:
            self.boundary_top = False
        if self.pos.y >= SCREEN_HEIGHT - SCREEN_HEIGHT / 4:
            self.acc.y -= 0.2
            self.boundary_down = True
            if self.pos.y >= SCREEN_HEIGHT - SCREEN_HEIGHT / 5:
                self.acc.y -= 0.6
        else:
            self.boundary_down = False




    def update(self):
        self.get_input()
        self.boundary()
        self.projectiles.update()
        mx, my = pygame.mouse.get_pos()
        image_center = pygame.Vector2(self.rect.x, self.rect.y)
        mouse_position = pygame.Vector2(mx, my)
        direction = mouse_position - image_center
        self.angle = direction.angle_to(pygame.Vector2(1, 0))
        rotated_image = pygame.transform.rotate(self.normal_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.rect.x, self.rect.y))
        self.image = rotated_image
        self.rect = rotated_rect

        if self.speed > self.max_speed:
            self.speed -= 0.01

        if self.heat > 5:
            self.heat -= 0.001
        else:
            self.heat -= 0.0005

        if self.energy <= self.max_energy:
            self.energy += self.energy_gen * ((self.max_energy - self.energy)/350)
        elif self.energy > 2 * self.max_energy:
            self.energy = 2 * self.max_energy - 10
        else:
            self.energy -= 1

        #if self.hit:
            self.image = self.hit_image
            self.hit = False
        #elif self.shield > 30 and self.heat < 30:
            self.image = self.shielded_image
        #elif self.shield < 30 and self.heat > 30:
            self.image = self.heat_image
        #elif self.shield > 30 and self.heat > 30:
            self.image = self.heat_shield_image
        #else:

