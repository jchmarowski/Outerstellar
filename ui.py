import pygame
from inventory import *
from settings import *

class UI:
    def __init__(self, surface, pos):
        self.display_surface = surface
        self.pos = pos
        self.max_width = 200
        self.height = 7
        self.font = pygame.font.Font("assets/ui/LazenbyCompSmooth.ttf", 24)

    def show_hp(self, current, max):
        current_value = current / max
        current_bar_width = current_value * self.max_width
        gauge_bar = pygame.Rect(self.pos, (current_bar_width, self.height))
        pygame.draw.rect(self.display_surface,"green",gauge_bar)

    def show_en(self, current, max):
        current_value = current / max
        current_bar_width = current_value * self.max_width
        if current_bar_width > self.max_width:
            current_bar_width = self.max_width
        bar = pygame.Rect(self.pos, (current_bar_width, self.height))
        pygame.draw.rect(self.display_surface,"#2A30FA",bar)

    def show_oc(self, current, max):
        self.height = 9
        if current > max:
            overcharged = current - max
            current_value = overcharged / max
            current_bar_width = current_value * self.max_width
            self.displace = current_bar_width
            bar = pygame.Rect(self.pos, (current_bar_width, self.height))
            pygame.draw.rect(self.display_surface,"purple",bar)

    def show_shield(self, current, max):
        current_value = current / max
        current_bar_width = current_value * self.max_width
        if current_bar_width > self.max_width:
            current_bar_width = self.max_width
        bar = pygame.Rect(self.pos, (current_bar_width, self.height))
        pygame.draw.rect(self.display_surface, "cyan", bar)

    def show_heat(self, current, max):
        current_value = current / max
        current_bar_width = current_value * self.max_width
        if current_bar_width > self.max_width:
            current_bar_width = self.max_width
        bar = pygame.Rect(self.pos, (current_bar_width, self.height))
        pygame.draw.rect(self.display_surface, "red", bar)

    def counter_hp(self, value):
        value = int(value)
        counter_surf = self.font.render((str(value)), False, "green")
        counter_rect = counter_surf.get_rect(center=self.pos)
        self.display_surface.blit(counter_surf, counter_rect)

    def counter_en(self, value):
        value = int(value)
        counter_surf = self.font.render((str(value)), False, "#6994F3")
        counter_rect = counter_surf.get_rect(center=self.pos)
        self.display_surface.blit(counter_surf, counter_rect)
    def counter_shield(self, value):
        value = int(value)
        counter_surf = self.font.render((str(value)), False, "cyan")
        counter_rect = counter_surf.get_rect(center=self.pos)
        self.display_surface.blit(counter_surf, counter_rect)
    def counter_heat(self, value):
        value = int(value)
        counter_surf = self.font.render((str(value)), False, "red")
        counter_rect = counter_surf.get_rect(center=self.pos)
        self.display_surface.blit(counter_surf, counter_rect)

