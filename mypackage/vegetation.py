# create ndvi function from nir and red bands
def ndvi(nir, red):
    return (nir - red) / (nir + red)

# NDMI function from nir and swir bands


def ndmi(nir, swir):
    return (nir - swir) / (nir + swir)
