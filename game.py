import random
import sys
import pygame
from pygame.math import Vector2
from random import randint
from settings import *
from player import Player
from player_ships import *
from enemies import *
from neutrals import *
from level import Level, SmallStars, BigStars
from ui import UI, ShipGridUI, CargoGridUI
from enum import Enum
from inventory import *
from weapons import *



class GameState(Enum):
    MENU = 1
    RUNNING = 2
    PAUSED = 3
    GAMEOVER = 4


pygame.init()

# Directory for all image to load.
img_dict = {}

random_number = (40,80)



# Draw the game tittle in main
def draw_text_outline_flicker(surface, text, font, pos, text_color, outline_color, flicker_count=12, max_offset=5):
    x, y = pos
    base = font.render(text, True, text_color)

    for _ in range(flicker_count):
        dx = random.randint(1, max_offset)  # pull mostly left, like it’s lagging
        dy = random.randint(-2, 2)
        flicker = font.render(text, True, outline_color)
        flicker.set_alpha(random.randint(30, 140))  # ghosty flicker
        surface.blit(flicker, (x + dx, y + dy))

    surface.blit(base, pos)

class Game:
    def __init__(self, screen):
        pygame.init()
        pygame.mixer.init()
        self.state = GameState.MENU

        self.music_on = False
        self.sfx_on = True
        self.music_volume = 0.2
        self.sfx_volume = 0.2

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.find_mid_point_x = SCREEN_WIDTH / 2
        self.find_mid_point_y = SCREEN_HEIGHT / 2
        self.screen_center = Vector2(int(self.find_mid_point_x), int(self.find_mid_point_y))
        self.target_shift_x = 0
        self.target_shift_y = 0
        self.camera_shift_x = 0
        self.camera_shift_y = 0
        self.zoom = 1.0


        self.load_image("player-scout1", (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE))
        self.load_image("player-scout2", (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE))
        self.load_image("player-scout3", (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE))
        self.load_image("player-scout4", (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE))
        self.load_image("player-scout5", (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE))
        self.load_image("player-scout-mini", (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE))

        self.load_image("blaster_proj", (25, 18))
        self.load_image("blaster_icon", (60, 60))
        self.load_image("blaster_flash1", (45, 55))
        self.load_image("blaster_flash2", (45, 55))
        self.load_image("blaster_flash3", (45, 55))

        self.load_image("cannon_proj", (180, 140))
        self.load_image("cannon_flash_l", (75, 75))
        self.load_image("cannon_flash_r", (75, 75))
        self.load_image("cannon_flash_f", (100, 100))

        self.load_image("bomber", (SMALL_ENEMY_SPRITE_SIZE, SMALL_ENEMY_SPRITE_SIZE))
        self.load_image("bulldog", (SMALL_ENEMY_SPRITE_SIZE, SMALL_ENEMY_SPRITE_SIZE))
        self.load_image("scout", (SMALL_ENEMY_SPRITE_SIZE, SMALL_ENEMY_SPRITE_SIZE))
        self.load_image("gunner", (SMALL_ENEMY_SPRITE_SIZE, SMALL_ENEMY_SPRITE_SIZE))

        self.load_image("ping", (300, 150))
        self.load_image("rocket", (35, 35))
        self.load_image("explosion", (80, 80))
        self.load_image("explosion2", (80, 80))

        # neutrals
        self.load_image("scrap", (40, 40))
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

        self.enemy_types = [
            {"class": Bomber, "weight": 1.0},
            # {"class": Bulldog, "weight": 2.0},
            # {"class": Gunner, "weight": 2.0},
            {"class": Scout, "weight": 1.0},
        ]

        self.weapon_sounds = {
            "blaster": pygame.mixer.Sound("assets/sfx/blaster_basic.wav"),
            "cannon": pygame.mixer.Sound("assets/sfx/cannon.wav")

        }
        for sfx in self.weapon_sounds.values(): sfx.set_volume(0.4)

        self.menu_music = "assets/music/NON_COMMERCIAL_mainmenu.mp3"
        self.game_music_playlist = [
            "assets/music/NON_COMMERCIAL_dnb.mp3",
            "assets/music/NON_COMMERCIAL_dnb2.mp3",
        ]
        self.current_track_index = 0
        for name, sfx in self.weapon_sounds.items():
            sfx.set_volume(self.sfx_volume)



        # Init player and enemy groups.
        player_sprite = Player((650,500), img_dict["player-scout1"], img_dict["player-scout2"], img_dict["player-scout3"], img_dict["player-scout4"], img_dict["player-scout5"], 0.2, img_dict, weapon_sounds=self.weapon_sounds, game=self)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.bullet_time = 1
        self.current_ship = ShipGrid(starter_ship)

        self.neutrals = pygame.sprite.Group()
        self.scrap = pygame.sprite.Group()

        self.enemies = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()

        # Init background effects and UI
        small_star = SmallStars(self.camera_shift_x, self.camera_shift_y)
        self.small_stars = pygame.sprite.Group(small_star)
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            self.small_stars.add(SmallStars(x, y))
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

        # Inventory management
        self.inventory = InventoryManager()
        self.inventory_open = False
        self.ui_blocking_input = False
        self.dragged_item = None
        self.cargo = CargoGrid()
        self.grid_ui = ShipGridUI(self.screen, self.current_ship, pos=(SCREEN_WIDTH - SCREEN_WIDTH/3 + 50, 80), cell_size=SCREEN_WIDTH/32, drag_ref=self)
        self.cargo_ui = CargoGridUI(self.screen, self.cargo, pos=(SCREEN_WIDTH - SCREEN_WIDTH/3, SCREEN_HEIGHT /3), cell_size=SCREEN_WIDTH/32, drag_ref=self)

        self.inventory.add_item(InventoryItem("Blaster", "weapon", data=Blaster(img_dict)))
        self.inventory.add_item(InventoryItem("Blaster", "weapon", data=Blaster(img_dict)))
        self.inventory.add_item(InventoryItem("Cannon", "weapon", data=Cannon(img_dict)))
        self.inventory.add_item(InventoryItem("Cannon", "weapon", data=Cannon(img_dict)))
        self.inventory.add_item(
            InventoryItem("Generator", "device", data=Device("Generator", "device", buffs={"weapon": {"cooldown": -5}})))

        # Use this for item creation: self.inventory.add_item(make_item("Blaster", "weapon", Blaster(img_dict)))
        # Theres a make_item() function before run()

        populate_cargo_from_inventory(self.inventory, self.cargo)

    def get_weapons_by_group(self, group_name):
        weapons = []
        for row in self.current_ship.grid:
            for cell in row:
                if cell.slot_type == group_name and cell.device:
                    if getattr(cell.device, "type", None) == "weapon":
                        weapons.append(cell.device)
        return weapons

    def get_weapon_offset(self, weapon):
        grid = self.current_ship.grid
        cell_size = 10  # match your visual scale
        grid_w = self.current_ship.width
        grid_h = self.current_ship.height

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell.device is weapon:
                    center_x = (grid_w - 1) / 2
                    center_y = (grid_h - 1) / 2

                    dx = (x - center_x) * cell_size
                    dy = (y - center_y) * cell_size  # don't flip yet

                    return Vector2(dx, -dy)  # flip Y here once at the end
        return Vector2(0, 0)

    def play_menu_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.play(-1)  # loop forever

    def play_next_game_track(self):
        if not self.game_music_playlist and self.music_on:
            return
        pygame.mixer.music.stop()
        track = self.game_music_playlist[self.current_track_index]
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()


        self.current_track_index = (self.current_track_index + 1) % len(self.game_music_playlist)

    def camera_shift(self):
        player_pos = self.player.sprite.pos


        dead_zone_radius = 80
        offset_vector = player_pos - self.screen_center
        if offset_vector.length() < dead_zone_radius:
            self.target_shift_x = 0
            self.target_shift_y = 0
        else:
            # Normalize how far player is from center
            offset_x = offset_vector.x / (SCREEN_WIDTH / 2)
            offset_y = offset_vector.y / (SCREEN_HEIGHT / 2)
            scroll_strength = 0.3  # how fast things scroll near edges

            self.target_shift_x = -offset_x * scroll_strength
            self.target_shift_y = -offset_y * scroll_strength

        # Smooth camera easing
        lerp_factor = 0.08
        self.camera_shift_x += (self.target_shift_x - self.camera_shift_x) * lerp_factor
        self.camera_shift_y += (self.target_shift_y - self.camera_shift_y) * lerp_factor

        


    def load_image(self, image_name, scale):
        image = pygame.image.load(f"assets/{image_name}.png").convert_alpha()
        resized = pygame.transform.scale(image, scale)
        img_dict[image_name] = resized

    def choose_weighted_enemy(self):
        total_weight = sum(entry["weight"] for entry in self.enemy_types)
        choice = random.uniform(0, total_weight)
        cumulative = 0
        for entry in self.enemy_types:
            cumulative += entry["weight"]
            if choice <= cumulative:
                return entry["class"]

    def spawn(self):
        EnemyClass = self.choose_weighted_enemy()

        # Pick spawn edge: left, right, top, bottom
        edge = random.choice(["left", "right", "top", "bottom"])
        margin = 100
        if edge == "left":
            pos = Vector2(-margin, random.randint(0, SCREEN_HEIGHT))
        elif edge == "right":
            pos = Vector2(SCREEN_WIDTH + margin, random.randint(0, SCREEN_HEIGHT))
        elif edge == "top":
            pos = Vector2(random.randint(0, SCREEN_WIDTH), -margin)
        else:  # bottom
            pos = Vector2(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + margin)

        if EnemyClass == Bomber:
            enemy = Bomber(pos, img_dict["bomber"], self)
        elif EnemyClass == Scout:
            enemy = Scout(pos, img_dict["scout"], self)

        self.enemies.add(enemy)

    def enemy_fire(self):
        for enemy in self.enemies:
            if enemy.weapon_ready == True:
                if enemy.weapon_type == "standard":
                    attack = Enemy_projectile(enemy.rect.center, enemy.weapon_damage, 0)
                    self.enemy_projectiles.add(attack)
                    enemy.weapon_ready = False
                elif enemy.weapon_type == "radar":
                    if random.randint(0, 2000) < 1:
                        radar = Radar_ping(enemy.rect.center, enemy.weapon_damage, 0, img_dict["ping"], self.player.sprite.rect.center)
                        self.enemy_projectiles.add(radar)
                        enemy.weapon_ready = False
                elif enemy.weapon_type == "rocket":
                    if random.randint(0, 200) < 1:
                        rocket = Rocket(enemy.rect.center, self.player.sprite, img_dict["rocket"], self, img_dict["explosion"], img_dict["explosion2"])
                        self.enemy_projectiles.add(rocket)
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
                        scrap = Scrap(enemy.rect.center, enemy.scrap, img_dict.get("scrap"), img_dict.get("scrap2"))
                        self.neutrals.add(scrap)

        rockets = [r for r in self.enemy_projectiles if isinstance(r, Rocket)]
        for rocket in rockets:
            hits = pygame.sprite.spritecollide(rocket, self.player.sprite.projectiles, False,
                                               pygame.sprite.collide_mask)
            for proj in hits:
                rocket.hp -= proj.damage
                rocket.hit = True
                if not proj.piercing:
                    proj.kill()
                if rocket.hp <= 0:
                    rocket.explode()
                    rocket.kill()

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
                if not projectile.piercing:
                    projectile.kill()
                if player.heat < 100:
                    player.heat += projectile.heat
                if self.player.sprite.hp <= 0:
                    self.state = GameState.GAMEOVER

    def make_item(name, item_type, data):
        return InventoryItem(name=name, item_type=item_type, quantity=1, data=data)

    def run(self):
        while True:
            dt = self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        self.inventory_open = not self.inventory_open
                        self.ui_blocking_input = self.inventory_open
                    if event.key == pygame.K_m:
                        if self.music_on:
                            self.music_on = False
                            pygame.mixer.music.stop()
                        else:
                            self.music_on = True
                    if event.key == pygame.K_n:
                        if self.music_on:
                            self.play_next_game_track()
                    if self.state == GameState.RUNNING and event.key == pygame.K_ESCAPE:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED and event.key == pygame.K_ESCAPE:
                        self.state = GameState.RUNNING
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Only UI handles the mouse click
                    self.ui_blocking_input = True
                    self.grid_ui.handle_mouse_click(event)
                    self.cargo_ui.handle_mouse_click(event)
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.RUNNING:
                self.update_game(dt)
            elif self.state == GameState.PAUSED:
                self.draw_paused()
            elif self.state == GameState.GAMEOVER:
                self.draw_gameover()


            pygame.display.update()

    def update_game(self, dt):

        self.screen.fill("black")
        self.level.run(dt)
        self.collision_checks()
        self.bullet_time = self.player.sprite.bullet_time

        # Background
        if len(self.small_stars.sprites()) < 100:
            spawn_pos = Vector2(
                random.randint(-100, SCREEN_WIDTH + 100),
                random.randint(-100, SCREEN_HEIGHT + 100))
            if not (0 <= spawn_pos.x <= SCREEN_WIDTH and 0 <= spawn_pos.y <= SCREEN_HEIGHT):
                self.small_stars.add(SmallStars(spawn_pos.x, spawn_pos.y))
        self.big_stars.update(self.bullet_time)
        self.small_stars.update(self.bullet_time, self.camera_shift_x, self.camera_shift_y)
        self.big_stars.draw(self.screen)
        self.small_stars.draw(self.screen)
        self.camera_shift()

        # Game objects
        self.player.update()
        self.player.draw(self.screen)
        for sprite in self.player.sprite.projectiles:
            self.screen.blit(sprite.image, sprite.rect)
        self.neutrals.update(self.bullet_time)
        self.neutrals.draw(self.screen)
        if random.randint(0, 100) < 2:  # 2% chance per frame to spawn
            self.spawn()
        self.enemies.update(self.bullet_time)
        self.enemies.draw(self.screen)
        self.enemy_fire()
        self.enemy_projectiles.update(self.bullet_time)
        self.enemy_projectiles.draw(self.screen)

        # UI
        self.hp_bar.show_hp(self.player.sprite.hp, self.player.sprite.max_hp)
        self.en_bar.show_en(self.player.sprite.energy, self.player.sprite.max_energy)
        self.oc_bar.show_oc(self.player.sprite.energy, self.player.sprite.max_energy)
        self.shield_bar.show_shield(self.player.sprite.shield, 100)
        self.heat_bar.show_heat(self.player.sprite.heat, 100)
        self.counter_1.counter_hp(self.player.sprite.hp)
        self.counter_2.counter_en(self.player.sprite.energy)
        self.counter_3.counter_shield(self.player.sprite.shield)
        self.counter_4.counter_heat(self.player.sprite.heat)

        if self.inventory_open:
            self.grid_ui.draw()
            self.cargo_ui.draw()
            if self.dragged_item:
                mx, my = pygame.mouse.get_pos()
                pygame.draw.rect(self.screen, "green", (mx, my, 64, 64), 2)
                font = pygame.font.SysFont(None, 16)
                label = font.render(self.dragged_item.name[:5], True, "green")
                self.screen.blit(label, (mx + 4, my + 4))

        if not pygame.mixer.music.get_busy() and self.music_on:
            self.play_next_game_track()

        if not self.inventory_open:
            self.ui_blocking_input = False

        pygame.display.update()


    def draw_menu(self):
        self.screen.fill("black")
        font = pygame.font.Font("assets/ui/LazenbyCompSmooth.ttf", 80)
        title_pos = (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 5)
        draw_text_outline_flicker(
            self.screen,
            "OUTERSTELLAR",
            font,
            title_pos,
            text_color="white",
            outline_color="purple",
            flicker_count=22,
            max_offset=8)
        start = font.render("Press ENTER to Start", True, "gray")
        self.screen.blit(start, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
        if len(self.small_stars.sprites()) < 100:
            spawn_pos = Vector2(
                random.randint(-100, SCREEN_WIDTH + 100),
                random.randint(-100, SCREEN_HEIGHT + 100))
            self.small_stars.add(SmallStars(spawn_pos.x, spawn_pos.y))
        self.small_stars.update(1, 0.1, 0)
        self.small_stars.draw(self.screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.state = GameState.RUNNING
            self.play_next_game_track()
        self.clock.tick(fps)
        if not pygame.mixer.music.get_busy() and self.music_on:
            self.play_menu_music()
        font_small = pygame.font.Font("assets/ui/LazenbyCompSmooth.ttf", 32)

        # Music toggle
        music_text = "MUSIC: ON" if self.music_on else "MUSIC: OFF"
        music_surface = font_small.render(music_text, True, "white")
        music_rect = music_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(music_surface, music_rect)

        # SFX toggle
        sfx_text = "SFX: ON" if self.sfx_on else "SFX: OFF"
        sfx_surface = font_small.render(sfx_text, True, "white")
        sfx_rect = sfx_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        self.screen.blit(sfx_surface, sfx_rect)

        # Volume info
        volume_text = f"VOL: {int(self.music_volume * 100)}%"
        volume_surface = font_small.render(volume_text, True, "gray")
        self.screen.blit(volume_surface, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200))

        # Handle input clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if music_rect.collidepoint(mouse_pos) and mouse_click:
            self.music_on = not self.music_on
            if self.music_on:
                pygame.mixer.music.set_volume(self.music_volume)
                if not pygame.mixer.music.get_busy():
                    self.play_menu_music()
            else:
                pygame.mixer.music.set_volume(0)

        if sfx_rect.collidepoint(mouse_pos) and mouse_click:
            self.sfx_on = not self.sfx_on


    def draw_paused(self):
        font = pygame.font.SysFont("arial", 60)
        pause = font.render("PAUSED - Press ESC to Resume", True, "yellow")
        self.screen.blit(pause, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2))
        self.clock.tick(fps)

    def draw_gameover(self):
        font = pygame.font.SysFont("arial", 60)
        over = font.render("GAME OVER - Press R to Restart", True, "red")
        self.screen.blit(over, (SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.__init__(self.screen)  # Restart game
            self.state = GameState.MENU
        self.clock.tick(fps)

current_time = pygame.time.get_ticks()

THREE_SECONDS = pygame.USEREVENT + 1
pygame.time.set_timer(THREE_SECONDS, 2000)


if __name__ == "__main__":
    game = Game()
    game.run()