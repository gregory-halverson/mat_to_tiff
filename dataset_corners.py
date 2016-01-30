def dataset_corners(ds):

    width = ds.RasterXSize
    height = ds.RasterYSize

    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5]  # from
    #http://gdal.org/gdal_datamodel.html
    maxx = gt[0] + width*gt[1] + height*gt[2]  # from
    #http://gdal.org/gdal_datamodel.html
    maxy = gt[3]

    return minx, maxx, miny, maxy