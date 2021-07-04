import attr

from widetms.tile_scalers.base import Scaler


@attr.s
class Sentinel1(Scaler):

    def scale(self, tile, dtype=None):
        return tile