class ShipGridUI:
    def __init__(self, surface, grid, pos, cell_size, drag_ref=None):
        self.drag_ref = drag_ref
        self.surface = surface
        self.grid = grid
        self.pos = pos
        self.cell_size = cell_size
        self.selected_device = None
        self.selected_coords = None
        self.selected_origin = None

    def handle_mouse_click(self, event):
        if event.button != 1:
            return

        mx, my = pygame.mouse.get_pos()
        rel_x = mx - self.pos[0]
        rel_y = my - self.pos[1]
        col = int(rel_x // self.cell_size)
        row = int(rel_y // self.cell_size)

        if not (0 <= row < self.grid.height and 0 <= col < self.grid.width):
            return

        cell = self.grid.grid[row][col]

        # 1. PICK UP from ship
        if self.drag_ref.dragged_item is None and cell.device:
            dev = cell.device
            self.drag_ref.dragged_item = InventoryItem(
                dev.name,
                dev.type if hasattr(dev, "type") else "device",  # keep original type!
                quantity=1,
                data=dev
            )
            self.drag_ref.selected_coords = (col, row)
            self.drag_ref.selected_origin = "ship"
            cell.device = None
            print(f"[DEBUG] Pickup: {dev.name} type={dev.type}")
            return

        # 2. PLACE from drag
        if self.drag_ref.dragged_item is not None:
            placed = self.grid.place_device(col, row, self.drag_ref.dragged_item, allow_swap=True)

            if isinstance(placed, InventoryItem):
                # valid swap
                self.drag_ref.dragged_item = placed
                self.drag_ref.selected_coords = (col, row)
                self.drag_ref.selected_origin = "ship"
                return  # allow further dragging
            elif placed is False:
                # invalid drop — bounce back
                if self.drag_ref.selected_origin == "cargo":
                    self.drag_ref.cargo.place_item(*self.drag_ref.selected_coords, self.drag_ref.dragged_item,
                                                   allow_swap=False)
                elif self.drag_ref.selected_origin == "ship":
                    x, y = self.drag_ref.selected_coords
                    self.grid.grid[y][x].device = self.drag_ref.dragged_item.data

            # In all other cases, drop complete
            self.drag_ref.dragged_item = None
            self.drag_ref.selected_coords = None
            self.drag_ref.selected_origin = None

    def draw(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.grid[y][x]
                rect = pygame.Rect(
                    self.pos[0] + x * self.cell_size,
                    self.pos[1] + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                # Draw background
                if not cell.available:
                    pygame.draw.rect(self.surface, "black", rect)
                elif cell.device:
                    pygame.draw.rect(self.surface, "blue", rect)
                else:
                    pygame.draw.rect(self.surface, "gray", rect)
                pygame.draw.rect(self.surface, "black", rect, 1)

                # Optionally render device name
                if cell.device:
                    font = pygame.font.SysFont(None, 16)
                    name_surf = font.render(cell.device.name[:5], True, "white")
                    self.surface.blit(name_surf, rect.topleft)



class CargoGridUI:
    def __init__(self, surface, cargo, pos, cell_size, drag_ref=None):
        self.drag_ref = drag_ref
        self.surface = surface
        self.cargo = cargo
        self.pos = pos
        self.cell_size = cell_size
        self.selected_device = None

    def handle_mouse_click(self, event):
        if event.button != 1:
            return
        mx, my = event.pos
        rel_x = mx - self.pos[0]
        rel_y = my - self.pos[1]
        col = int(rel_x // self.cell_size)
        row = int(rel_y // self.cell_size)

        if not (0 <= row < self.cargo.height and 0 <= col < self.cargo.width):
            return

        if self.drag_ref.dragged_item is None:
            item = self.cargo.grid[row][col]
            if item:
                self.drag_ref.dragged_item = item
                self.drag_ref.selected_coords = (col, row)
                self.drag_ref.selected_origin = "cargo"
                self.cargo.grid[row][col] = None
        else:
            result = self.cargo.place_item(col, row, self.drag_ref.dragged_item, allow_swap=True)
            if isinstance(result, InventoryItem):
                self.drag_ref.dragged_item = result
                self.drag_ref.selected_coords = (col, row)
                self.drag_ref.selected_origin = "cargo"
            else:
                self.drag_ref.dragged_item = None
                self.drag_ref.selected_coords = None
                self.drag_ref.selected_origin = None

    def draw(self):
        for y in range(self.cargo.height):
            for x in range(self.cargo.width):
                rect = pygame.Rect(
                    self.pos[0] + x * self.cell_size,
                    self.pos[1] + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.surface, "gray", rect)
                pygame.draw.rect(self.surface, "black", rect, 1)
                device = self.cargo.grid[y][x]
                if device:
                    font = pygame.font.SysFont(None, 16)
                    label = font.render(device.name[:5], True, "white")
                    self.surface.blit(label, rect.topleft)
                    if device.type != "device" and device.quantity > 1:
                        qty_surf = font.render(f"x{device.quantity}", True, "gray")
                        self.surface.blit(qty_surf, rect.bottomright)

