import pygame
from settings import *
from enemies import Enemy
from random import randint
from player import Player
from pygame.math import Vector2
import numpy as np

current_map = 0
major_locations = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
major_list = major_locations

minor_locations = [100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130]
minor_list = minor_locations

starting_pos = 0

def populate_map(size_of_map=(17, 17), len_major=len(major_list), len_minor = len(minor_list)):
    rows, cols = size_of_map
    array = np.zeros((rows, cols), dtype=int)  # Initialize with zeros
    placed_majors = 0
    placed_minors = 0
    find_starting_pos = 0
    while placed_majors < len_major:
        x, y = np.random.randint(0, rows), np.random.randint(0, cols)
        array[8, 8] = 99 # Place player in the middle
        if array[x, y] == 0:
            neighbors = array[max(0, x - 2):min(rows, x + 3), max(0, y - 2):min(cols, y + 3)]
            if np.all(neighbors == 0):
                rand_loc = randint(0, len(major_list) -1)
                array[x, y] = major_list.pop(rand_loc)
                placed_majors += 1
    while placed_minors < len_minor:
        x, y = np.random.randint(0, rows), np.random.randint(0, cols)
        if array[x, y] == 0:
            neighbors = array[max(0, x - 1):min(rows, x + 2), max(0, y - 1):min(cols, y + 2)]
            if np.all(neighbors == 0):
                rand = randint(0, len(minor_list) -1)
                array[x, y] = minor_list.pop(rand)
                placed_minors += 1
    
    return array

location_map = populate_map()



class Level:
    def __init__(self):
        pass

    def run(self, dt):
        pass

class SmallStars(pygame.sprite.Sprite):
    def __init__(self, camera_shift_x, camera_shift_y):
        super().__init__()
        random_brightness = randint(6, 15)
        random_size = randint(2,3)
        self.image = pygame.Surface((random_size, random_size))
        self.image.fill("white")
        self.image.set_alpha(random_brightness ** 2)
        self.pos = Vector2(randint(-350, SCREEN_WIDTH + 80), randint(-100, SCREEN_HEIGHT + 80))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 0
        self.velocity = Vector2(0,0)
        self.acc = Vector2(camera_shift_x, camera_shift_y)

    def update(self, bullet_time, cam_shift_x, camera_shift_y):
        self.acc = Vector2(cam_shift_x, camera_shift_y)
        self.velocity += self.acc
        self.pos += self.velocity + 1 * self.acc
        self.rect = self.pos
        self.velocity = self.velocity * 0.99
        if self.rect.x < -300 or self.rect.x > SCREEN_WIDTH + 300 or \
                self.rect.y < -300 or self.rect.y > SCREEN_HEIGHT + 300:
            self.kill()

class BigStars(pygame.sprite.Sprite):
    def __init__(self, star1, star2, star3):
        super().__init__()
        random = randint(1,15)
        if random <= 7:
            self.type = 1
            self.image = star1
        elif random <= 14:
            self.type = 2
            self.image = star2
        else:
            self.type = 3
            self.image = star3
            self.shield = 20
            self.energy = 100
        self.pos = (SCREEN_WIDTH + 50, randint(0, SCREEN_HEIGHT))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 0 - randint(1,3)


    def update(self, bullet_time):
        self.rect.x += self.speed * bullet_time -1
        self.destroy()
        self.image.set_alpha(randint(120,240))


    def destroy(self):
        if self.rect.x <= -50:
            self.kill()

