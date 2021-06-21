import os

from rio_tiler.io import COGReader
from config.celery_app import app
from config.environment import SOURCE_STORAGE


@app.task()
def tile(task):
    filepath = os.path.join(SOURCE_STORAGE, task['filepath'])
    with COGReader(filepath) as georaster:
        _tile = georaster.tile(task['x'], task['y'], task['z'], tilesize=task['resolution']).data[0]
        print(_tile.shape)
        return _tile
