# map/map_loader.py
"""Map loader module.
Loads map configuration from a JSON file and creates MapLayer objects.
"""
import json
import os
import pygame
from .layer import MapLayer

def load_map(json_path: str) -> dict:
    """Load map definition from a JSON file.
    The JSON should contain:
    {
        "tile_width": int,
        "tile_height": int,
        "layers": [
            {
                "name": "ground",
                "tileset": "path/to/tileset.png",
                "grid": [[0,1,...], ...]
            },
            ...
        ]
    }
    Returns a dict mapping layer name to MapLayer instance.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tile_w = data.get('tile_width')
    tile_h = data.get('tile_height')
    layers = {}
    for layer_def in data.get('layers', []):
        name = layer_def['name']
        tileset_path = os.path.join(os.path.dirname(json_path), layer_def['tileset'])
        grid = layer_def['grid']
        layers[name] = MapLayer(tileset_path, tile_w, tile_h, grid)
    return layers
