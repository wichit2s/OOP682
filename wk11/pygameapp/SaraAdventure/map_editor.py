import pygame
import sys
import os
import json

# Configuration
TILE_SIZE = 64
GRID_SIZE = 20
SCREEN_WIDTH = TILE_SIZE * GRID_SIZE
SCREEN_HEIGHT = TILE_SIZE * GRID_SIZE
MAP_FILE = os.path.join('map', 'sample_map.json')
TILESET_PATH = os.path.join('assets', 'maps', 'forest_tileset.png')

class MapEditor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Map Editor - Wheel to select, Left click to draw, S to save")
        
        # Load Tileset
        try:
            self.tileset = pygame.image.load(TILESET_PATH).convert_alpha()
        except Exception as e:
            print(f"Error loading tileset: {e}")
            pygame.quit()
            sys.exit()
            
        self.tileset_width = self.tileset.get_width()
        self.tileset_height = self.tileset.get_height()
        self.tileset_cols = self.tileset_width // TILE_SIZE
        self.tileset_rows = self.tileset_height // TILE_SIZE
        self.total_tiles = self.tileset_cols * self.tileset_rows
        
        # Grid Data (3 layers as per requirement: ground, path, items)
        # For simplicity, this editor will edit the 'ground' layer by default.
        # You can switch layers if needed, but we'll start with ground.
        self.current_layer_index = 0 # 0: ground, 1: path, 2: items
        self.layers = self.load_existing_map()
        
        self.selected_tile = 0
        self.clock = pygame.time.Clock()

    def load_existing_map(self):
        if os.path.exists(MAP_FILE):
            try:
                with open(MAP_FILE, 'r') as f:
                    data = json.load(f)
                    return data['layers']
            except Exception as e:
                print(f"Error reading JSON: {e}")
        
        # Fallback empty map
        return [
            {"name": "ground", "tileset": "../assets/maps/forest_tileset.png", "grid": [[0]*GRID_SIZE for _ in range(GRID_SIZE)]},
            {"name": "path", "tileset": "../assets/maps/forest_tileset.png", "grid": [[-1]*GRID_SIZE for _ in range(GRID_SIZE)]},
            {"name": "items", "tileset": "../assets/maps/forest_tileset.png", "grid": [[-1]*GRID_SIZE for _ in range(GRID_SIZE)]}
        ]

    def save_map(self):
        data = {
            "tile_width": TILE_SIZE,
            "tile_height": TILE_SIZE,
            "layers": self.layers
        }
        try:
            with open(MAP_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Map saved to {MAP_FILE}")
        except Exception as e:
            print(f"Error saving map: {e}")

    def get_tile_surface(self, tile_index):
        if tile_index < 0: return None
        tx = (tile_index % self.tileset_cols) * TILE_SIZE
        ty = (tile_index // self.tileset_cols) * TILE_SIZE
        return self.tileset.subsurface((tx, ty, TILE_SIZE, TILE_SIZE))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Mouse Wheel to select tile
                if event.type == pygame.MOUSEWHEEL:
                    self.selected_tile = (self.selected_tile + event.y) % self.total_tiles
                    if self.selected_tile < 0: self.selected_tile += self.total_tiles

                # Keyboard shortcuts
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_map()
                    if event.key == pygame.K_1: self.current_layer_index = 0
                    if event.key == pygame.K_2: self.current_layer_index = 1
                    if event.key == pygame.K_3: self.current_layer_index = 2

            # Mouse input for drawing
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // TILE_SIZE
            grid_y = mouse_pos[1] // TILE_SIZE
            
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]: # Left Click
                    self.layers[self.current_layer_index]['grid'][grid_y][grid_x] = self.selected_tile
                elif mouse_buttons[2]: # Right Click
                    self.layers[self.current_layer_index]['grid'][grid_y][grid_x] = -1

            # Drawing
            self.screen.fill((50, 50, 50))
            
            # Draw layers in order
            for layer in self.layers:
                grid = layer['grid']
                for y in range(GRID_SIZE):
                    for x in range(GRID_SIZE):
                        tile = grid[y][x]
                        if tile != -1:
                            surf = self.get_tile_surface(tile)
                            self.screen.blit(surf, (x * TILE_SIZE, y * TILE_SIZE))

            # Draw grid lines
            for i in range(GRID_SIZE + 1):
                pygame.draw.line(self.screen, (100, 100, 100), (i * TILE_SIZE, 0), (i * TILE_SIZE, SCREEN_HEIGHT))
                pygame.draw.line(self.screen, (100, 100, 100), (0, i * TILE_SIZE), (SCREEN_WIDTH, i * TILE_SIZE))

            # Draw preview under mouse
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                preview = self.get_tile_surface(self.selected_tile)
                if preview:
                    preview.set_alpha(150)
                    self.screen.blit(preview, (grid_x * TILE_SIZE, grid_y * TILE_SIZE))
            
            # Status text
            font = pygame.font.SysFont(None, 24)
            layer_name = self.layers[self.current_layer_index]['name']
            text = font.render(f"Layer: {layer_name} (1,2,3) | Tile: {self.selected_tile} | S to Save", True, (255, 255, 255))
            self.screen.blit(text, (10, SCREEN_HEIGHT - 30))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    editor = MapEditor()
    editor.run()
