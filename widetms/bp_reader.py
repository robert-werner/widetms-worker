import os
import typing
from typing import Sequence

import attr
from morecantile import TileMatrixSet
from rio_tiler.constants import WEB_MERCATOR_TMS
from rio_tiler.io import COGReader
from rio_tiler.io.base import MultiBandReader, BaseReader


@attr.s
class BandPackageReader(MultiBandReader):
    band_package: Sequence[typing.Tuple[str, typing.Union[str, bytes, os.PathLike]]] = attr.ib()
    reader: typing.Type[BaseReader] = attr.ib(default=COGReader)
    reader_options: typing.Dict = attr.ib(factory=dict)
    tms: TileMatrixSet = attr.ib(default=WEB_MERCATOR_TMS)

    def dataset(self, band):
        url = self._get_band_url(band)
        with self.reader(url, tms=self.tms, **self.reader_options) as cog:  # type: ignore
            return cog.dataset

    def __attrs_post_init__(self):
        self.bands = sorted(pack[1] for pack in self.band_package)
        self.paths = sorted(pack[0] for pack in self.band_package)
        with self.reader(self._get_band_url(self.bands[0])) as cog:
            self.bounds = cog.bounds
            self.minzoom = cog.minzoom
            self.maxzoom = cog.maxzoom

    def get_item(self, _tuple, key):
        for obj, num in _tuple:
            if obj == key:
                return obj, num

    def _get_band_url(self, band: str) -> str:
        return self.get_item(zip(self.bands, self.paths), band)[1]
