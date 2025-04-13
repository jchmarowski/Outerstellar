from player_ships import *

class InventoryItem:
    def __init__(self, name, item_type, quantity=1, data=None):
        self.name = name
        self.type = item_type
        self.quantity = quantity
        self.data = data

    def is_equippable(self):
        return self.type in ["weapon", "device"]

class InventoryManager:
    def __init__(self):
        self.items = []  # List of InventoryItem

    def add_item(self, item: InventoryItem):
        # Merge with existing stack if same name/type and stackable
        for inv_item in self.items:
            if inv_item.name == item.name and inv_item.type == item.type and item.type != "device" and item.type != "weapon" :
                inv_item.quantity += item.quantity
                return
        self.items.append(item)

    def remove_item(self, name, amount=1):
        for item in self.items:
            if item.name == name:
                item.quantity -= amount
                if item.quantity <= 0:
                    self.items.remove(item)
                return True
        return False

    def get_devices(self):
        return [i.data for i in self.items if i.is_device()]

    def get_all(self):
        return self.items[:]




class ShipGridCell:
    def __init__(self, slot_type="X"):
        self.slot_type = slot_type      # e.g., "W1", "W2", "D", "X"
        self.device = None

    def available(self):
        return self.slot_type != "X"

    def fire_group(self):
        if self.slot_type.startswith("W"):
            return self.slot_type       # returns "W1", "W2", etc.
        return None

class ShipGrid:
    def __init__(self, ship_type: ShipType):
        self.ship_type = ship_type
        self.width = len(ship_type.layout[0])
        self.height = len(ship_type.layout)
        self.grid = [
            [ShipGridCell(slot_type) for slot_type in row]
            for row in ship_type.layout
        ]
        # Set cell availability based on layout
        for y in range(self.height):
            for x in range(self.width):
                cell_type = ship_type.get_cell_type(x, y)
                self.grid[y][x].available = cell_type != "X"
                self.grid[y][x].slot_type = cell_type

    def apply_layout_mask(self, mask):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].available = mask[y][x]

    def place_device(self, x, y, item, allow_swap=True):
        cell = self.grid[y][x]

        if not cell.available:
            return False


        if not isinstance(item, InventoryItem):
            return False

        slot_type = cell.slot_type
        if slot_type == "W" and item.type != "weapon":
            return False
        if slot_type == "D" and item.type != "device":
            return False
        if slot_type == "S" and item.type not in ["device", "weapon"]:
            return False

        if cell.device is None:
            cell.device = item.data
            return True

        elif allow_swap:
            old_device = cell.device
            cell.device = item.data
            return InventoryItem(old_device.name, old_device.type, quantity=1, data=old_device)


        return False

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[ny][nx]
                if neighbor.available and neighbor.device:
                    neighbors.append((nx, ny, neighbor.device))
        return neighbors

    def calculate_effective_stats(self):
        combined_stats = {}
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.device:
                    for stat, value in cell.device.base_stats.items():
                        combined_stats[stat] = combined_stats.get(stat, 0) + value

                    neighbors = self.get_neighbors(x, y)
                    for _, _, neighbor in neighbors:
                        buffs = cell.device.apply_buffs(neighbor)
                        for stat, value in buffs.items():
                            combined_stats[stat] = combined_stats.get(stat, 0) + value
        return combined_stats


class CargoGrid:
    def __init__(self, width=8, height=6):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def place_item(self, x, y, item, allow_swap=True):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        if self.grid[y][x] is None:
            self.grid[y][x] = item
            return True

        elif allow_swap:
            old_item = self.grid[y][x]
            self.grid[y][x] = item
            return old_item

        return False

    def remove_item(self, x, y):
        item = self.grid[y][x]
        self.grid[y][x] = None
        return item


class Device:
    def __init__(self, name, device_type, buffs=None):
        self.name = name
        self.type = device_type
        self.buffs = buffs or {}

    def apply_buffs(self, neighbor):
        """Check if this device buffs the neighbor based on its type"""
        if neighbor.type in self.buffs:
            return self.buffs[neighbor.type]
        return {}

def populate_cargo_from_inventory(inv: InventoryManager, cargo: CargoGrid):
    index = 0
    for item in inv.get_all():
        x = index % cargo.width
        y = index // cargo.width
        if y < cargo.height:
            cargo.grid[y][x] = item
            index += 1
        else:
            break  # cargo is full