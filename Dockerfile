FROM python:3.7-slim-buster

ENV C_FORCE_ROOT = true

COPY . .
RUN pip install -r ./requirements.txt
CMD celery -A widetms.worker worker --concurrency $(nproc) --loglevel=INFO -Q tiler