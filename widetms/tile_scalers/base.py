import operator
import typing
from functools import reduce

import attr
import numpy as np


@attr.s
class Scaler:
    scale_value: typing.Any = attr.ib()
    scale_op: typing.Any = attr.ib(default=operator.truediv)

    def scale(self, tile, dtype=None):
        if dtype is None:
            return reduce(self.scale_op, [tile, self.scale_value])
        destination_dtype = np.dtype(dtype)
        if np.issubdtype(tile.dtype, np.integer) and np.issubdtype(destination_dtype, np.floating):
            conversion_coef = np.iinfo(tile.dtype).max
            divided_tile = tile / conversion_coef
            return divided_tile.astype(destination_dtype)
        if np.issubdtype(tile.dtype, np.floating) and np.issubdtype(destination_dtype, np.integer):
            conversion_coef = np.iinfo(destination_dtype).max
            tile *= conversion_coef
            return np.round(tile).astype(destination_dtype)
        if np.issubdtype(tile.dtype, np.integer) and np.issubdtype(destination_dtype, np.integer):
            conversion_coef = np.iinfo(destination_dtype).max
            if np.dtype(tile.dtype) > destination_dtype:
                divided_tile = tile / np.iinfo(tile.dtype).max / conversion_coef
                return np.round(divided_tile).astype(destination_dtype)
            if np.dtype(tile.dtype) < destination_dtype:
                return np.round(tile).astype(destination_dtype)


