import attr

from widetms.tile_scalers.base import Scaler


@attr.s
class Sentinel2(Scaler):
    scale_value = 65535
    in_range = ((0, 4000),)
