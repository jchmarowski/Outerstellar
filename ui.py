import pygame

class UI:
    def __init__(self, surface, pos):
        self.display_surface = surface
        self.pos = pos
        self.max_width = 300
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

