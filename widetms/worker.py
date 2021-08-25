import os
import gc
import numpy
from rasterio.dtypes import dtype_ranges

from widetms.tile_scalers.scaler import get_in_range
from config.celery_app import app
from config.environment import SOURCE_STORAGE
from widetms.bp_reader import BandPackageReader
from widetms.tile_scalers.scaler import scale_tile


@app.task()
def tile(task):
    result_tile = None
    try:
        filepaths = [os.path.join(SOURCE_STORAGE, filepath) for filepath in task['filepaths']]
        band_package = list(zip(filepaths, task['bands']))
        with BandPackageReader(band_package, reader_options={'resampling_method': task['resampling']}) as georaster:
            result_tile = georaster.tile(task['x'],
                                         task['y'],
                                         task['z'],
                                         tilesize=task['resolution'],
                                         bands=georaster.bands,
                                         expression=task['expressions'])
            result_tile_data = result_tile.data[0]
            if task['visualize'] is not None:
                return result_tile.post_process(in_range=get_in_range(task['rs_device'])).data[0]
            if task['expressions'] == '':
                if numpy.dtype(task['dtype']) == result_tile_data.dtype:
                    return result_tile_data
                else:
                    result_tile_data = scale_tile(task['rs_device'], result_tile_data, dtype=task['dtype'])
            else:
                result_tile_data = scale_tile(task['rs_device'], result_tile_data)
            return result_tile_data
    except Exception as e:
        raise Exception(str(e))
    finally:
        del result_tile
        gc.collect()
