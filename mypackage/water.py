# create NDWI function from green and nir bands

def ndwi(green, nir):
    return (green - nir) / (green + nir)
