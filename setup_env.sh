#!/usr/bin/env bash

export APP_SETTINGS="config.DevelopmentConfig"
export FLASK_DEBUG=1
export PY3RUMCAJS_DATABASE_URL='postgresql://rumcajs:turbo@localhost/rumcajs_db'
# psql -U rumcajs rumcajs_db -h 127.0.0.1
celery -A app.celery worker  --loglevel=debug 
