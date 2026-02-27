# map/layer.py
"""MapLayer module.
Provides a simple class to represent a single map layer (ground, path, items).
The layer loads a tileset image and a 2D grid of tile indices.
"""
import pygame
from typing import List, Tuple

class MapLayer:
    def __init__(self, tileset_path: str, tile_width: int, tile_height: int, grid: List[List[int]]):
        """Create a map layer.
        :param tileset_path: Path to the tileset image.
        :param tile_width: Width of a single tile in pixels.
        :param tile_height: Height of a single tile in pixels.
        :param grid: 2D list of tile indices (row‑major).
        """
        self.tileset = pygame.image.load(tileset_path).convert_alpha()
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.grid = grid
        # Calculate number of columns in the tileset image
        self.tileset_cols = self.tileset.get_width() // tile_width

    def draw(self, surface: pygame.Surface, offset: Tuple[int, int] = (0, 0)):
        """Draw the layer onto the given surface.
        :param surface: Target pygame surface.
        :param offset: (x, y) pixel offset for the whole layer (e.g., camera).
        """
        ox, oy = offset
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile_idx in enumerate(row):
                if tile_idx < 0:
                    continue  # -1 means empty/no tile
                # Determine tile position in the tileset
                ts_col = tile_idx % self.tileset_cols
                ts_row = tile_idx // self.tileset_cols
                tile_rect = pygame.Rect(
                    ts_col * self.tile_width,
                    ts_row * self.tile_height,
                    self.tile_width,
                    self.tile_height,
                )
                dest_pos = (ox + col_idx * self.tile_width, oy + row_idx * self.tile_height)
                surface.blit(self.tileset, dest_pos, tile_rect)
