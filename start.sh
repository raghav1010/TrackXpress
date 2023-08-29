#!/usr/bin/env bash

set -e

export PYTHONUNBUFFERED=1

exec gunicorn -b :5050 main:APP --reload