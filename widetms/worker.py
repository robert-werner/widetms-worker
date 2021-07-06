import os
import gc
import numpy

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
            if task['expressions'] is None:
                if numpy.dtype(task['dtype']) == result_tile.data[0].dtype:
                    return result_tile.data[0]
                else:
                    return scale_tile(task['rs_device'], result_tile.data[0], task['dtype'])
            else:
                return scale_tile(task['rs_device'], result_tile.data[0])
    except Exception as e:
        raise Exception(str(e))
    finally:
        del result_tile
        gc.collect()

