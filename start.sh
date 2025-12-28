#!/bin/bash

echo "🚀 Mixart server ishga tushyapti..."

cd /root/mixart || exit 1

source venv/bin/activate

export PYTHONPATH=/root/mixart

gunicorn main_app:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info
