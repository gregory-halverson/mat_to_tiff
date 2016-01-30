import os
import numpy
from glob import glob

from mat_to_tiff import \
    read_matlab_matrix, \
    load_sinusoidal_tile_corners, \
    matrix_to_land_tile_geotiff

MATRICES_DIRECTORY = 'matrices'
MATLAB_VARIABLE_NAME = 'LEptJPL'

TIFF_OUTPUT_DIRECTORY = 'tiff'

sinusoidal_tile_corners = load_sinusoidal_tile_corners()

matlab_file_list = glob(MATRICES_DIRECTORY + '/*.mat')

for matlab_filename in matlab_file_list:
    tiff_filename = TIFF_OUTPUT_DIRECTORY + '/' + os.path.basename(matlab_filename).replace('.mat', '.tif')
    print("converting '%s' to '%s'" % (os.path.basename(matlab_filename), os.path.basename(tiff_filename)))


    hv = os.path.basename(matlab_filename).split('_')[-1].split('.')[0]
    x_min = sinusoidal_tile_corners[hv]['x_min']
    y_max = sinusoidal_tile_corners[hv]['y_max']
    matrix = read_matlab_matrix(matlab_filename, MATLAB_VARIABLE_NAME)
    matrix[numpy.isnan(matrix)] = 0


    matrix_to_land_tile_geotiff(matrix, x_min, y_max, tiff_filename)