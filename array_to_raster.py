from osgeo import gdal

def array_to_raster(array, dst_filename, wkt_projection, matrix_size_pixels, cell_size_meters, x_min, y_max):
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(dst_filename, matrix_size_pixels, matrix_size_pixels, 1, gdal.GDT_Float32)
    dataset.SetGeoTransform((x_min, cell_size_meters, 0, y_max, 0, -cell_size_meters))
    dataset.SetProjection(wkt_projection)
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.FlushCache()
    dataset = None
