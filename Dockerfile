FROM python:3.7-slim-buster

ENV C_FORCE_ROOT = true
RUN apt update
RUN apt install -y libjemalloc-dev
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so
COPY . .
RUN pip install -r ./requirements.txt
CMD celery -A widetms.worker worker --concurrency 1 --loglevel=INFO -Q tiler
