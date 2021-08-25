from typing import Sequence, Tuple, Union

import numpy
from rio_tiler.constants import NumType
from rio_tiler.utils import linear_rescale

from widetms.tile_scalers.sentinel_1 import Sentinel1
from widetms.tile_scalers.sentinel_2 import Sentinel2

scalers = {
    'Sentinel-2': Sentinel2(scale_value=65535, in_range=((0, 4000),)),
    'Sentinel-1': Sentinel1(scale_value=0, in_range=((0, 4000),))
}


def scale_tile(rs_device, tile, dtype=None):
    if rs_device in scalers:
        return scalers[rs_device].scale(tile, dtype)
    else:
        raise NotImplementedError(f'The {rs_device} scaler is not implemented now.')

def get_in_range(rs_device):
    if rs_device in scalers:
        return scalers[rs_device].in_range
    else:
        raise NotImplementedError(f'The {rs_device} in_range is not implemented now.')


def rescale(
        data: numpy.ndarray,
        mask: numpy.ndarray,
        in_range: Sequence[Tuple[NumType, NumType]],
        out_range: Sequence[Tuple[NumType, NumType]] = ((0, 255),),
        out_dtype: Union[str, numpy.number] = "uint8",
):
    """Rescale data."""
    nbands = data.shape[0]

    if len(in_range) != nbands:
        in_range = ((in_range[0]),) * nbands

    if len(out_range) != nbands:
        out_range = ((out_range[0]),) * nbands

    for bdx in range(nbands):
        data[bdx] = numpy.where(
            mask,
            linear_rescale(
                data[bdx], in_range=in_range[bdx], out_range=out_range[bdx]
            ),
            0,
        )
    return data.astype(out_dtype)