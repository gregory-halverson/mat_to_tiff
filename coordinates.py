# Create map info using spherical datum (2*pi*r is the circumference)
ULC_X = -20015109.354 # upper left corner x
ULC_Y = 10007554.677 # upper left corner y

RASTER_SIZE_METERS = 4631.5 # meter (463.31*10) (463.31 pixel is usually referred to as 500 m product)
MATRIX_SIZE_PIXELS = 240 # each tile in 240 by 240

def coordinates(h, v):
    xlim1 = ULC_X + h * RASTER_SIZE_METERS * MATRIX_SIZE_PIXELS + RASTER_SIZE_METERS / 2
    xlim2 = ULC_X + (h + 1) * RASTER_SIZE_METERS * MATRIX_SIZE_PIXELS + RASTER_SIZE_METERS / 2
    
    ylim1 = ULC_Y - v * RASTER_SIZE_METERS * MATRIX_SIZE_PIXELS - RASTER_SIZE_METERS / 2
    ylim2 = ULC_Y - (v + 1) * RASTER_SIZE_METERS * MATRIX_SIZE_PIXELS - RASTER_SIZE_METERS / 2

    return xlim1, xlim2, ylim1, ylim2