import traceback

import celery
from celery import states


class BaseTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.log.error(f'{self.name} on {self.worker} failed after {self.execTime} seconds: {exc}')
        self.update_state(state=states.FAILURE, meta={
            'exc_type': type(exc).__name__,
            'exc_message': traceback.format_exc().split('\n')})