from widetms.tile_scalers.sentinel_1 import Sentinel1
from widetms.tile_scalers.sentinel_2 import Sentinel2

scalers = {
    'Sentinel-2': Sentinel2(scale_value=65535),
    'Sentinel-1': Sentinel1(scale_value=0)
}


def scale_tile(rs_device, tile, dtype=None):
    if rs_device in scalers:
        return scalers[rs_device].scale(tile, dtype)
    else:
        raise NotImplementedError(f'The {rs_device} scaler is not implemented now.')
