#!/bin/bash
set -e
gunicorn -w $GUNICORN_WORKERS -b 0.0.0.0:5000 api:app;