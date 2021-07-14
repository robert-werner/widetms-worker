FROM python:3.7-slim-buster

ENV C_FORCE_ROOT = true

COPY . .
RUN apt update
RUN apt install -y libjemalloc-dev
RUN pip install -r ./requirements.txt
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so
CMD celery -A widetms.worker worker --concurrency 1 --loglevel=INFO -Q tiler