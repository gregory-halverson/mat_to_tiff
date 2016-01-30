import os
import json
import math
import subprocess
from glob import glob
import scipy.io as sio
import numpy
from osgeo import gdal


MODIS_LAND_TILE_WIDTH_METERS = 1111950.5196670014
MODIS_LAND_TILE_PROJECTION_WKT = 'PROJCS["unnamed",GEOGCS["Unknown datum based upon the custom spheroid",DATUM["Not_specified_based_on_custom_spheroid",SPHEROID["Custom spheroid",6371007.181,0]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Sinusoidal"],PARAMETER["longitude_of_center",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]'


path = os.path.dirname(os.path.abspath(__file__))
sinusoidal_tile_corners_filename = path + '/sinusoidal_tile_corners.json'


def read_matlab_matrix(mat_filename, variable_name):
    return sio.loadmat(mat_filename)[variable_name]


def cell_size_meters_from_matrix_size_pixels(matrix_size_pixels):
    return MODIS_LAND_TILE_WIDTH_METERS / matrix_size_pixels


def load_sinusoidal_tile_corners(filename=sinusoidal_tile_corners_filename):
    with open(sinusoidal_tile_corners_filename, 'r') as f:
        sinusoidal_tile_corners = json.loads(f.read())

    return sinusoidal_tile_corners


def array_to_raster(array, dst_filename, wkt_projection, matrix_size_pixels, cell_size_meters, x_min, y_max):
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(dst_filename, matrix_size_pixels, matrix_size_pixels, 1, gdal.GDT_Float32)
    dataset.SetGeoTransform((x_min, cell_size_meters, 0, y_max, 0, -cell_size_meters))
    dataset.SetProjection(wkt_projection)
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.FlushCache()
    dataset = None

    return os.path.exists(dst_filename)


def matrix_to_land_tile_geotiff(matrix, x_min, y_max, destination_filename):
    matrix_size_pixels = int(math.sqrt(matrix.size))
    cell_size_meters = cell_size_meters_from_matrix_size_pixels(matrix_size_pixels)

    return array_to_raster(matrix,
                           destination_filename,
                           MODIS_LAND_TILE_PROJECTION_WKT,
                           matrix_size_pixels,
                           cell_size_meters,
                           x_min, y_max)

def matlab_matrix_to_land_tile_geotiff(matlab_filename, matlab_variable_name, tiff_filename):
    sinusoidal_tile_corners = load_sinusoidal_tile_corners()
    hv = os.path.basename(matlab_filename).split('_')[-1].split('.')[0]
    x_min = sinusoidal_tile_corners[hv]['x_min']
    y_max = sinusoidal_tile_corners[hv]['y_max']
    matrix = read_matlab_matrix(matlab_filename, matlab_variable_name)
    matrix[numpy.isnan(matrix)] = 0
    matrix_to_land_tile_geotiff(matrix, x_min, y_max, tiff_filename)

def matlab_to_global_tiff(matlab_directory, variable_name, output_directory):
    mat_file_list = glob(matlab_directory + '/*.mat')

    os.makedirs(output_directory)

    tiff_file_list = []

    for mat_filename in mat_file_list:
        tiff_filename = output_directory + '/' + os.path.basename(mat_filename).replace('.mat', '.tif')
        tiff_file_list += [tiff_filename]
        print("converting '%s' to '%s'" % (os.path.basename(mat_filename), os.path.basename(tiff_filename)))
        matlab_matrix_to_land_tile_geotiff(mat_filename, variable_name, tiff_filename)

    subprocess.call(['gdal_merge', '-n', '0', '-a_nodata', '0', '-o', output_directory + '/global.tif'] + tiff_file_list)

