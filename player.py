import pygame
from projectiles import Projectile
from projectiles import Flash

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, boundary_width, boundary_height, speed):
        super().__init__()
        DFLT_IMG_SZ = (100, 100)
        ship1 = pygame.image.load("assets/scout-ship.png").convert_alpha()
        ship1 = pygame.transform.scale(ship1, DFLT_IMG_SZ)
        self.image = ship1
        self.mask = pygame.mask.from_surface(self.image)  # ?????
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.max_x_constraint = boundary_width
        self.max_y_constraint = boundary_height
        self.s1_rdy = True
        self.s1_time = 0
        self.s1_cd = 100
        self.projectiles = pygame.sprite.Group()
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

    # Use gun1 (A), position + speed.
    def shoot1(self):
        self.projectiles.add(Projectile(self.rect.center, 30))
        self.projectiles.add(Flash(self.rect.center))

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
