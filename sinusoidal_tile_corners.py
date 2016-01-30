import os
import json

path = os.path.dirname(os.path.abspath(__file__))

sinusoidal_tile_corners_filename = path + '/sinusoidal_tile_corners.json'

def load_sinusoidal_tile_corners(filename=sinusoidal_tile_corners_filename):
    with open(sinusoidal_tile_corners_filename, 'r') as f:
        sinusoidal_tile_corners = json.loads(f.read())

    return sinusoidal_tile_corners